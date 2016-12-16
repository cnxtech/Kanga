Rename Fields Processor
----------------------

This processor is a Node.js bolt that substitutes the names of some fields in a data stream.<br>
Timestamp in meta is not updated.

* __Category:__ transform
* __Class:__ transform.rename-fields
* __Version:__ 0.2

### API

* __input field name(s)__
    * __variable type:__ String
    * __possible values (examples):__ name, gender
    * __limitation:__ Comma separated<br>They should be existing fields in an event
    * __mandatory field__

* __output field name(s)__
    * __variable type:__ String
    * __possible values (examples):__ nickname, sex
    * __limitation:__ Comma separated<br>They should not exist in an event
    * __mandatory field__

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ transform_result (output stream name to be emitted)
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
* at T1, "person":{"name":"Mark", "gender":"male"}
* at T2, "person":{"name":"John", "gender":"female"}

##### argument
* __input field name:__ name, gender
* __output field name:__ nickname, sex
* __output name:__ student

##### emitted events
* at T1, "student":{"nickname":"Mark", "sex":"male"}
* at T2, "student":{"nickname":"John", "sex":"female"}