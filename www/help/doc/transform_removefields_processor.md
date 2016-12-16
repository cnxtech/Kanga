Remove Fields Processor
----------------------

This processor is an Apache Storm bolt that removes multiple fields from data stream.<br>
The fields to be deleted are given as a line of String that can be split by comma.<br>
Timestamp in meta is not updated.

* __Category:__ transform
* __Java class:__ com.sec.kanga.bolt.transform.RemoveFieldsBolt
* __Version:__ 0.81

### API

* __input field name(s)__
    * __variable type:__ String
    * __possible values (examples):__ age, empid
    * __limitation:__ It should be an existing field in an event
    * __mandatory field__

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ remove_result (output stream name to be emitted)
    * __mandatory field__


### Feature

* __Run-time evaluation (ScriptEngine):__ No
* __Batch window (Bucket):__ No
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ No
* __Group by:__ No
* __Input event type:__ Data or Collection
* __Output event type:__ Data or Collection


### Examples

#### Example 1

##### incoming events
* at T1, "person":{"name":"Mark", "age":25, "empid":1001}

##### argument
* __input field names:__ age, empid
* __output name:__ employee

##### emitted events
* at T1, "employee":{"name":"Mark"}