from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from knowledge.models import RealtimeQuery
import urllib
import urllib2
from multiprocessing import Process,Queue
import os
import json
import yaml
import translator
import base64
from workspace.builder import builder
from random import randint
import django

class NodeDetection:
    def __init__(self):
        self.allMacroNode = list()

def traverseAllMacroNode(obj,macroId):
    user_query = RealtimeQuery.objects.get(pk=macroId)
    query = yaml.safe_load(user_query.query)
    for node in query['nodes']:
        if 'macro' in node['nodetype']:
            argData = yaml.safe_load(base64.b64decode(node['argData']))
            macroId = argData[0]['value'].split("_")[0]
            obj.allMacroNode.append(macroId)
            traverseAllMacroNode(obj, macroId)

def detectAllMacro(obj,query):
    # 1. detect and list duplicated macro node
    for node in query['nodes']:
        if 'macro' in node['nodetype']:
            argData = yaml.safe_load(base64.b64decode(node['argData']))
            macroId = argData[0]['value'].split("_")[0]
            obj.allMacroNode.append(macroId)
            traverseAllMacroNode(obj,macroId)

def expose_all_macro(rawQuery):
    tempMacroBlockId = ''
    tempMacroConnection = list()
    tempNode = list()
    tempConnect = list()
    #1. find Macro keyword in nodes and break
    for node in rawQuery['nodes']:
        if 'macro' in node['nodetype']:
            tempMacroBlockId = node['blockId']
            argData = yaml.safe_load(base64.b64decode(node['argData']))
            tempMacroId = argData[0]['value'].split("_")[0]
            break

    #2. find all connection to that macro
    for connection in rawQuery['connections']:
        if connection['pageSourceId'] == tempMacroBlockId or connection['pageTargetId'] == tempMacroBlockId:
            tempMacroConnection.append(connection)

    #3. pull all macro detail from database
    data = RealtimeQuery.objects.get(pk=tempMacroId)
    data_query = yaml.safe_load(data.query)

    # 1. Try to expose macro node detail to node list
    for node in data_query['nodes']:
        # if macro doesn't have output or input, expose its connection to tempConnection
        if 'flowchart_dummy_input' not in node['blockId'] and 'flowchart_dummy_output' not in node['blockId']:
            if node not in tempNode:
                tempNode.append(node)

    # 2. Expose macro connection detail to tempConnection list
    for connection in data_query['connections']:
        if connection not in tempConnect:
            tempConnect.append(connection)

    #3. reconnect the macro to detail
    for connection in tempMacroConnection:
        if connection['pageSourceId'] == tempMacroBlockId:
            for con in tempConnect:
                if 'flowchart_dummy_output' in con['pageTargetId']:
                    tempConnect.append({'pageSourceId': con['pageSourceId'],'pageTargetId': connection['pageTargetId']})
        elif connection['pageTargetId'] == tempMacroBlockId:
            for con in tempConnect:
                if 'flowchart_dummy_input' in con['pageSourceId']:
                    tempConnect.append({'pageSourceId': connection['pageSourceId'], 'pageTargetId': con['pageTargetId']})

    tempConnection = list(tempConnect)
    for con in tempConnection:
        if 'flowchart_dummy_output' in con['pageTargetId'] or 'flowchart_dummy_input' in con['pageSourceId']:
            tempConnect.remove(con)
    del tempConnection[:]

    #5. Give new Id for every element
    for idx,node in enumerate(tempNode):
        old = node['blockId']
        new = 'flowchart_' + node['nodetype'] + '_' + str(randint(0, 999))
        tempNode[idx]['blockId'] = new
        for idx,connection in enumerate(tempConnect):
            if connection['pageSourceId'] == old:
                tempConnect[idx]['pageSourceId'] = new
            if connection['pageTargetId'] == old:
                tempConnect[idx]['pageTargetId'] = new

    #6. push every new element to the new exposed query
    conn = list(rawQuery['connections'])
    node = list(rawQuery['nodes'])

    for a in rawQuery['connections']:
        if a['pageSourceId'] == tempMacroBlockId or a['pageTargetId'] == tempMacroBlockId:
            conn.remove(a)
    for a in rawQuery['nodes']:
        if a['blockId'] == tempMacroBlockId:
            node.remove(a)

    conn.extend(tempConnect)
    node.extend(tempNode)
    finalQuery = {'connections': conn, 'nodes': node}

    return finalQuery

def get_kafka_info_in_macro(request):
    if request.method == 'POST':
        obj = NodeDetection()
        query = request.POST['query']
        loopQuery = yaml.safe_load(query)
        detectAllMacro(obj,loopQuery)
        counter = 0
        while counter < len(obj.allMacroNode):
            loopQuery = expose_all_macro(loopQuery)
            counter += 1
        return HttpResponse(json.dumps(loopQuery))

