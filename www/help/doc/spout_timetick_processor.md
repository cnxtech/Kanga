Time Tick Processor
----------------------

This processor is a Node.js bolt that generate time tick event.

* __Category:__ spout
* __Class:__ spout.time-tick
* __Version:__ 0.2

### API

* __time size__
    * __variable type:__ int
    * __possible values (examples):__ 10
    * __limitation:__ It should be greater than 0
    * __mandatory field__
    
* __bucket unit__
    * __variable type:__ enum
    * __possible values (examples):__ TICK, SECOND
    * __limitation:__ Either of TICK, SECOND
    * __mandatory field__

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ utility_meter (output stream name to be emitted)
    * __mandatory field__


### Feature

* __Run-time evaluation (ScriptEngine):__ No
* __Batch window (Bucket):__ No
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ No
* __Group by:__ No
* __Output event type:__ Data 


### Examples

#### Example 1

##### incoming events
* at T1, "person":{"name":"Mark", "age":25, "empid":1001}
* at T2, "person":{"name":"John", "age":32, "empid":1002}
* at T3, "person":{"name":"Greg", "age":27, "empid":1003}

##### argument
* __bucket size:__ 3
* __event type:__ EVENT
* __bucket unit:__ TICK
* __output name:__ employee

##### emitted events
* {"root":{"_header_":{"log":"","name":"time tick","type":2,"timestamp":1455863028},"tick":{}}}