Transaction Filter Processor
----------------------

This processor is an Apache Storm bolt that perform the transaction on incoming input stream of collection.<br>
Timestamp in meta is updated to current time.

* __Category:__ collection
* __Java class:__ com.sec.kanga.bolt.function.TransactionBolt
* __Version:__ 0.81

### API

* __input field name__
    * __variable type:__ String
    * __possible values (examples):__ value
    * __limitation:__ Multiple fields should be separated by comma and special characters are not supported.
    * __mandatory field__

* __initializeScript__
    * __variable type:__ String
    * __possible values (examples):__ var target={"field1":0, "field3":0}
    * __limitation:__ It should be proper JavaScript expression that assigns initial values to the target variables as JSON format.
    * __mandatory field__


* __maxBufferMillSec__
    * __variable type:__ int
    * __possible values (examples):__ 500
    * __limitation:__ Value must not be negative.
    * __mandatory field__

* __flushingMillSec__
    * __variable type:__ int
    * __possible values (examples):__ 10000
    * __limitation:__ Value must not be negative.
    * __mandatory field__

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ colors
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

##### incoming events
* at T1, "colors":[{"color":"black", "value":7}, {"color":"black", "value":5}, {"color":"red", "value":77},
{"color":"black", "value":4}, {"color":"red", "value":12}, {"color":"green", "value":4}, {"color":"red", "value":12}]


##### argument
* __input field name:__ color
* __maxPause:__ 5000
* __maxSize:__ 3

##### emitted events
* at T1, "colors":[{"color":"black", "value":7}, {"color":"black", "value":5}, {"color":"black", "value":4}]
</br>"colors":[{"color":"red", "value":77}, {"color":"red", "value":12}, {"color":"red", "value":12}]