def realtimequery_validate(request,realtimequery_id):
    obj = NodeDetection()
    user_query = ''
    query = ''
    err_msg = ''
    success_msg = ''
    compiled = True
    stdout = ''
    node_code = ''
    node = {}
    try:
        user_query = RealtimeQuery.objects.get(pk=realtimequery_id)
        loopQuery = yaml.safe_load(user_query.query)
        detectAllMacro(obj, loopQuery)
        counter = 0
        while counter < len(obj.allMacroNode):
            loopQuery = expose_all_macro(loopQuery)
            counter += 1
        query = translator.decode64(loopQuery)
        translator.attach_edges(query)
        translator.attach_template(query)
        translator.validate_graph(query)
        topology_name = "KangaTopology"+str(realtimequery_id)
        query['topology_name'] = topology_name
        #paths = builder.get_paths(realtimequery_id)
        #json_code = paths['TMP_FILE_DIR']+'\\'+topology_name+'.json'
        #json_code = json_code.replace('\\','/')
        node_code = translator.to_node_code(query,topology_name)
        translator.write_code(topology_name+'.js',node_code)
        #translator.write_code(topology_name+'.json',json.dumps(query,indent=4))
        success_msg = 'Kanga generates a cep code successfully'
    except Exception as e:
        err_msg = str(e)
        compiled = False
    try:
        node = {
            "user_query": json.dumps(loopQuery),
            "intermediate_query": query,
            "stdout" : stdout,
            "result": compiled,
            "error_message": err_msg,
            "success_message": success_msg,
            "node_code": node_code,
        }
    except Exception as e:
        node = {
            "error_message": err_msg + "\n\n" + str(e),
            "result": False,
        }
    return HttpResponse(json.dumps(node,sort_keys=True,indent=4), content_type='application/json')


def api_remote_launch(ip,query_id,code):
    msg = ''
    status = ''
    result = {}
    url = 'http://'+ip +':8888/topology'
    data = {
        'id': query_id,
        'code': code
    }
    try:
        req = urllib2.Request(url, urllib.urlencode(data))
        # req.get_method = lambda : "DELETE"
        res = urllib2.urlopen(req,timeout=30)
        status = res.result
        if res.result =='success':
            msg = ip + ': ' + query_id + ' submitted successfully...\n' +'topology is launched successfully.'
        elif res.result =='running':
            msg = ip + ': ' + query_id + ' is already running.'
        else:
            msg = ip + ': ' + query_id +  ' submission failed.'
    except Exception as e:
        msg = ip + ': ' + query_id +  ' submission failed.\n' + str(e)
        status = 'failed'
    result = {
        "status": status,
        "message": msg,
    }
    return result


def realtimequery_remote_launch(request, realtimequery_id):
    print "realtimequery_remote_launch ....................."
    err_msg = ''
    success_msg = ''
    stdout = ''
    launched = True
    res = {}
    launch_result= []
    try:
        node_code = request.POST.get('code', '')
        ip_arr = []
        ip_arr= request.POST.getlist('ipList[]', '')
        if node_code == '':
            raise Exception("Can not execute empty Code.")
        topology_name = 'KangaTopology'+str(realtimequery_id)
        proc = []

        for ip in ip_arr:
            stdout = api_remote_launch(ip, topology_name, node_code)
            if stdout['status'] !='success':
                launch_result.append(stdout['message'])
                err_msg = 'Error occurs in some machines during launches the topology'
            else:
                success_msg = 'Kanga successfully launches the topology into selected machines.'
        #     p = Process(target=api_remote_launch, args=(ip,topology_name,node_code))
        #     proc.append(p)
        #     p.start()
        # for p in proc:
        #     p.join()
    except Exception as e:
        err_msg = str(e)
        launched = False

    res = {
        "stdout" : launch_result,
        "result": launched,
        "error_message": err_msg,
        "success_message": success_msg,
    }
    return HttpResponse(json.dumps(res, sort_keys=True, indent=4), content_type='application/json')

def realtimequery_launch(request,realtimequery_id):
    print "realtimequery_launch ....................."
    err_msg = ''
    success_msg = ''
    stdout = ''
    launched = True
    node = {}
    try:
        topology_name = 'KangaTopology'+str(realtimequery_id)
        topology_src_file = topology_name+'.js'
        rtq = get_object_or_404(RealtimeQuery, pk=realtimequery_id)
        paths = dict()
        topology_src_file = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "builder", "tmp", topology_src_file
            )
        )
        # builder.clean(paths,10)
        stdout = builder.submit_topology(topology_name, topology_src_file)+'\n\n'
        success_msg = 'Kanga successfully launches the topology into cep engine'
    except Exception as e:
        err_msg = str(e)
        compiled = False
    try:
        node = {
            "stdout" : stdout,
            "result": launched,
            "error_message": err_msg,
            "success_message": success_msg,
        }
    except Exception as e:
        node = {
            "error_message": err_msg + "\n\n" + str(e),
            "result": False,
        }
    return HttpResponse(json.dumps(node,sort_keys=True,indent=4), content_type='application/json')