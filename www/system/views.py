from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import  HttpResponse, JsonResponse , HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from time import gmtime, strftime
from system.models import Node, Config, Service,ConnectedDevice
from help.models import Library
from system.forms import ConnectedDeviceForm
import urllib2
import subprocess
import json
import zipfile
import socket
import mimetypes
import os
import pprint

# Create your views here.

def index(request):
    return render(request, 'system/index.html')

def plugins(request):
    return render(request, 'system/plugins_index.html')


@login_required
def summary(request):
    context = {
        'IP': 'localhost'
    }
    try:
        nodes = Node.objects.all()
        ip = request.POST.get('ip', request.GET.get('ip', ''))
        context['nodes'] = nodes
        if ip != '':
            context['IP'] = ip
    except Exception as e:
        print e
    return render(request,'system/summary.html',context)

@login_required
def settings(request):
    context = {
        'IP': 'localhost'
    }
    try:
        nodes = Node.objects.all()
        ip = request.POST.get('ip', request.GET.get('ip', ''))
        context['nodes'] = nodes
        if ip != '':
            context['IP'] = ip
    except Exception as e:
        print e
    return render(request,'system/settings.html',context)


@login_required
def ip_settings(request):
    context = {}
    service_list = list()
    try:
        services = Service.objects.all()
        for service in services:
            url = request.build_absolute_uri('/').rstrip('/') + reverse('data:update-ip') + "?code="+service.code
            service_code = service.code
            ip = '<a href="javascript:bootbox_ip_settings(\''+url+'\',\''+service_code+'\')">'+service.node.ip+'</a>'
            service_list.append({
                'node': ip,
                'name': service.name,
                'port': service.port,
                'active': service.active,
                'purpose': service.purpose
            })
    except Exception as e:
        print e
    context = {
        'services': service_list
    }
    return render(request,'system/ip-settings.html',context)

@login_required
def settings_detail(request,hostname,id):
    nodes = {}
    detail = None
    content = None
    roots = dict()
    roots['kafka'] = '/cepdev/kafka_2.10-0.8.2.2/config/'
    roots['zookeeper'] = '/cepdev/kafka_2.10-0.8.2.2/config/'
    roots['elasticsearch'] = '/cepdev/elasticsearch-1.7.1/config/'
    roots['storm'] = '/cepdev/apache-storm-0.9.5/conf/'
    try:
        nodes = Node.objects.all()
        detail = Config.objects.get(pk=id)
        code = detail.service.code.lower()
        full_path = roots[code]+detail.filename
        with file(full_path) as f:
            content = f.read()
            print content
    except Exception as e:
        print str(e)
    context = {
        'nodes': nodes,
        'detail': detail,
        'content': content
    }
    return render(request,'system/settings-detail.html', context)


@login_required
def node(request):
    return render(request,'system/node.html')

@login_required
def threshold_settings(request):
    return render(request,'system/threshold_settings.html')



def storm(request):
    return render(request,'system/storm.html')

def node_metrics(request):
    return render(request, 'system/node-metrics.html')



# This method parse the threshold json while saving the settings
def parse_json(json_, condition, metric_name):
    array = json_[condition]
    out = [];
    for metric in array:
        if (metric['metric_name'] == metric_name):
            out.append(metric['from'])
            out.append(metric['to'])
    return out

@login_required
def connected_devices(request):
    return render(request, 'system/connected_device.html')


def get_deviceList(request):
    result = {}
    connected_devices = ConnectedDevice.objects.all()
    connected_devices_array= []
    result ={
        "data": connected_devices_array
    }
    for connected_device in connected_devices :
        connected_devices_array.append(
            {
                "ip": connected_device.ip,
                "device type": connected_device.deviceType,
                "hostname": connected_device.hostname
            }
        )
    return HttpResponse(json.dumps(result), content_type="application/json")

def api_get_devicesStatus(request):
    result = {}
    response_data = ''
    connected_devices = ConnectedDevice.objects.all()
    connected_devices_status_array = []
    result = {
        "data": connected_devices_status_array
    }

    for device in connected_devices :
        url = 'http://' + str(device.ip) + ':8888/system/ttl/'
        try:
            res = urllib2.urlopen(url, timeout=2)
            response_data = json.loads(res.read())
            res.close()

            anchor = lambda ip: "<a href='/system/connected_device/details/?ip=" + str(ip) + "'>"+str(ip)+"</a>"
            action = lambda ip: '<a href="javascript:ajax_npm_install(\'' + str(ip) + '\')">npm install</a>'

            connected_devices_status_array.append({
                "ip": anchor(device.ip),
                "device_type": device.deviceType,
                "cpu": response_data['cpu'],
                "memory": response_data['freemem'],
                "status": 'up',
                "lib_version": response_data['base_lib_ver'],
                "action": action(device.ip),
                "description": device.description
            })
        except Exception as e:
            connected_devices_status_array.append({
                "ip": device.ip,
                "device_type": device.deviceType,
                "cpu": 'N/A',
                "memory": 'N/A',
                "status": 'down',
                "lib_version": 'N/A',
                "action": 'N/A',
                "description": device.description
            })
    return HttpResponse(json.dumps(result), content_type="application/json")

