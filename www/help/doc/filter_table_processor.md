Table Processor
----------------------

This processor is an Apache Storm bolt that filters the incoming event based on the provided filter columns.<br>
If the filter field is missing in the event then empty value base on type is passed.<br>
Timestamp in meta is not updated.

* __Category:__ filter
* __Java class:__ com.sec.kanga.bolt.filter.TableBolt
* __Version:__ 0.81

### API

* __field(s) name__
    * __variable type:__ String
    * __possible values (examples):__ name, age
    * __limitation:__ The fields should be comma separated
    * __mandatory field__

* __field type(s)__
    * __variable type:__ String
    * __possible values (examples):__ str, num
    * __limitation:__ The fields should be comma separated
    * __mandatory field__

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ filter_result (output stream name to be emitted)
    * __mandatory field__


### Feature

* __Run-time evaluation (ScriptEngine):__ No
* __Batch window (Bucket):__ No
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ No
* __Group by:__ No
* __Input event type:__ Data
* __Output event type:__ Data


### Examples

#### Example 1

##### incoming events
* at T1, "person":{"name":"Mark", "age":25, "empid":1001}
* at T2, "person":{"name":"John", "age":32, "empid":1002}
* at T3, "person":{"name":"Greg", "age":27, "empid":1003}

##### argument
* __field name:__ name, age
* __field type:__ str, num
* __output name:__ employee

##### emitted events
* at T1, "employee":{"name":"Mark", "age":25}
* at T2, "employee":{"name":"John", "age":32}
* at T3, "employee":{"name":"Greg", "age":27}