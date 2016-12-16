import pprint

from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from urllib2 import urlopen, Request, URLError, HTTPError

from system.models import Service,Node
from views_services import get_storm_hosts, is_number
import json
import time


def index(request):
    return render(request, 'monitor/index.html')


def storm_settings(request):
    hosts = Service.objects.values_list('node', flat=True).filter(code=Service.STORM, name__icontains='ui').distinct()
    context = {'IP': hosts[0]}
    return render(request, 'monitor/storm_settings.html', context)

def streaming_queries_history(request):
    hosts = Service.objects.values_list('node', flat=True).filter(code=Service.STORM, name__icontains='ui').distinct()
    context = {'IP': hosts[0]}
    return render(request, 'monitor/streaming_queries_history.html', context)

def batch_queries_history(request):
    return render(request, 'monitor/batch_queries_history.html')


def running_queries(request):
    return render(request, 'monitor/running_queries.html')

def registered_topology(request):
    return render(request, 'monitor/registered_topology.html')

def get_recent_topology_id():
    try:
        timeout = 2
        hosts = get_storm_hosts()
        url = 'http://'+hosts[0]+'/api/v1/topology/summary'
        data = json.loads(urlopen(Request(url), timeout=timeout).read())
        for topology in data['topologies']:
            return  topology['id']
    except (URLError, HTTPError) as e:
        print e
    return None


def topology_summary(request,id=None):
	nodes = Node.objects.all()
	print nodes
	print nodes[0].ip
	context = {'IP': nodes[0].ip}
	return render(request, 'monitor/topology_summary.html', context)
    