def api_get_device_details(request):
    result={}
    ip = request.POST.get('ip','')
    device_detail_array = []

    result = {
        "data": device_detail_array
    }
    try:
        url = 'http://' + str(ip) + ':8888/topology'
        res = urllib2.urlopen(url, timeout=5)
        response_data = res.read()
        res.close()
        response_data = json.loads(response_data)

        for info in response_data['info']:
            if info['name'] == '_Kanga_Supervisor':
                action = '<a href="javascript:ajax_start_topology(\'' + str(ip) + '\',\'' + str(info['name']) + '\',true)">Restart</a>'
            elif 'KangaTopology' in info['name']:
                if info['pm2_env']['status'] == 'online':
                    action = '<a href="javascript:ajax_stop_topology(\'' + str(ip) + '\',\'' + str(info['name']) + '\')">Stop</a> | <a href="javascript:ajax_kill_topology(\'' + str(ip) + '\',\'' + str(info['name']) + '\')">Kill</a>'
                else:
                    action = '<a href="javascript:ajax_start_topology(\'' + str(ip) + '\',\'' + str(info['name']) + '\',false)">Start</a> | <a href="javascript:ajax_kill_topology(\'' + str(ip) + '\',\'' + str(info['name']) + '\')">Kill</a>'
            else:
                if info['pm2_env']['status'] == 'online':
                    action = '<a href="javascript:ajax_stop_topology(\'' + str(ip) + '\',\'' + str(info['name']) + '\')">Stop</a>'
                else:
                    action = '<a href="javascript:ajax_start_topology(\'' + str(ip) + '\',\'' + str(info['name']) + '\',false)">Start</a>'

            device_detail_array.append(
                {
                    "pid": info['pid'],
                    "name": info['name'],
                    "status": info['pm2_env']['status'],
                    "created_at": info['pm2_env']['created_at'],
                    "uptime": info['pm2_env']['pm_uptime'],
                    "restart_time": info['pm2_env']['restart_time'],
                    "cpu": info['monit']['cpu'],
                    "memory": int(info['monit']['memory']) / 1024 / 1024,
                    "action": action
                }
            )

    except Exception as e:
        print 'exception occur : ', str(e)

    return HttpResponse(json.dumps(result), content_type="application/json")


def set_device(request):
    result={}
    device_type = request.POST.get('device_type', '')
    ip = request.POST.get('ip','')
    hostname = request.POST.get('hostname', '')
    description = request.POST.get('description','')

    try:
        if ConnectedDevice.objects.filter(ip=ip).exists():
            device = ConnectedDevice.objects.get(ip=ip)
            device.device_type = device_type
            device.hostname = hostname
            device.description = description
            device.save()
        else:
            device = ConnectedDevice(ip=ip, deviceType=device_type, hostname=hostname, description=description)
            device.save()
        result = {
            'status': 'ok',
            'message': 'device registered successfully.'
        }
    except Exception as e:
        result = {
            'status': 'failed',
            'message': str(e)
        }
    return HttpResponse(json.dumps(result), content_type="application/json")

def delete_device(request):
    result = {}
    status =''
    msg = ''
    ip_arr = request.POST.getlist('ip_arr[]', '')
    err_flag = 0
    for ip in ip_arr:
        try:
            if ConnectedDevice.objects.filter(ip=ip).exists():
                device = ConnectedDevice.objects.get(ip=ip)
                device.delete()
                status = 'ok'
                msg = 'Device deleted successfully.'
        except Exception as e:
            status = 'failed'
            msg = 'Error occur : ' + str(e)

    result ={
        'status': status,
        'message': msg
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
def connected_device_details(request):
    context = {}
    ip = request.GET.get('ip', '')
    context = {
        'ip': ip
    }
    return render(request, 'system/connected_device_details.html', context)

def api_remote_downdload_library(request):
    result = {}

    library = Library.objects.get(library_type='BASE_LIBRARY')
    file_path = library.package_location
    filename = library.package_filename
    base_library_full_path = ''
    base_library_name =''

    extract_path = file_path[:file_path.index(filename)] + os.path.splitext(filename)[0]
    print extract_path
    if not os.path.exists(file_path):
        os.mkdir(extract_path)
    response = HttpResponse()
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as z:
                z.extractall(extract_path)

            files = os.listdir(extract_path)
            for file in files :
                if '.zip' in file:
                    base_library_name= file
                    base_library_full_path = os.path.join(extract_path, file)
            if base_library_full_path =='':
                raise Exception('File Not Found')

            print base_library_full_path
            with open(base_library_full_path, 'rb') as fp:
                response = HttpResponse(fp.read())
            content_type, encoding = mimetypes.guess_type(base_library_name)
            if content_type is None:
                content_type = 'application/octet-stream'
            response['Content-Type'] = content_type
            response['Content-Length'] = str(os.stat(base_library_full_path).st_size)
            response['Content-Disposition'] = 'attachment; filename='+base_library_name
        return response
    except Exception as e:
        return HttpResponseNotFound('<h1>Download file not found</h1>')
