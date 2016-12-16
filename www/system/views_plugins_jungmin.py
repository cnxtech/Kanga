import json
from django.shortcuts import render
from django.http import  HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import paramiko
import subprocess
import xml.etree.ElementTree as ET
import markdown2
import os, zipfile, shutil, glob
import libxml2
from kanga import settings
import sys
from pywinservicemanager.WindowsServiceConfigurationManager import *

@login_required
def plugins_register(request):
    return render(request,'system/plugin-register-stepwise.html')


@login_required
def upload(request):
    UPLOAD_PATH = os.path.join(settings.BASE_DIR, 'system\\library')
    try:
        if dir_creation(UPLOAD_PATH):
            if request.method == 'POST':
                if 'file' in request.FILES:
                    file = request.FILES['file']
                    filename = file._name

                    fp = open('%s/%s' % (UPLOAD_PATH, filename) , 'wb')
                    for chunk in file.chunks():
                        fp.write(chunk)
                    fp.close()
                    return JsonResponse({'result':'File Uploaded'})
    except Exception as error:
        print "Upload failed!: " + error.message
    return JsonResponse({'result':'Failed to Upload File'})

def dir_creation(dir_path):
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as oserror:
            raise Exception('Make Directory is failed!: ' + oserror.message)
    return True

def find_file(target_path,file_extension):
    try:
        file_path = glob.glob(target_path + '\\' + file_extension)
        temp = file_path[0].split('\\')
        filename = temp[len(temp) - 1]
    except Exception as error:
        raise Exception("Find file failed: " + error.message)
    return filename


def zipfile_decompression(request):
    file_list = {}
    ZIP_TARGET_PATH = os.path.join(settings.BASE_DIR, 'system\\library')
    try:
        zipfile_path = glob.glob(ZIP_TARGET_PATH + '\\*.zip')
        with zipfile.ZipFile(zipfile_path[0],'r') as z:
            z.extractall(ZIP_TARGET_PATH)
            file_list['file_list'] = z.namelist()
    except Exception as ziperror:
        raise Exception('Extract zip is failed: ' + ziperror.message)
    return JsonResponse(file_list)

def folder_validation(request):
    LIBRARY_PATH = os.path.join(settings.BASE_DIR, 'system\\library')
    if request.method == 'POST':
        folder_path = request.POST.get('foldername','')
        if os.path.exists(LIBRARY_PATH + '\\' + folder_path):
            return JsonResponse({'folder_exist':'True'})
    return JsonResponse({'folder_exist':'False'})

def file_validation(request):
    LIBRARY_PATH = os.path.join(settings.BASE_DIR, 'system\\library')
    if request.method == 'POST':
        file_extension = request.POST.get('file_extension','')
        try:
            file_path = glob.glob(LIBRARY_PATH + '\\' + file_extension)
            temp = file_path[0].split('\\')
            filename = temp[len(temp) - 1]
        except Exception as error:
            raise Exception("Validation and Move failed: " + error.message)
    return JsonResponse({'file_exist':'True','file_name':filename})

# def extract_zip_file(request):
#     file_list = {}
#     ZIP_TARGET_PATH = os.path.join(settings.BASE_DIR, 'system\\library')
#     JAR_PATH = os.path.join(settings.BASE_DIR, 'workspace\\builder\\lib')
#     try:
#         zipfile_path = glob.glob(ZIP_TARGET_PATH + '\\*.zip')
#         with zipfile.ZipFile(zipfile_path[0],'r') as z:
#             z.extractall(ZIP_TARGET_PATH)
#             file_list['file_list'] = z.namelist()
#
#             jarfilename = find_file(ZIP_TARGET_PATH,"*.jar")
#             shutil.move( ZIP_TARGET_PATH + '\\' + jarfilename , JAR_PATH + '\\' + jarfilename )
#     except Exception as ziperror:
#         raise Exception('Extract zip is failed: ' + ziperror.message)
#     return JsonResponse(file_list)

