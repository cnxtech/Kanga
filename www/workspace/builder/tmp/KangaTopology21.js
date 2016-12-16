
var kangaBase = '../lib/base';
var events = require('events');
var clone = require(kangaBase + '/utils/kanga-common').clone;
var kangaLogger = require(kangaBase + '/utils/kanga-logger');
var kangaEmitter = new events.EventEmitter();
var node = {};

// Create the logger for the given topology
var klogger = new kangaLogger("KangaTopology21", 'debug');


// Load all the required bolts
var cpu_info = require(kangaBase + "/nodes/spout/cpu-info")
var to_socket_io = require(kangaBase + "/nodes/sink/to-socket-io")
var tcp_server = require(kangaBase + "/nodes/spout/tcp-server")
var reformat = require(kangaBase + "/nodes/oneM2M/reformat")

// Create an object with the required set of parameters
var flowchart_cpu_info_913_params = {}
flowchart_cpu_info_913_params.klogger = klogger
flowchart_cpu_info_913_params.sleeping_time = "1000"
node["flowchart_cpu_info_913"] = new cpu_info(flowchart_cpu_info_913_params)

var flowchart_to_socket_io_472_params = {}
flowchart_to_socket_io_472_params.klogger = klogger
flowchart_to_socket_io_472_params.host = "10.240.245.124:3000"
flowchart_to_socket_io_472_params.topicname = "oneM2M"
node["flowchart_to_socket_io_472"] = new to_socket_io(flowchart_to_socket_io_472_params)

var flowchart_from_tcp_server_817_params = {}
flowchart_from_tcp_server_817_params.klogger = klogger
flowchart_from_tcp_server_817_params.output_name = "tcp"
flowchart_from_tcp_server_817_params.port = "7622"
node["flowchart_from_tcp_server_817"] = new tcp_server(flowchart_from_tcp_server_817_params)

var flowchart_reformat_706_params = {}
flowchart_reformat_706_params.klogger = klogger
flowchart_reformat_706_params.key_field_name = "ctname"
flowchart_reformat_706_params.value_field_name = "con"
flowchart_reformat_706_params.locale = "ko-kr"
node["flowchart_reformat_706"] = new reformat(flowchart_reformat_706_params)



// Define callback functions
var flowchart_cpu_info_913 = function(){
	node["flowchart_cpu_info_913"].generateEvents(kangaEmitter.emit.bind(kangaEmitter,"flowchart_cpu_info_913"), true);
}
var flowchart_to_socket_io_472 = function(event, isClone){
	event = node["flowchart_to_socket_io_472"].execute((isClone == true) ? clone(event) : event);
	kangaEmit("flowchart_to_socket_io_472",event, true);
}
var flowchart_from_tcp_server_817 = function(){
	node["flowchart_from_tcp_server_817"].generateEvents(kangaEmitter.emit.bind(kangaEmitter,"flowchart_from_tcp_server_817"), true);
}
var flowchart_reformat_706 = function(event, isClone){
	event = node["flowchart_reformat_706"].execute((isClone == true) ? clone(event) : event);
	kangaEmit("flowchart_reformat_706",event, true);
}

// Register the call back functions with kangaEmitter
kangaEmitter.on("start",flowchart_cpu_info_913)
kangaEmitter.on("start",flowchart_from_tcp_server_817)

kangaEmitter.on("flowchart_reformat_706",flowchart_to_socket_io_472);
kangaEmitter.on("flowchart_cpu_info_913",flowchart_to_socket_io_472);
kangaEmitter.on("flowchart_from_tcp_server_817",flowchart_reformat_706);

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


