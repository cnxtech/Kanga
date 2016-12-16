
var kangaBase = '../lib/base';
var events = require('events');
var clone = require(kangaBase + '/utils/kanga-common').clone;
var kangaLogger = require(kangaBase + '/utils/kanga-logger');
var kangaEmitter = new events.EventEmitter();
var node = {};

// Create the logger for the given topology
var klogger = new kangaLogger("KangaTopology19", 'debug');


// Load all the required bolts
var resource_info = require(kangaBase + "/nodes/spout/resource-info")
var reformat = require(kangaBase + "/nodes/oneM2M/reformat")
var to_socket_io = require(kangaBase + "/nodes/sink/to-socket-io")

// Create an object with the required set of parameters
var flowchart_cpu_mem_info_590_params = {}
flowchart_cpu_mem_info_590_params.klogger = klogger
flowchart_cpu_mem_info_590_params.sleeping_time = "1000"
node["flowchart_cpu_mem_info_590"] = new resource_info(flowchart_cpu_mem_info_590_params)

var flowchart_reformat_13_params = {}
flowchart_reformat_13_params.klogger = klogger
flowchart_reformat_13_params.key_field_name = "ctname"
flowchart_reformat_13_params.value_field_name = "con"
flowchart_reformat_13_params.locale = "ko-kr"
node["flowchart_reformat_13"] = new reformat(flowchart_reformat_13_params)

var flowchart_to_socket_io_971_params = {}
flowchart_to_socket_io_971_params.klogger = klogger
flowchart_to_socket_io_971_params.host = "10.251.20.120:3000"
flowchart_to_socket_io_971_params.topicname = "oneM2M"
node["flowchart_to_socket_io_971"] = new to_socket_io(flowchart_to_socket_io_971_params)



// Define callback functions
var flowchart_cpu_mem_info_590 = function(){
	node["flowchart_cpu_mem_info_590"].generateEvents(kangaEmitter.emit.bind(kangaEmitter,"flowchart_cpu_mem_info_590"), true);
}
var flowchart_reformat_13 = function(event, isClone){
	event = node["flowchart_reformat_13"].execute((isClone == true) ? clone(event) : event);
	kangaEmit("flowchart_reformat_13",event, true);
}
var flowchart_to_socket_io_971 = function(event, isClone){
	event = node["flowchart_to_socket_io_971"].execute((isClone == true) ? clone(event) : event);
	kangaEmit("flowchart_to_socket_io_971",event, true);
}

// Register the call back functions with kangaEmitter
kangaEmitter.on("start",flowchart_cpu_mem_info_590)

kangaEmitter.on("flowchart_reformat_13",flowchart_to_socket_io_971);
kangaEmitter.on("flowchart_cpu_mem_info_590",flowchart_reformat_13);

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


