import pprint

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from system.models import Service
from urllib2 import urlopen, Request, URLError, HTTPError
import json
import time
import re
from django.shortcuts import render
import os
import psutil
import subprocess

def get_storm_hosts():
    services = Service.objects.filter(code=Service.STORM, name__icontains='ui').distinct()
    hosts = []
    for host in services:
        hosts.append(host.node.ip+":"+str(host.port))
    return hosts



def storm_topology_details(request,id):
    node = {}
    try:
        pattern = "KangaTopology[0-9]+\-[0-9\-]{1,28}"
        if re.match(pattern,id) is None:
            id = find_actual_id(id)
        if id is None:
            node = {
                'error': 'There is no matched running query in the realtime processing service',
            }
        else:
            timeout = 2
            hosts = get_storm_hosts()
            url = 'http://'+hosts[0]+'/api/v1/topology/'+id
            data = json.loads(urlopen(Request(url), timeout=timeout).read())
            topology = dict()
            topology['status'] = data['status']
            topology['name'] = data['name']
            topology['executorsTotal'] = data['executorsTotal']
            topology['workersTotal'] = data['workersTotal']
            topology['tasksTotal'] = data['tasksTotal']
            topology['uptime'] = data['uptime']
            configuration = dict()
            for key, value in data['configuration'].iteritems():
                configuration[key] = str(value).encode('ascii','ignore')
            node = {
                'topology': topology,
                'topologyStats': data['topologyStats'],
                'spouts': data['spouts'],
                'bolts': data['bolts'],
                'configuration': configuration,
            }
    except (URLError, HTTPError) as e:
        node = {
            'error': str(e),
        }
    return HttpResponse(json.dumps(node), content_type='application/json')

def running_topologies():
    ids = []
    PROCESS_NAME = "java.exe"
    func = 'kanga.cep.storm.users.'
    try:
        for process in psutil.process_iter():
            if process.name() == PROCESS_NAME:
                cmdline = process.cmdline()
                if not 'Topology' in cmdline[-1]:
                    continue
                topology = cmdline[-1]
                if func in topology:
                    id = topology.replace(func,'')
                    ids.append(id)
    except Exception as e:
        print e
    return ids

def storm_topology_summary(request):
    node = {}
    pids = []
    PROCESS_NAME = "java.exe"
    try:
        cmd = "sudo pm2 jlist"
        pm_list = json.loads(subprocess.check_output(cmd, shell=True))
        # pprint.pprint(pids)
        for pid in pm_list:
            kill_url = reverse('monitor:api-kill-topology',args=[pid['name'].replace('KangaTopology','')])
            pids.append(
                {
                    'pid': pid['pid'],
                    'topology': pid['name'],
                    'cpu': pid['monit']['cpu'],
                    'memory': pid['monit']['memory'],
                    'restart_time': pid['pm2_env']['restart_time'],
                    'pm_uptime' : pid['pm2_env']['pm_uptime'],
                    'status' : pid['pm2_env']['status'],
                    'action': '<a href=\'javascript:kill_topology("'+kill_url+'")\'>kill</a>'
                }
            )
        node = {
            'data': pids
        }
        print pids
    except Exception as e:
        node = {
            'error': str(e),
        }
    return HttpResponse(json.dumps(node), content_type='application/json')

def storm_cluster_summary(request):
    node = {}
    try:
        timeout = 2
        hosts = get_storm_hosts()
        url = 'http://'+hosts[0]+'/api/v1/cluster/summary'
        data = json.loads(urlopen(Request(url), timeout=timeout).read())
        clusters = []
        clusters.append(
            {
                'slotsFree': data['slotsFree'],
                'slotsUsed': data['slotsUsed'],
                'slotsTotal': data['slotsTotal'],
                'executorsTotal': data['executorsTotal'],
                'tasksTotal': data['tasksTotal'],
                'supervisors': data['supervisors'],
                'nimbusUptime': data['nimbusUptime'],
            }
        )
        node = {
            'data': clusters
        }
    except (URLError, HTTPError) as e:
        node = {
            'error': str(e),
        }
    return HttpResponse(json.dumps(node), content_type='application/json')


def storm_supervisors_summary(request):
    node = {}
    try:
        timeout = 2
        hosts = get_storm_hosts()
        url = 'http://'+hosts[0]+'/api/v1/supervisor/summary'
        data = json.loads(urlopen(Request(url), timeout=timeout).read())
        supervisors = []
        for supervisor in data['supervisors']:
            supervisors.append(
                {
                    'slotsTotal': supervisor['slotsTotal'],
                    'slotsUsed': supervisor['slotsUsed'],
                    'uptime': supervisor['uptime'],
                    'host': supervisor['host'],
                    'id': supervisor['id'],
                }
            )
        node = {
            'data': supervisors
        }
    except (URLError, HTTPError) as e:
        node = {
            'error': str(e),
        }
    return HttpResponse(json.dumps(node), content_type='application/json')

