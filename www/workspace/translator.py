import networkx as nx
import yaml
import base64
import os
from Cheetah.Template import Template
from help.models import Command
from kanga import settings
from jsmin import jsmin
import pprint


def attach_edges(query):
    edges = dict()
    edges['ordered'] = dict()
    edges['reverse'] = dict()
    edges['list'] = list()
    for connection in query['connections']:
        if connection['pageSourceId'] in edges['ordered'].keys():
            edges['ordered'][connection['pageSourceId']].append(connection['pageTargetId'])
        else:
            edges['ordered'][connection['pageSourceId']] = [connection['pageTargetId']]
        if connection['pageTargetId'] in edges['reverse'].keys():
            edges['reverse'][connection['pageTargetId']].append(connection['pageSourceId'])
        else:
            edges['reverse'][connection['pageTargetId']] = [connection['pageSourceId']]
        edge = (connection['pageSourceId'],connection['pageTargetId'])
        edges['list'].append(edge)
    query['edges'] = edges

def validate_graph(query):
    edges = query['edges']['list']
    G = nx.DiGraph(edges)
    if not nx.is_weakly_connected(G):
        raise Exception('Your query is not connected fully. Please check if any required link is not connected')
    if not nx.is_directed_acyclic_graph(G):
        raise Exception('Directed acyclic graph is only accepted. Please check if your graph is cyclic. Typically graph needs to have one (or many) source and one (or many) sink')
    is_node_type_violated(query)

def decode64(query):
    for node in query['nodes']:
        if not 'argData' in node:
            raise Exception('Please insert argument in '+node['blockId'])
        node['argData'] = yaml.safe_load(base64.b64decode(node['argData']))
    return query

def find_shuffle_groups(query, child_node_name):
    shuffle_groups = ''
    if child_node_name in query['edges']['reverse'].keys():
        for sg in query['edges']['reverse'][child_node_name]:
            shuffle_groups+='.shuffleGrouping("'+sg+'")'
    return shuffle_groups

def is_node_type_violated(query):
    for node in query['nodes']:
        if node['type']=="SOURCE":
            if node['blockId'] in query['edges']['reverse']:
                raise Exception(node['blockId']+'is SOURCE type which should not have any parent node')
            if not node['blockId'] in query['edges']['ordered']:
                raise Exception(node['blockId']+' is SOURCE type which should have at least any child node')
        if node['type']=="SINK":
            if not node['blockId'] in query['edges']['reverse']:
                raise Exception(node['blockId']+'is SINK type which should have at least any parent node')
            if node['blockId'] in query['edges']['ordered']:
                raise Exception(node['blockId']+' is SINK type which should be a final node with no child node')
        if node['type']=="NORMAL":
            if not node['blockId'] in query['edges']['reverse']:
                raise Exception(node['blockId']+'is NORMAL type which should have at least any parent node')
            if not node['blockId'] in query['edges']['ordered']:
                raise Exception(node['blockId']+' is NORMAL type which should have at least any child node')
        if node['type']=="JOIN":
            if not node['blockId'] in query['edges']['reverse'] or query['edges']['reverse'][node['blockId']].__len__ < 2 :
                raise Exception(node['blockId']+' is JOIN type which should have at least more than 2 parent nodes')
            if not node['blockId'] in query['edges']['ordered']:
                raise Exception(node['blockId']+' is JOIN type which should have at least any child node')


def attach_template(query):
    for node in query['nodes']:
        snippet = Command.objects.values_list('node_type','bolt_name').filter(command=node['nodetype'])
        node['type'] = snippet[0][0]
        node['bolt_name'] = snippet[0][1]

def to_node_code(nodeData, topology_name):
    kanga_base = os.path.join(settings.BASE_DIR, 'workspace','builder','lib','base').replace('\\','/')
    kanga_base = '../lib/base'

    template = """
var kangaBase = '$kanga_base';
var events = require('events');
var clone = require(kangaBase + '/utils/kanga-common').clone;
var kangaLogger = require(kangaBase + '/utils/kanga-logger');
var kangaEmitter = new events.EventEmitter();
var node = {};

// Create the logger for the given topology
var klogger = new kangaLogger("$topology_name", 'debug');


// Load all the required bolts
#for $node in $nodeData.nodes
	#set $name = $node.bolt_name.split('.')
    #set $var_name = $name[1].replace('-','_')
var $var_name = require(kangaBase + "/nodes/$name[0]/$name[1]")
#end for

// Create an object with the required set of parameters
#for $nodeInfo in $nodeData.nodes
	#set $argData = $nodeInfo.argData
var ${nodeInfo.blockId}_params = {}
${nodeInfo.blockId}_params.klogger = klogger
	#for $arg in argData
${nodeInfo.blockId}_params.$arg.name = "$arg.value"
	#end for
#set name = $nodeInfo.bolt_name.split(".")
#set $var_name = $name[1].replace('-','_')
node["$nodeInfo.blockId"] = new ${var_name}(${nodeInfo.blockId}_params)

#end for


// Define callback functions
#for $node in $nodeData.nodes
	#if $node.type == 'SOURCE'
		## Source nodes don't have an event input
var $node.blockId = function(){
	node["$node.blockId"].generateEvents(kangaEmitter.emit.bind(kangaEmitter,"$node.blockId"), true);
}
	#else
var $node.blockId = function(event, isClone){
	event = node["$node.blockId"].execute((isClone == true) ? clone(event) : event);
	kangaEmit("$node.blockId",event, true);
}
	#end if
#end for

// Register the call back functions with kangaEmitter
#for $nodeInfo in $nodeData.nodes:
	#if $nodeInfo.type=="SOURCE"
kangaEmitter.on("start",$nodeInfo.blockId)
	#end if
#end for

#for $boltName in $nodeData.edges.ordered
	#for $toBolt in $nodeData.edges.ordered[$boltName]
kangaEmitter.on("$boltName",$toBolt);
	#end for
#end for

kangaEmitter.emit("start");
klogger.info("Flow Started");

function kangaEmit(eId, event, isClone) {
    if (event != null) {
        if (event.constructor == Array) {
            for (var i = 0; i < event.length; i++) {
                kangaEmitter.emit(eId, event[i], isClone);
            }
        } else {
            kangaEmitter.emit(eId, event, isClone);
        }
    }
}

"""
    nameSpace={
        'nodeData':nodeData,
        'topology_name': topology_name,
        'kanga_base': kanga_base
    }
    code = Template(template,searchList=[nameSpace])
    return str(code)


def to_node_code_old(json_code,query):
    pprint.pprint(query)
    template = """

var kangaFlow = require('$flow_parse');

var flow = new kangaFlow('$json_code');
flow.activateFlows();

"""
    flow_parse = 'C:/Users/User/workspace/Kanga_Nodejs_160617/kanga/runtime/kangaFlowParse'
    name_space = {'json_code': json_code,
                 'flow_parse': flow_parse}
    code = Template(template, searchList=[name_space])
    return str(code)


def write_code(filename,code):
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


