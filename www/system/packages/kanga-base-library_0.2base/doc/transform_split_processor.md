Split Processor
----------------------

This processor is a Node.js bolt that decomposes a field in a data stream into multiple fields, using the given delimiter.<br>
Timestamp in meta is not updated.

* __Category:__ transform
* __Class:__ transform.split
* __Version:__ 0.2

### API

* __input field name__
    * __variable type:__ String
    * __possible values (examples):__ email
    * __limitation:__ It should be existing field in an event
    * __mandatory field__

* __output field name(s)__
    * __variable type:__ String
    * __possible values (examples):__ id, domain
    * __limitation:__ Comma-separated<br>They should not exist in an event
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
* at T1, "person":{"email":"Mark@samsung.com"}
* at T2, "person":{"email":"John@samsung.com"}

##### argument
* __input field name:__ email
* __output field name:__ id, domain
* __output name:__ student

##### emitted events
* at T1, "student":{"email":"Mark@samsung.com", "id":"Mark", "domain":"samsung.com"}
* at T2, "student":{"email":"John@samsung.com", "id":"John", "domain":"samsung.com"}