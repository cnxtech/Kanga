
var kangaBase = '../lib/base';
var events = require('events');
var clone = require(kangaBase + '/utils/kanga-common').clone;
var kangaLogger = require(kangaBase + '/utils/kanga-logger');
var kangaEmitter = new events.EventEmitter();
var node = {};

// Create the logger for the given topology
var klogger = new kangaLogger("KangaTopology20", 'debug');


// Load all the required bolts
var cpu_info = require(kangaBase + "/nodes/spout/cpu-info")
var to_socket_io = require(kangaBase + "/nodes/sink/to-socket-io")

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



// Define callback functions
var flowchart_cpu_info_913 = function(){
	node["flowchart_cpu_info_913"].generateEvents(kangaEmitter.emit.bind(kangaEmitter,"flowchart_cpu_info_913"), true);
}
var flowchart_to_socket_io_472 = function(event, isClone){
	event = node["flowchart_to_socket_io_472"].execute((isClone == true) ? clone(event) : event);
	kangaEmit("flowchart_to_socket_io_472",event, true);
}

// Register the call back functions with kangaEmitter
kangaEmitter.on("start",flowchart_cpu_info_913)

kangaEmitter.on("flowchart_cpu_info_913",flowchart_to_socket_io_472);

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


