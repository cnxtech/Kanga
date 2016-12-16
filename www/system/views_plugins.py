import json
import mimetypes
import tempfile
from help.models import *
from django.core.urlresolvers import reverse
from django.db import transaction
from django.utils.encoding import smart_str
from django.shortcuts import render
from django.http import  HttpResponse, JsonResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
# from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.models import User
from system.plugins_register import *
# import paramiko
import subprocess
import xml.etree.ElementTree as ET
import markdown2
import os
from kanga import settings
from help.models import *
import time

@login_required
def plugins_register(request):
    return render(request,'system/plugin-register-stepwise.html')


@login_required
def plugins_registry_history(request):
    return render(request,'system/plugin-registry-history.html')


@login_required
def plugins_library(request):
    return render(request,'system/plugin-library.html')


@login_required
def get_plugins_registry_history(request):
    histories = RegistryHistory.objects.all()
    history_json_array = []
    node = {"data": history_json_array}
    for history in histories:
        download_url = reverse('system:api-plugins-download-library',args=('history',history.id,))
        history_json_array.append(
            {
                "library_id": history.library_id,
                "user_id": history.user.username,
                "package_location": history.package_location,
                "description": history.description,
                "created": history.created.strftime('%Y-%m-%d %H:%M:%S'),
                "download": "<a href='"+download_url+"'>download</a>",
            }
        )
    return HttpResponse(json.dumps(node), content_type='application/json')


@login_required
def get_plugins_library(request):
    libraries = Library.objects.all()
    library_json_array = []
    node = {"data": library_json_array}
    host = request.build_absolute_uri('/').rstrip('/')
    for library in libraries:
        download_url = reverse('system:api-plugins-download-library',args=('library',library.id,))
        uninstall_url = reverse('system:api-plugins-uninstall-library',args=(library.id,))
        library_json_array.append(
            {
                "name": library.name,
                "version": library.version,
                "owner": library.user.username,
                "package_location": library.package_location,
                "type": library.library_type,
                "description": library.description,
                "created": library.created.strftime('%Y-%m-%d %H:%M:%S'),
                "download": "<a href='"+download_url+"'>download</a>",
                "uninstall": "<a href='javascript:uninstall(\""+host+uninstall_url+"\")'>uninstall</a>",
            }
        )
    return HttpResponse(json.dumps(node), content_type='application/json')


@login_required
def download_plugins_library(request,ref,id):
    file_path = ''
    filename = ''
    if ref=='library':
        library = Library.objects.get(id=id)
        file_path = library.package_location
        filename = library.package_filename
    if ref=='history':
        history = RegistryHistory.objects.get(id=id)
        file_path = history.package_location
        filename = history.package_filename
    response = HttpResponse()
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as fp:
                response = HttpResponse(fp.read())
            content_type, encoding = mimetypes.guess_type(filename)
            if content_type is None:
                content_type = 'application/octet-stream'
            response['Content-Type'] = content_type
            response['Content-Length'] = str(os.stat(file_path).st_size)
            response['Content-Disposition'] = 'attachment; filename='+filename
        return response
    except Exception as e:
        return HttpResponseNotFound('<h1>Download file not found</h1>')


@login_required
@transaction.atomic
def uninstall_plugins_library(request,library_id):
    node = {}
    try:
        library = Library.objects.get(id=library_id)
        description = "["+library.id+"] is successfully uninstalled"
        registry_history = RegistryHistory(description=description,
                                           user=request.user,
                                           package_location=library.package_location,
                                           package_filename=library.package_filename,
                                           library_id=library.id)
        library.delete()
        registry_history.save()
        node = {
            'status':'ok',
            'msg':description
        }
    except Exception as e:
        node = {
            'status':'fail',
            'error':e.message
        }
    return HttpResponse(json.dumps(node), content_type="application/json")


@login_required
def upload(request):
    UPLOAD_DIR = os.path.normpath(os.path.join(settings.BASE_DIR, "system","tmp",))
    tmp_file_prefix = 'zip_'+time.strftime('%Y%m%d_%H%M%S')+'_'
    UPLOAD_DIR = os.path.normpath(tempfile.mkdtemp(prefix=tmp_file_prefix, dir=UPLOAD_DIR))
    node = {}
    try:
        if request.method == 'POST':
            if 'file' in request.FILES:
                file = request.FILES['file']
                filename = os.path.normpath(os.path.join(UPLOAD_DIR,file._name))
                fp = open(filename, 'wb')
                for chunk in file.chunks():
                    fp.write(chunk)
                fp.close()
                node = {
                    'status':'success',
                    'full_path_zip_filename': filename,
                    'zip_filename': file._name
                }
    except Exception as e:
        node = {
            'status': 'fail',
            'error': e.message
        }
    return JsonResponse(node)


