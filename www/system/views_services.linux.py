from django.http import HttpResponse
from urllib2 import urlopen, Request, URLError, HTTPError
import json
import subprocess
from time import gmtime, strftime


def get_services_status(request):
    services = list()
    try:
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
    node = {'data':services}
    return HttpResponse(json.dumps(node), content_type="application/json")


def command_supervisor(request,hostname,processname,action):
    try:
        timeout = 2
        url = 'http://'+hostname+':9001/index.html?processname='+processname+'&action='+action
        response = urlopen(Request(url), timeout=timeout)
        html = response.read()
    except (URLError, HTTPError) as e:
        print e