def storm_nimbus_configuration(request):
    node = {}
    try:
        timeout = 2
        hosts = get_storm_hosts()
        url = 'http://'+hosts[0]+'/api/v1/cluster/configuration'
        data = json.loads(urlopen(Request(url), timeout=timeout).read())
        confs = []
        for key in data.keys():
            confs.append(
                {
                    'key': key,
                    'value': data[key],
                }
            )
        node = {
            'data': confs
        }
    except (URLError, HTTPError) as e:
        node = {
            'error': str(e),
        }
    return HttpResponse(json.dumps(node), content_type='application/json')

def find_actual_id(qid):
    id = None
    PROCESS_NAME = "java.exe"
    try:
        for process in psutil.process_iter():
            if process.name() == PROCESS_NAME:
                cmdline = process.cmdline()
                if cmdline[-1] == 'kanga.cep.storm.users.KangaTopology'+str(qid):
                    id = process.pid
                    break
    except Exception as e:
        print str(e)
    return id


def kill_topology(request,id):
    node = {}
    try:
        cmd = "pm2 id KangaTopology"+id
        pid = subprocess.check_output(cmd, shell=True)
        if len(pid) > 3:
            os.system("pm2 delete KangaTopology"+id)
            node = {
                        'data': 'Topology ['+id+'] is successfully killed.',
                    }
        else:
            node = {
                'error': 'Topology ['+id+'] is not killed since there is no such process',
            }
    except (URLError, HTTPError) as e:
        node = {
            'error': 'Topology ['+id+'] is not killed. '+str(e),
        }
    return HttpResponse(json.dumps(node), content_type='application/json')

def topology_stat(request,id):
    node = {}
    try:
        pattern = "KangaTopology[0-9]+\-[0-9\-]{1,28}"
        if re.match(pattern,id) is None:
            id = find_actual_id(id)
        if id is None:
            node = {
                'error': 'There is no matched running query in the realtime processing service',
            }
        else:
            timeout = 2
            hosts = get_storm_hosts()
            url = 'http://'+hosts[0]+'/api/v1/topology/'+id
            data = json.loads(urlopen(Request(url), timeout=timeout).read())
            io_perf = list()
            latency_perf = list()
            topology_perf = dict()
            topology_perf['uptime'] = data['uptime']
            print data['topologyStats'][0]['transferred']
            print data['topologyStats'][0]['window']
            if is_number(data['topologyStats'][0]['transferred']) and \
                is_number(data['topologyStats'][0]['emitted']) and \
                is_number(data['topologyStats'][0]['window']):
                topology_perf['transferred_eps'] = "{:10.1f}".format(float(data['topologyStats'][0]['transferred'])/float(data['topologyStats'][0]['window']))
                topology_perf['emitted_eps'] = "{:10.1f}".format(float(data['topologyStats'][0]['emitted'])/float(data['topologyStats'][0]['window']))
                topology_perf['transferred'] = "{:,}".format(data['topologyStats'][3]['transferred'])
                topology_perf['emitted'] = "{:,}".format(data['topologyStats'][3]['emitted'])
                topology_perf['acked'] = "{:,}".format(data['topologyStats'][3]['acked'])
                topology_perf['failed'] = "{:,}".format(data['topologyStats'][3]['failed'])
            else :
                topology_perf['transferred_eps'] = "0.0"
                topology_perf['emitted_eps'] = "0.0"
                topology_perf['transferred'] = "0"
                topology_perf['emitted'] = "0"
                topology_perf['acked'] = "0"
                topology_perf['failed'] = "0"
            for spout in data['spouts']:
                perf = dict()
                latency = dict()
                perf['emitted'] = spout['emitted']
                perf['transferred'] = spout['transferred']
                perf['acked'] = spout['acked']
                perf['id'] = spout['spoutId']
                latency['id'] = spout['spoutId']
                latency['latency'] = spout['completeLatency']
                io_perf.append(perf)
                latency_perf.append(latency)
            for bolt in data['bolts']:
                perf = dict()
                latency = dict()
                perf['emitted'] = bolt['emitted']
                perf['transferred'] = bolt['transferred']
                perf['acked'] = bolt['acked']
                perf['id'] = bolt['boltId']
                latency['id'] = bolt['boltId']
                latency['latency'] = bolt['processLatency']
                io_perf.append(perf)
                latency_perf.append(latency)
            node = {
                'io_perf': io_perf,
                'latency_perf': latency_perf,
                'topology_perf': topology_perf
            }
    except (URLError, HTTPError, Exception) as e:
        node = {
            'error': str(e),
        }
    return HttpResponse(json.dumps(node), content_type='application/json')

def is_number(s):
    if s is None:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False