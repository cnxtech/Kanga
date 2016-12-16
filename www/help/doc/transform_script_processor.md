Script Processor
----------------------

This processor is an Apache Storm bolt that executes script on given data object.<br>
Timestamp in meta is not updated.

* __Category:__ transform
* __Java class:__ com.sec.kanga.bolt.transform.ScriptBolt
* __Version:__ 0.81

### API

* __script__
    * __variable type:__ String
    * __possible values (examples):__ object.person.age=20;
    * __limitation:__ It should be a valid java script expression
    * __mandatory field__

* __data object name__
    * __variable type:__ String
    * __possible values (examples):__ object
    * __mandatory field__

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ transform_result (output stream name to be emitted)
    * __mandatory field__


### Feature

* __Run-time evaluation (ScriptEngine):__ Yes
* __Batch window (Bucket):__ No
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ No
* __Group by:__ No
* __Input event type:__ Data or Collection
* __Output event type:__ Data or Collection


### Examples

#### Example 1

##### incoming events
* at T1, "person":{"age":50}
* at T2, "person":{"age":60}

##### argument
* __script:__ object.person.age=20;
* __data object name:__ object
* __output name:__ student

##### emitted events
* at T1, "student":{"age":20}
* at T2, "student":{"age":20}