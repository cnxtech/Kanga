Extract And Join Processor
--------------------------

This processor is an Apache Storm bolt that extracts the specified fields from multiple event stream, and emits the joined event whenever an incoming event arrives.<br>
Timestamp in meta is updated to current time.

* __Category:__ join
* __Java class:__ com.sec.kanga.bolt.join.ExtractAndJoinBolt
* __Version:__ 0.81

### API

* __initialize__
	* __variable type:__ String
    * __possible values (examples):__ var target={"field1":0, "field3":0}
    * __limitation:__ It should be proper JavaScript expression that assigns initial values to the target variables as JSON format.
    * __mandatory field__
 
* __assign__
	* __variable type:__ String
    * __possible values (examples):__ target.field1=e1.field1;\n target.field3=e2.field3 
    * __limitation:__ It should be proper JavaScript expression that assigns values in the event streams into the target variables.
    * __mandatory field__ 

* __data object__
	* __variable type:__ String
    * __possible values (examples):__ target
    * __limitation:__ It should be the same as in the initialize script.
    * __mandatory field__ 

* __output name__
	* __variable type:__ String
    * __possible values (examples):__ merge_result (output stream name to be emitted)
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
* at T1, "left":{"k1":"1", "k2":"11"}
* at T2, "right":{"k3":"2", "k4":"22"}
* at T3, "left":{"k1":"3", "k2":"33"}
* at T4, "right":{"k3":"4", "k4":"44"}
* at T5, "left":{"k1":"5", "k2":"55"}
* at T6, "right":{"k3":"6", "k4":"66"}

##### argument
* __initialize:__ var result={"k1":0, "k3":0}
* __assign:__ result.k1=left.k1;result.k3=right.k3
* __data object:__ result
* __output name:__ result

##### emitted events
* at T2, "result":{"k1":"1", "k3":"2"}
* at T3, "result":{"k1":"3", "k3":"2"}
* at T4, "result":{"k1":"3", "k3":"4"}
* at T5, "result":{"k1":"5", "k3":"4"}
* at T6, "result":{"k1":"5", "k3":"6"}
