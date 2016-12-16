import json
import sys
from Cheetah.Template import Template
templateDef="""\
var kangaBase = '../../../';
var events = require('events');
var clone = require(kangaBase + 'utils/common').clone;
var kangaLogger = require(kangaBase + 'utils/kanga.logger.js');
var kanga = new events.EventEmitter();
var node = {};
var log = new kangaLogger();

// Create the logger for the given topology
log.topologyLog("$nodeData.topology_name","info");
var klogger = log.getTopologyLog("$nodeData.topology_name")

// Load all the required bolts
#for $node in $nodeSet
	#set $name = $node[0].split('.')
var $name[-1] = require(kangaBase + "nodes/$node[1]/$node[0]")
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
node["$nodeInfo.blockId"] = new ${name[-1]}(${nodeInfo.blockId}_params)

#end for


// Define callback functions
#for $node in $nodeData.nodes
	#if $node.type == 'SOURCE'
		## Source nodes don't have an event input
var $node.blockId = function(){
	node["$node.blockId"].generateEvents(kanga.emit.bind(kanga,"$node.blockId"));
}
	#else
var $node.blockId = function(event){
	event = node["$node.blockId"].processData(clone(event));
	kanga.emit("$node.blockId",event);
}
	#end if
#end for

// Register the call back functions with kanga
#for $nodeInfo in $nodeData.nodes:
	#if $nodeInfo.type=="SOURCE"
kanga.on("start",$nodeInfo.blockId)
	#end if
#end for

#for $boltName in $nodeData.edges.ordered	
	#for $toBolt in $nodeData.edges.ordered[$boltName]
kanga.on("$boltName",$toBolt);
	#end for
#end for

kanga.emit("start");
klogger.info("Flow Started");
"""

if len(sys.argv) != 3:
	print("Invalid Number of arguments")
	print("Usage: "+sys.argv[0]+" "+"<json file> <output file>")
	exit()

output = open(sys.argv[2],mode='w')
jsonFile = open(sys.argv[1],mode='r')
jsonData = jsonFile.read()
nodeData = json.loads(jsonData)

# Create a set of required bolts
nodeSet = set()
for node in nodeData['nodes']:
	if node["type"]=="SOURCE":
		nodeSet.add((node['bolt_name'],"input"))
	elif node["type"]=="SINK":
		nodeSet.add((node['bolt_name'],"output"))
	else:
		nodeSet.add((node['bolt_name'],"function"))

nameSpace={'nodeData':nodeData,'nodeSet':nodeSet}
t=Template(templateDef,searchList=[nameSpace])
output.write(str(t))