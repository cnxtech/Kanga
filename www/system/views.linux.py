from django.shortcuts import render
from django.http import  HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from time import gmtime, strftime
from system.models import Node, Config
import subprocess
import json
import pprint

# Create your views here.
@login_required
def summary(request,ip='all'):
    services = list()
    nodes = {}
    try:
        nodes = Node.objects.all()
        p = subprocess.Popen(['/usr/local/bin/supervisorctl','status'],stdout=subprocess.PIPE)
        ret = p.communicate()
        lines = ret[0].split('\n')

        for line in lines:
            if line == '':
                continue
            contents = line.split('  ')
            size = len(contents)
            state = contents[size-2].strip()
            name = contents[0]
            actions = '<button type="button" class="action_button btn btn-primary btn-xs" value="start_'+name+'"><i class="fa fa-play"></i> Start</button> <button type="button" class="action_button btn btn-info btn-xs" value="tail_'+name+'">Tail Log</button>'
            if state == "RUNNING":
                state = '<span class="label label-info">'+state+'</span>'
                actions = '<button type="button" class="action_button btn btn-primary btn-xs" value="restart_'+name+'"><i class="fa fa-refresh"></i> Restart</button> <button type="button" class="action_button btn btn-danger btn-xs" value="stop_'+name+'"><i class="fa fa-stop"></i> Stop</button> <button type="button" class="action_button btn btn-info btn-xs" value="tail_'+name+'">Tail Log</button>'
            elif state == "STOPPED":
                state = '<span class="label label-warning">'+state+'</span>'
            else:
                state = '<span class="label label-danger">'+state+'</span>'
            service = {
                'name':name,
                'state':state,
                'description':contents[size-1].strip(),
                'checked': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                'actions': actions
            }
            services.append(service)
    except Exception as e:
        service = {
                'name':'supervisorctl',
                'state':'ERROR',
                'description':str(e),
                'checked': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                'actions': 'restart, etc'
        }
        services.append(service)
    context = {
        'services':services,
        'nodes': nodes
    }
    return render(request,'system/summary.html',context)

@login_required
def settings(request,ip='all'):
    nodes = {}
    settings = {}
    try:
        nodes = Node.objects.all()
        if ip=='all':
            settings = Config.objects.all()
        else:
            settings = Config.objects.filter(service__node__ip=ip)
    except Exception as e:
        print str(e)
    context = {
        'nodes': nodes,
        'settings': settings,
    }
    return render(request,'system/settings.html', context)

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


