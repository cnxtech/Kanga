from django.http import HttpResponse
from urllib2 import urlopen, Request, URLError, HTTPError
import json
from time import gmtime, strftime

# from pywinservicemanager.WindowsServiceConfigurationManager import *
from django.core.urlresolvers import reverse

from system.models import Config


def get_config_list(request):
    node = {}
    config_list = list()
    host = request.build_absolute_uri('/').rstrip('/')
    viewer_uri = reverse('system:api-settings-config')
    actions = lambda config_file, config_id: "<a href='javascript:view_file_content(\""+host+viewer_uri+"?command=get&config_id="+config_id+"\")'>"+config_file+"</a>"
    try:
        configs = Config.objects.all()
        for config in configs:
            config_list.append({
                'service_name': config.service.name,
                'config_file': actions(config.filename, str(config.id)),
                'updated': config.updated.strftime('%Y-%m-%d %H:%M:%S')
            })
        node = {
            'data':config_list
        }
    except Exception as e:
        print e
    return HttpResponse(json.dumps(node), content_type="application/json")


def config(request):
    node = {}
    try:
        config_id = request.POST.get('config_id', request.GET.get('config_id', ''))
        command = request.POST.get('command', request.GET.get('command', ''))
        content = request.POST.get('content', request.GET.get('content', ''))
        if command=="get":
            config = Config.objects.get(id=config_id)
            with file(config.filename) as f:
                content = f.read()
            node = {
                'content': content
            }
        elif command=="set":
            config = Config.objects.get(id=config_id)
            config.content = content
            f = open(config.filename,'w+')
            f.write(content)
            node = {
                'state': 'success'
            }
    except Exception as e:
        node = {
            'state': 'failure',
            'error': str(e)
        }
    return HttpResponse(json.dumps(node), content_type="application/json")


def set_config(request):
    node = {}
    content = ''
    try:
        config_id = request.POST.get('config_id', request.GET.get('config_id', ''))
        content = request.POST.get('content', request.GET.get('content', ''))
        config = Config.objects.get(id=config_id)
        with file(config.filename) as f:
            content = f.read()
    except Exception as e:
        print e
    node = {
        'content': content
    }
    return HttpResponse(json.dumps(node), content_type="application/json")




# def get_services_status(request):
#     services = list()
#     host = request.build_absolute_uri('/').rstrip('/')
#     run_command_uri = reverse('system:api-run-command')
#     actions = lambda service_name, command: "<a href='javascript:run_command(\""+host+run_command_uri+"?service_name="+service_name+"&command="+command+"\")'>"+command+"</a>"
#     try:
#         windows_services = QueryAllServicesStatus()
#
#         for service in windows_services:
#             if 'Kanga' in str(service['ServiceName']):
#                 command = "stop"
#                 state_button = ""
#                 service_name = str(service['ServiceName'])
#                 state = str(service['CurrentState'])
#                 service_configuration = GetService(service_name).Configurations
#                 description = str(service_configuration['Description'])
#                 start_type = str(service_configuration['StartType'])
#
#                 if state == "RUNNING":
#                     command = "stop"
#                     state_button = '<button class="btn btn-success btn-xs">'+state+'</button>'
#                 elif state == "STOPPED":
#                     command = "start"
#                     state_button = '<button class="btn btn-danger btn-xs">'+state+'</button>'
#                 elif state == "PAUSED":
#                     command = "start"
#                     state_button = '<button class="btn btn-warning btn-xs">'+state+'</button>'
#                 else:
#                     command = "restart"
#                 service_status = { 'state': state_button,
#                                    'service_name': service_name,
#                                    'description': description,
#                                    'start_type': start_type,
#                                    'actions': actions(service_name,command),
#                                    'checked': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
#                                    }
#                 services.append(service_status)
#     except Exception as e:
#         service_status = { 'state': 'ERROR',
#                            'service_name': 'Windows services',
#                            'description': e.message,
#                            'start_type': 'NA',
#                            'actions': 'Please contact Kanga administrator',
#                            'checked': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
#                            }
#         services.append(service_status)
#     node = {'data':services}
#     return HttpResponse(json.dumps(node), content_type="application/json")


# def run_command(request):
#     node = {}
#     state = 'fail'
#     message = ''
#     service_name = ''
#     try:
#         command = request.POST.get('command', request.GET.get('command', ''))
#         service_name = request.POST.get('service_name', request.GET.get('service_name', ''))
#         if ServiceExists(service_name):
#             service = GetService(service_name)
#             if command == "start":
#                 service.Start()
#                 message = service_name + ' is now RUNNING'
#                 state = 'success'
#             elif command == "stop":
#                 service.Stop()
#                 message = service_name + ' is now STOPPED'
#                 state = 'success'
#             elif command == "restart":
#                 service.Stop()
#                 service.Start()
#                 message = service_name + ' is now RESTARTING'
#                 state = 'success'
#         if state == 'fail':
#             message = service_name + ' does not EXIST'
#     except Exception as e:
#         message = service_name + ": " + str(e)
#     node = {
#         'state': state,
#         'message': message
#     }
#     return HttpResponse(json.dumps(node), content_type="application/json")