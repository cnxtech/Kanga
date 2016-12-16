Time Join Processor
--------------------

This processor is an Apache Storm bolt that synchronizes and merges multiple data streams into one stream.<br>
The data tuples from multiple data streams are synchronized, even though there are some time differences between arrivals of tuples, less than the specified threshold.<br>
Timestamp in meta is updated to current time.

* __Category:__ join
* __Java class:__ com.sec.kanga.bolt.join.TimeJoinBolt
* __Version:__ 0.81

### API

* __leading data name__
	* __variable type:__ String
    * __possible values (examples):__ weights
    * __limitation:__ It should be one of the output stream names of the previous bolt.
    * __mandatory field__ 
    
* __max wait time ms__
	* __variable type:__ long
    * __possible values (examples):__ 1000 
    * __limitation:__ Valid time in milliseconds.This value is a weak threshold; this processor cannot precisely guarantee that an event came later than this maximum wait time won't be joined.
    * __mandatory field__ 

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
* __Input event type:__ Data
* __Output event type:__ Data

### Examples

#### Example 1

##### incoming events
* at T1, "left":{"id":"A", "k1":"k1a"}
* at T2, "right":{"id":"B", "k2":"k2a"}
* at T3, "left":{"id":"B", "k1":"k1b"}
* at T4, "right":{"id":"B", "k2":"k2b"}
* at T5, "left":{"id":"C", "k1":"k1c"}
* at T6, "right":{"id":"D", "k2":"k2d"}

##### argument
* __output name:__ result
* __leading data name:__ left
* __max wait time ms:__ 1000

##### emitted events
* at T2, "result":{"id":"A", "k1":"k1a", "k2":"k2a"}
* at T4, "result":{"id":"B", "k1":"k1b", "k2":"k2b"}
* at T6, "result":{"id":"C", "k1":"k1c", "k2":"k2d"}