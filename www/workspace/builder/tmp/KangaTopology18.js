
var kangaBase = '../lib/base';
var events = require('events');
var clone = require(kangaBase + '/utils/kanga-common').clone;
var kangaLogger = require(kangaBase + '/utils/kanga-logger');
var kangaEmitter = new events.EventEmitter();
var node = {};

// Create the logger for the given topology
var klogger = new kangaLogger("KangaTopology18", 'debug');


// Load all the required bolts
var file_reader = require(kangaBase + "/nodes/spout/file-reader")
var save_to_file = require(kangaBase + "/nodes/sink/save-to-file")

// Create an object with the required set of parameters
var flowchart_from_file_958_params = {}
flowchart_from_file_958_params.klogger = klogger
flowchart_from_file_958_params.output_name = "test"
flowchart_from_file_958_params.file_path = "../workspace/input_single_line.json"
flowchart_from_file_958_params.sleeping_time = "100"
node["flowchart_from_file_958"] = new file_reader(flowchart_from_file_958_params)

var flowchart_to_file_379_params = {}
flowchart_to_file_379_params.klogger = klogger
flowchart_to_file_379_params.output_file_path = "../workspace/output_single_line.json"
node["flowchart_to_file_379"] = new save_to_file(flowchart_to_file_379_params)



// Define callback functions
var flowchart_from_file_958 = function(){
	node["flowchart_from_file_958"].generateEvents(kangaEmitter.emit.bind(kangaEmitter,"flowchart_from_file_958"), true);
}
var flowchart_to_file_379 = function(event, isClone){
	event = node["flowchart_to_file_379"].execute((isClone == true) ? clone(event) : event);
	kangaEmit("flowchart_to_file_379",event, true);
}

// Register the call back functions with kangaEmitter
kangaEmitter.on("start",flowchart_from_file_958)

kangaEmitter.on("flowchart_from_file_958",flowchart_to_file_379);

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