def xml_validation(request):
    DTD_FILE_PATH = os.path.join(settings.BASE_DIR,'system\\sample.dtd')
    LIBRARY_PATH = os.path.join(settings.BASE_DIR,'system\\library')
    if request.method == 'POST':
        XML_FILE_PATH = LIBRARY_PATH + '\\' + request.POST.get('filename','')
        if validXML(DTD_FILE_PATH,XML_FILE_PATH):
            return JsonResponse({'result':'True'})
    return JsonResponse({'result':'True'})


def validXML(dtd_file,xml_file):
    try:
        dtd = libxml2.parseDTD(None, dtd_file)
        ctxt = libxml2.newValidCtxt()
        doc = libxml2.parseFile(xml_file)
        ret = doc.validateDtd(ctxt, dtd)
        if ret != 1:
            return False
        doc.freeDoc()
        dtd.freeDtd()
        del dtd
        del ctxt
    except Exception as e:
        raise Exception("validation is failed due to " + e.message)

    return True


def get_windows_services_status(request):
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
        services = QueryAllServicesStatus()
        kanga_services = []
        for service in services:
            if 'Kanga' in str(service['DisplayName']):
                service_configuration = GetService( str(service['ServiceName']) ).Configurations
                service_status = { 'state':str(service['CurrentState']),
                                   'servicename':str(service['ServiceName']),
                                   'description':str(service_configuration['Description']),
                                   'starttype':str(service_configuration['StartType'])}
                kanga_services.append(service_status)
    except Exception as error:
        return JsonResponse({'result': 'fail', 'message': error.message})

    return JsonResponse({'result':'success', 'srvs_status':kanga_services})


def service_onoff(request):
    try:
        if request.method == 'POST':
            servicename = request.POST.get('servicename','')
            ison = request.POST.get('ison','')
            print type(bool(ison))
            if ServiceExists(servicename):
                service = GetService(servicename)
                if bool(ison):
                    service.Start()
                # elif ison == 'False':
                else:
                    service.Stop()
                # else:
                #     return JsonResponse({'result':'fail', 'message':'Please put on/off parameter into api url'})
        else:
            return JsonResponse({'result':'fail', 'message':'Do not support GET method'})
    except Exception as error:
        return JsonResponse({'result':'fail', 'message':error.message})
    return JsonResponse({'result':'success'})


# def get_ide_hosts():
#     services = Service.objects.filter(code=Service.DJANGO, name__icontains='IDE').distinct()
#     host = services[0].node.ip
#     return host

@login_required
def check(request):
    LIB_DIR = settings.BASE_DIR+'/workspace/builder/lib/'
    files = os.listdir(LIB_DIR)
    node = {
        'result': files
    }
    return JsonResponse(node)


def delete(request):
    result = {}
    cmd = ['rm','/cepdev/webroot/kanga/workspace/builder/lib/' + request.GET.get('param','') ]
    result["result"] = process(cmd)
    return JsonResponse(result)

def process(cmd):
    try:
        fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        data = fd_popen.read().strip()
        fd_popen.close()

    except subprocess.CalledProcessError as e:
        raise Exception ('ERROR: Exception running command : ' + cmd + "\nException : " + str(e))
    except UnicodeError as e:
        raise Exception ('ERROR: Exception running command : ' + cmd + "\nException : " + str(e))

    return data


def ssh_worker(ip,portnum,userid,pwd,command):
    result = {"result":"nothing"}
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)

        client.connect(ip,port=portnum, username=userid, password=pwd)

        stdin, stdout, stderr = client.exec_command(command)
        result["result"] = stdout.read()

    except paramiko.BadHostKeyException, e:
        result["result"] = e
    except paramiko.AuthenticationException, e:
        result["result"] = e
    except paramiko.SSHException, e:
        result["result"] = e

    finally:
        client.close()

    return JsonResponse(result)


def markdowntest(request):
    path = "/cepdev/webroot/kanga/markdowntest.md"
    html = markdown2.markdown_path(path)
    return HttpResponse(html)