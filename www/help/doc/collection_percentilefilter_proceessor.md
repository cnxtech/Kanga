Percentile Filter Processor
----------------------

This processor is an Apache Storm bolt that perform the percentile filtering on incoming input stream of collection.<br>
Timestamp in meta is not updated.

* __Category:__ collection
* __Java class:__ com.sec.kanga.bolt.collection.PercentileFilterBolt
* __Version:__ 0.81

### API

* __input field name__
    * __variable type:__ String
    * __possible values (examples):__ value
    * __limitation:__ The input field should have numeric value in the stream. Special chars are not supported
    * __mandatory field__

* __side__
    * __variable type:__ enum
    * __possible values (examples):__ BOTH, UPPER, LOWER
    * __limitation:__ One of BOTH, UPPER, LOWER
    * __mandatory field__

* __type__
    * __variable type:__ enum
    * __possible values (examples):__ INCLUSIVE, EXCLUSIVE
    * __limitation:__ Either of INCLUSIVE, EXCLUSIVE
    * __mandatory field__

* __percentile__
    * __variable type:__ double
    * __possible values (examples):__ 0.2 (=20%). should be less than 1.0
    * __limitation:__ Value between 0.0< x<1.0. Special chars are not supported
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
* __Input event type:__ Collection
* __Output event type:__ Collection


### Examples

#### Example 1

##### incoming events
* at T1, "colors":[{"color":"black", "value":7}, {"color":"black", "value":5}, {"color":"black", "value":77}, {"color":"black", "value":4}, {"color":"black", "value":12}]


##### argument
* __input field name:__ value
* __side:__ UPPER
* __type:__ EXCLUSIVE
* __percentile:__ 0.2
* __output name:__ colors

##### emitted events
* at T1, "colors":[{"color":"black", "value":7}, {"color":"black", "value":5}, {"color":"black", "value":4}, {"color":"black", "value":12}]
