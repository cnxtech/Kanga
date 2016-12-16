Calculate Processor
----------------------

This processor is an Apache Storm bolt that calculate the aggregation on incoming input stream of collection.<br>
Timestamp in meta is not updated.

* __Category:__ collection
* __Java class:__ com.sec.kanga.bolt.collection.CalculateBolt
* __Version:__ 0.81

### API

* __input field name__
    * __variable type:__ String
    * __possible values (examples):__ salary
    * __limitation:__ The input field should have numeric value in the stream. Special chars are not supported
    * __mandatory field__

* __group by__
    * __variable type:__ String
    * __possible values (examples):__ dept, grade
    * __limitation:__ The multiple fields should be comma separated. Special chars are not supported

* __aggregate functions__
    * __variable type:__ String
    * __possible values (examples):__ sum, avg, max
    * __limitation:__ Only sum, avg, min, max, count are supported aggregation. Any other string or special chars are not supported
    * __mandatory field__

* __output name__
    * __variable type:__ String
    * __possible values (examples):__ salary_aggregation_result
    * __mandatory field__
	
	
### Feature

* __Run-time evaluation (ScriptEngine):__ No
* __Batch window (Bucket):__ No
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ No
* __Group by:__ Yes
* __Input event type:__ Collection
* __Output event type:__ Collection


### Examples

#### Example 1

##### incoming events
* at T1, "persons":[{"name":"sean", "weight":70, "gender":"male"}, {"name":"brahma", "weight":85, "gender":"male"}, {"name":"lily", "weight":60, "gender":"female"}, {"name":"lucy", "weight":53, "gender":"female"}]


##### argument
* __input field name:__  weight
* __group by:__ gender
* __aggregate functions:__ avg,sum
* __output name:__ aggs

##### emitted events
* at T1, "aggs":[{"gender":"female", "sum_weight":113.0, "avg_weight":56.5}, {"gender":"male", "sum_weight":155.0, "avg_weight":77.5}]
