Last Tick Processor
----------------------

This processor is an Apache Storm bolt that samples incoming events based on user given bucket size per unit.<br>
It will choose the last event in a bucket.<br>
If type=STATIC, previous emitted value is emitted where there is no incoming event in the current bucket.<br>
If type=EVENT, only event is emitted, where the current bucket has element(s).<br>
Timestamp in meta is not updated.

* __Category:__ sample
* __Java class:__ com.sec.kanga.bolt.sample.LastTickBolt
* __Version:__ 0.81

### API

* __bucket size__
    * __variable type:__ int
    * __possible values (examples):__ 10
    * __limitation:__ It should be greater than 0
    * __mandatory field__

* __event type__
    * __variable type:__ enum
    * __possible values (examples):__ STATIC, EVENT
    * __limitation:__ Either of STATIC, EVENT
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
* __Batch window (Bucket):__ Yes
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ No
* __Group by:__ No
* __Input event type:__ Data or Collection
* __Output event type:__ Data or Collection


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
* at T3, "employee":{"name":"Greg", "age":27, "empid":1003}