@login_required
def verify_plugins(request):
    node = {}
    params = dict()
    try:
        if request.method == 'POST':
            params['dtd_file'] = os.path.normpath(settings.BASE_DIR + '/kanga/library.dtd')
            params['library_zip_file'] = request.POST.get('zip_filename','')
            params['library_zip_file_path'] = request.POST.get('full_path_zip_filename','')
            params['target_zip_file_path'] = os.path.normpath(settings.BASE_DIR + '/system/packages/##library_id##/' + params['library_zip_file'])
            params['tmp_base_folder'] = os.path.normpath(settings.BASE_DIR + '/system/tmp')
            params['tmp_file_prefix'] = 'unzip_'+time.strftime('%Y%m%d_%H%M%S')+'_'
            params['tmp_target_path'] = tempfile.mkdtemp(prefix=params['tmp_file_prefix'], dir=params['tmp_base_folder'])
            params['xml_file'] = os.path.normpath(params['tmp_target_path']+'/library.xml')
            params['tmp_md_target_path'] = os.path.normpath(params['tmp_target_path']+'/doc/*.md')
            params['md_target_path'] = os.path.normpath(settings.BASE_DIR+'/help/doc/')
            unzip(params)
            validate_xml(params)
            node = {
                'status':'success',
                'tmp_target_path': params['tmp_target_path'],
                'message':'successfully verified'
            }
    except Exception as e:
        node = {
            'status':'fail',
            'error': str(e)
        }
    return JsonResponse(node)


@login_required
def register_plugins(request):
    node = {}
    params = dict()
    try:
        if request.method == 'POST':
            params['dtd_file'] = os.path.normpath(settings.BASE_DIR + '/kanga/library.dtd')
            params['library_zip_file'] = request.POST.get('zip_filename','')
            params['library_zip_file_path'] = request.POST.get('full_path_zip_filename','')
            params['tmp_target_path'] = request.POST.get('full_path_unzip_folder','')
            params['target_zip_file_path'] = os.path.normpath(settings.BASE_DIR + '/system/packages/##library_id##/' + params['library_zip_file'])
            params['xml_file'] = os.path.normpath(params['tmp_target_path']+'/library.xml')
            params['tmp_md_target_path'] = os.path.normpath(params['tmp_target_path']+'/doc/*.md')
            params['md_target_path'] = os.path.normpath(settings.BASE_DIR+'/help/doc/')
            params['jar_target_path'] = os.path.normpath(settings.BASE_DIR + '/workspace/builder/lib')
            params['build_xml_path'] = os.path.normpath(settings.BASE_DIR+'/workspace/builder/tmp')
            params['build_template'] = os.path.normpath(settings.BASE_DIR+'/workspace/builder/tmp/build.xml.template')
            params['build_xml'] = os.path.normpath(settings.BASE_DIR+'/workspace/builder/tmp/build.xml')

            clean_up_previous_base_library(params)
            library = register_library_xml_to_db(params, request.user)
            # update_build_xml(params) # required only for java - ant
            node = {
                'status':'success',
                'message':'successfully registered',
                'version': library.id
            }
            clean_tmp_files(params)
    except Exception as e:
        node = {
            'status':'fail',
            'error': e.message
        }
    return JsonResponse(node)
    
    
    
@login_required
def install_plugins(request):
    node = {}
    params = dict()
    try:
        if request.method == 'POST':
            params['dtd_file'] = os.path.normpath(settings.BASE_DIR + '/kanga/library.dtd')
            params['library_zip_file'] = request.POST.get('zip_filename','')
            params['library_zip_file_path'] = request.POST.get('full_path_zip_filename','')
            params['tmp_target_path'] = request.POST.get('full_path_unzip_folder','')
            params['target_zip_file_path'] = os.path.normpath(settings.BASE_DIR + '/system/packages/##library_id##/' + params['library_zip_file'])
            params['xml_file'] = os.path.normpath(params['tmp_target_path']+'/library.xml')
            params['tmp_md_target_path'] = os.path.normpath(params['tmp_target_path']+'/doc/*.md')
            params['md_target_path'] = os.path.normpath(settings.BASE_DIR+'/help/doc/')
            params['jar_target_path'] = os.path.normpath(settings.BASE_DIR + '/workspace/builder/lib')
            params['build_xml_path'] = os.path.normpath(settings.BASE_DIR+'/workspace/builder/tmp')
            params['build_template'] = os.path.normpath(settings.BASE_DIR+'/workspace/builder/tmp/build.xml.template')
            params['build_xml'] = os.path.normpath(settings.BASE_DIR+'/workspace/builder/tmp/build.xml')
            
            # library = register_library_xml_to_db(params, request.user)
            # update_build_xml(params) # required only for java - ant
            npm_install(params)
            node = {
                'status':'success',
                'message':'successfully installed',                
            }            
    except Exception as e:
        node = {
            'status':'fail',
            'error': e.message
        }
    return JsonResponse(node)


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


# def ssh_worker(ip,portnum,userid,pwd,command):
#     result = {"result":"nothing"}
#     try:
#         client = paramiko.SSHClient()
#         client.load_system_host_keys()
#         client.set_missing_host_key_policy(paramiko.WarningPolicy)
#
#         client.connect(ip,port=portnum, username=userid, password=pwd)
#
#         stdin, stdout, stderr = client.exec_command(command)
#         result["result"] = stdout.read()
#
#     except paramiko.BadHostKeyException, e:
#         result["result"] = e
#     except paramiko.AuthenticationException, e:
#         result["result"] = e
#     except paramiko.SSHException, e:
#         result["result"] = e
#
#     finally:
#         client.close()
#
#     return JsonResponse(result)


def markdowntest(request):
    path = "/cepdev/webroot/kanga/markdowntest.md"
    html = markdown2.markdown_path(path)
    return HttpResponse(html)