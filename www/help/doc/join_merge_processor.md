Merge Processor
----------------------

This processor is an Apache Storm bolt that merges multi-stream as one stream.<br>
Timestamp in meta is not updated.

* __Category:__ join
* __Java class:__ com.sec.kanga.bolt.join.MergeBolt
* __Version:__ 0.81

### API

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ merge_result (output stream name to be emitted)
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
* at T1 (from stream 1), "person":{"age":25}
* at T2 (from stream 2), "employee":{"age":32}
* at T3 (from stream 1), "person":{"age":19}
* at T4 (from stream 2), "employee":{"age":45}


##### argument
* __output name:__ staff

##### emitted events
* at T1, "staff":{"age":25}
* at T2, "staff":{"age":32}
* at T3, "staff":{"age":19}
* at T4, "staff":{"age":45}
