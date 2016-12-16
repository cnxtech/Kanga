Rename Fields Processor
----------------------

This processor is an Apache Storm bolt that ppends additional field into a data stream.<br>
A value of the additional field can be a constant (such as integer or String value), <br>
or a calculated result of  an JavaScript expression based on the fields in the previous historic data.<br>
Timestamp in meta is not updated.

* __Category:__ transform
* __Java class:__ com.sec.kanga.bolt.transform.AddFieldsBolt
* __Version:__ 0.81

### API

* __input field name__
    * __variable type:__ String
    * __possible values (examples):__ gender
    * __limitation:__ It should be the name of non-existing field in an event
    * __mandatory field__

* __value__
    * __variable type:__ String
    * __possible values (examples):__ salary*1.1
    * __limitation:__ It should be a valid JavaScript expression
    * __mandatory field__

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ transform_result (output stream name to be emitted)
    * __mandatory field__


### Feature

* __Run-time evaluation (ScriptEngine):__ Yes
* __Batch window (Bucket):__ No
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ Yes
* __Group by:__ No
* __Input event type:__ Data or Collection
* __Output event type:__ Data or Collection


### Examples

#### Example 1

##### incoming events
* at T1, "person":{"name":"Mark", "salary":1000}
* at T2, "person":{"name":"John", "salary":800}

##### argument
* __input field name:__ salary
* __output field name:__ salary*1.1
* __output name:__ stuff

##### emitted events
* at T1, "stuff":{"name":"Mark", "salary":1100}
* at T2, "stuff":{"name":"John", "salary":880}