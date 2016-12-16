Stdev Processor
----------------------

This processor is an Apache Storm bolt that calculates a standard deviation of the specified numeric field in events.<br>
It calculates standard deviation per groups, according to values of the specified 'GROUP_BY' fields.<br>
Timestamp in meta is updated to current time.

* __Category:__ aggregate
* __Java class:__ com.sec.kanga.bolt.aggregate.StdevBolt
* __Version:__ 0.81

### API

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ aggregation (output stream name to be emitted)
    * __mandatory field__

* __window type__
    * __variable type:__ enum
    * __possible values (examples):__ BATCH 
    * __limitation:__ Either of BATCH and SLIDING
    * __mandatory field__

* __window unit__
    * __variable type:__ enum
    * __possible values (examples):__ SECOND 
    * __limitation:__ One of TICK, SECOND, MINUTE and HOUR
    * __mandatory field__

* __window size__
    * __variable type:__ int
    * __possible values (examples):__ 5 (TICK or SECOND/MINUTE/HOUR)
    * __limitation:__ If TICK-based mode: windowUnit is TICK and windowSize should not be greater than 100<br> If TIME-based mode: windowUnit is SECOND/MINUTE/HOUR and windowSize*windowUnit should not be greater than 1 hour
    * __mandatory field__
    
* __group by field(s)__
    * __variable type:__ String
    * __possible values (examples):__ gender
    * __limitation:__ Comma-separated field names.<br>Each field name should be an existing field in an event               
    * __optional field__

* __input field name(s)__
    * __variable type:__ String
    * __possible values (examples):__ age
    * __limitation:__ Comma-separated field names.<br>Each field name should be an existing field in an event               
    * __mandatory field__

* __output event type__
    * __variable type:__ enum
    * __possible values (examples):__ DATA
    * __limitation:__ Either of DATA and COLLECTION
    * __mandatory field__  


### Feature

* __Run-time evaluation (ScriptEngine):__ No
* __Batch window (Bucket):__ Yes
* __Sliding window (Queue):__ Yes
* __Access previous values through expression:__ No
* __Group by:__ Yes
* __Input event type:__ Data
* __Output event type:__ Data or Collection


### Examples

#### Example 1

##### incoming events
* at T1, "person":{"gender":"male", "height":150, "age":50}
* at T2, "person":{"gender":"female", "height":150, "age":45}
* at T3, "person":{"gender":"male", "height":160, "age":28}

##### argument
* __window type:__ BATCH
* __window unit:__ TICK
* __window size:__ 3
* __group by fields:__ gender
* __input field name:__ age
* __output event type:__ DATA
* __output name:__ aggregation

##### emitted events
*at T3, event1: "aggregation":{"gender":"female", "height_stdev":0.0}, event2: "aggregation":{"gender":"male", "height_stdev":5.0}