Rename Fields Processor
----------------------

This processor is a Node.js bolt that appends additional field into a data stream.<br>
Timestamp in meta is not updated.

* __Category:__ transform
* __Class:__ transform.add-field
* __Version:__ 0.2

### API

* __input field name__
    * __variable type:__ String
    * __possible values (examples):__ gender
    * __limitation:__ It should be the name of non-existing field in an event
    * __mandatory field__

* __value__
    * __variable type:__ String
    * __possible values (examples):__ man
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
* at T1, "person":{"name":"Mark"}
* at T2, "person":{"name":"John"}

##### argument
* __input field name:__ department
* __value:__ human_resource
* __output name:__ stuff

##### emitted events
* at T1, "stuff":{"name":"Mark", "department":"human_resource"}
* at T2, "stuff":{"name":"John", "department":"human_resource"}