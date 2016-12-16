import json
import os
import subprocess
import tempfile
import shutil
import urllib2
import time
import re
from datetime import datetime

from django.http import HttpResponse

from kanga import settings
from monitor.views_services import running_topologies


def is_topology_active(topology_name,host='localhost:8080'):
    RETRY_INTERVAL = 0.1  # seconds
    STORM_SUMMARY_URL = 'http://'+host+'/api/v1/topology/summary'
    result = False
    retry_counter = 5
    try:
        while retry_counter > 0:
            retry_counter -= 1
            urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler({})))
            json_resp = urllib2.urlopen(STORM_SUMMARY_URL).read()
            index = json_resp.find(topology_name)
            index = json_resp.find('ACTIVE', index, json_resp.find('}', index))
            if index == -1:
                # New topology may not be registered yet. Wait for some time...
                time.sleep(RETRY_INTERVAL)
            else:
                result = True
                break
    except Exception as e:
        raise Exception('Error occurs when system checks topology health: '+str(e))
    return result


def is_nimbus_active():
    # Check if Nimbus is running
    result = command('jps')
    # TODO --- by storm ui restful
    # if not 'nimbus' in result:
    #     raise Exception('ERROR: Nimbus is not running.')


def command(command, env=None):
    stdout = ''
    try:
        proc = subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        stdout = out + err
    except subprocess.CalledProcessError as e:
        raise Exception ('ERROR: Exception running command : ' + command + "\nException : " + str(e))
    except UnicodeError as e:
        raise Exception ('ERROR: Exception running command : ' + command + "\nException : " + str(e))
    return stdout

def bg_command(command, env=None):
    stdout = ''
    try:
        proc = subprocess.Popen(command, env=env, shell=True)
        stdout = 'topology is launched successfully' # it should be modified later ... SEAN..
    except subprocess.CalledProcessError as e:
        raise Exception ('ERROR: Exception running command : ' + command + "\nException : " + str(e))
    except UnicodeError as e:
        raise Exception ('ERROR: Exception running command : ' + command + "\nException : " + str(e))
    return stdout


def get_paths(realtimequery_id):
    paths = dict()
    paths['TMP_FILE_DIR'] = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "tmp"
        )
    )
    paths['ANT_BUILD_FILE'] = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "tmp/build.xml"
        )
    )
    paths['LIB_PATH'] = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 'lib'
        )
    )
    paths['LIB_PROVIDED_PATH'] = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 'provided'
        )
    )
    tmp_file_prefix = 'topology'+realtimequery_id+'_'+time.strftime('%Y%m%d_%H%M%S')+'_'
    paths['TOPOLOGY_TMP_DIR'] = tempfile.mkdtemp(prefix=tmp_file_prefix, dir=paths['TMP_FILE_DIR'])
    paths['JAR_FILE_DEST_PATH'] = '.'
    return paths


def run_ant(topology_name, topology_src_file, paths):
    stdout = ''
    # temp workspace dir
    DBG = 'true'
    # Copy ant build file and topology src files to tmp dir
    shutil.copy(paths['ANT_BUILD_FILE'], paths['TOPOLOGY_TMP_DIR'])
    src_file = os.path.join(paths['TMP_FILE_DIR'],topology_src_file)
    shutil.move(src_file, paths['TOPOLOGY_TMP_DIR'])
    # Set environment variables
    env = dict(
        os.environ,
        KANGA_LIB_PATH=paths['LIB_PATH'],
        KANGA_LIB_PROVIDED_PATH=paths['LIB_PROVIDED_PATH'],
        KANGA_JAR_FILE_NAME=topology_name,
        KANGA_JAR_FILE_DEST_PATH=paths['JAR_FILE_DEST_PATH'],
        DEBUG=DBG
    )
    # Make call for ant build
    # ant main -buildfile <path_to_build_xml>

    # ant_cmd = '/cepdev/apache-ant-1.9.6/bin/ant'
    ant_cmd = 'ant'
    cmd = ant_cmd+' main -buildfile ' + os.path.abspath(
        os.path.join(
            paths['TOPOLOGY_TMP_DIR'], "build.xml"
        )
    )
    stdout = command(cmd, env)
    print stdout
    # Check if the build was successful
    if 'BUILD SUCCESSFUL' in stdout:
        stdout = 'Build passed with logs : \n' + stdout
    else:
        raise Exception('ERROR: Build failed with logs : \n'+stdout)
    return stdout


def submit_topology(topology_name,topology_src_file):
    print "submit_topology ....................."
    topologies = running_topologies()
    if topology_name in topologies:
        raise Exception('ERROR: Topology submission failed.\nTopology is already running')
    stdout = ''
    # cmd = 'start /MIN node '+topology_src_file
    cmd = 'sudo pm2 start '+topology_src_file
    print cmd
    stdout = bg_command(cmd)
    if 'Exception in thread' in stdout:
        raise Exception('ERROR: Topology submission failed.\n'+stdout)
    else:
        return 'Topology ' + topology_name + ' submitted successfully...\n' + stdout


def write_launch_command(filename,code):
    filename = os.path.join(
                os.path.dirname(__file__), 'builder/tmp/'+filename
               )
    try:
        with open(filename, 'w+') as f:
            for line in code.split('\n'):
                f.write(line.rstrip()+'\n')
            f.close()
        # print (code, file=filename)
    except Exception as e:
        raise Exception('file write failed. detailed error is '+str(e))



def clean(paths,last_seconds=3600):
    TMP_FILE_DIR = paths['TMP_FILE_DIR']
    onlydirs = [ f for f in os.listdir(TMP_FILE_DIR) if os.path.isdir(os.path.join(TMP_FILE_DIR,f)) ]
    last_seconds=time.time()-last_seconds
    last_seconds = datetime.fromtimestamp(last_seconds)
    print 'Housekeeper will delete previous tmp topologies built before '+str(last_seconds)
    for mydir in onlydirs:
        try:
            m = re.search('_([0-9]+\_[0-9]+)',mydir)
            if datetime.strptime(m.group(1),'%Y%m%d_%H%M%S') < last_seconds:
                targetdir = os.path.join(TMP_FILE_DIR,mydir)
                print targetdir+' is deleted'
                shutil.rmtree(targetdir)
        except Exception as e:
            print e
    print 'Housekeeper job done --------------'



def submit_topology_from_deployment_server_call(request):
    topology = request.POST.get('topology',request.GET.get('topology',''))
    try:
        if topology == '':
            node = {
                'status': 'failed',
                'message': 'Requested topology name is empty'
            }
        else:
            cmd_file = os.path.normpath(os.path.join(settings.BASE_DIR,'workspace/builder/topologies/')+topology+'.cmd')
            print cmd_file
            topologies = running_topologies()
            if topology in topologies:
                node = {
                    'status': 'failed',
                    'message': 'Topology is already running'
                }
            else:
                stdout = bg_command('start /MIN '+cmd_file)
                if 'Exception in thread' in stdout:
                    node = {
                        'status': 'failed',
                        'message': 'Topology is already running'
                    }
                else:
                    node = {
                        'status': 'success',
                        'message': 'Topology ' + topology + ' submitted successfully...\n' + stdout
                    }
    except Exception as e:
        node = {
            'status': 'failed',
            'message': str(e)
        }
    return HttpResponse(json.dumps(node), content_type='application/json')
