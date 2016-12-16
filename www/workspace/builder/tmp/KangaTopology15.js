
var kangaBase = '../lib/base';
var events = require('events');
var clone = require(kangaBase + '/utils/kanga-common').clone;
var kangaLogger = require(kangaBase + '/utils/kanga-logger');
var kangaEmitter = new events.EventEmitter();
var node = {};

// Create the logger for the given topology
var klogger = new kangaLogger("KangaTopology15", 'debug');


// Load all the required bolts
var file_reader = require(kangaBase + "/nodes/spout/file-reader")
var save_to_file = require(kangaBase + "/nodes/sink/save-to-file")
var add_field = require(kangaBase + "/nodes/transform/add-field")

// Create an object with the required set of parameters
var flowchart_from_file_585_params = {}
flowchart_from_file_585_params.klogger = klogger
flowchart_from_file_585_params.output_name = "test"
flowchart_from_file_585_params.file_path = "C:\kanga\sw\test.txt"
flowchart_from_file_585_params.sleeping_time = "100"
node["flowchart_from_file_585"] = new file_reader(flowchart_from_file_585_params)

var flowchart_to_file_539_params = {}
flowchart_to_file_539_params.klogger = klogger
flowchart_to_file_539_params.output_file_path = "C:\kanga\sw\output_test.txt"
node["flowchart_to_file_539"] = new save_to_file(flowchart_to_file_539_params)

var flowchart_add_field_76_params = {}
flowchart_add_field_76_params.klogger = klogger
flowchart_add_field_76_params.input_field_name = "test"
flowchart_add_field_76_params.value = "xxxx"
flowchart_add_field_76_params.output_name = "test2"
node["flowchart_add_field_76"] = new add_field(flowchart_add_field_76_params)



// Define callback functions
var flowchart_from_file_585 = function(){
	node["flowchart_from_file_585"].generateEvents(kangaEmitter.emit.bind(kangaEmitter,"flowchart_from_file_585"), true);
}
var flowchart_to_file_539 = function(event, isClone){
	event = node["flowchart_to_file_539"].execute((isClone == true) ? clone(event) : event);
	kangaEmit("flowchart_to_file_539",event, true);
}
var flowchart_add_field_76 = function(event, isClone){
	event = node["flowchart_add_field_76"].execute((isClone == true) ? clone(event) : event);
	kangaEmit("flowchart_add_field_76",event, true);
}

// Register the call back functions with kangaEmitter
kangaEmitter.on("start",flowchart_from_file_585)

kangaEmitter.on("flowchart_add_field_76",flowchart_to_file_539);
kangaEmitter.on("flowchart_from_file_585",flowchart_add_field_76);

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


