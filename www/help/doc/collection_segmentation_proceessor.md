Segmentation Processor
----------------------

This processor is an Apache Storm bolt that create the segment based on given single field in input stream and pass the collection stream to next processor.<br>
Timestamp in meta is updated to current time.

* __Category:__ collection
* __Java class:__ com.sec.kanga.bolt.collection.SegmentationBolt
* __Version:__ 0.81

### API

* __input field name(s)__
    * __variable type:__ String
    * __possible values (examples):__ gender
    * __limitation:__ Multiple fields should be comma separated. Special chars are not supported
    * __mandatory field__

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ employee
    * __mandatory field__
	
	
### Feature

* __Run-time evaluation (ScriptEngine):__ No
* __Batch window (Bucket):__ No
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ No
* __Group by:__ No
* __Input event type:__ Data
* __Output event type:__ Collection


### Examples

#### Example 1

##### incoming events
* at T1, "person":{"name":"Charlie", "age":25, "gender":"male"}
* at T2, "person":{"name":"Tom", "age":22, "gender":"male"}
* at T3, "person":{"name":"Lily", "age":21, "gender":"female"}


##### argument
* __input field names:__ gender
* __output name:__ employee

##### emitted events
* at T3, "employee":[{"name":"Charlie", "age":25, "gender":"male"},{"name":"Tom", "age":22, "gender":"male"}]