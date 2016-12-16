Regex Processor
----------------------

This processor is a Node.js bolt that decomposes a String field in a data stream into multiple String fields using the given regular expression.<br>
Timestamp in meta is not updated.

* __Category:__ transform
* __Class:__ transform.regex
* __Version:__ 0.2

### API

* __input field name__
    * __variable type:__ String
    * __possible values (examples):__ email
    * __limitation:__ It should be an existing field in an event
    * __mandatory field__

* __pattern__
    * __variable type:__ String
    * __possible values (examples):__ (.*?)@(.*)
    * __limitation:__ It should be a valid Regex pattern
    * __mandatory field__
    
* __output field names__
    * __variable type:__ String
    * __possible values (examples):__ id, domain
    * __limitation:__ Comma-separated. It should not exist in an event
    * __mandatory field__

* __output field types__
    * __variable type:__ String
    * __possible values (examples):__ string, string
    * __limitation:__ Comma-separated, acceptable types: string, number,boolean,object
    * __mandatory field__
    
* __output name__
    * __variable type:__ String
    * __possible values (examples):__ regex_result (output stream name to be emitted)
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
* at T1, "person":{"name":"Mark", "email":"Mark@samsung.com", "age":21}

##### argument
* __input field name:__ email
* __pattern:__ (.*)?@(.*)
* __output field names:__ id, domain
* __output field types:__ String, String
* __output name:__ employee

##### emitted events
* at T1, "employee":{"id":"Mark", "domain":"samsung.com", "name":"Mark", "email":"Mark@samsung.com", "age":21}