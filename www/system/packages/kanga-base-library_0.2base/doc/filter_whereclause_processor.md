Where Clause Processor
----------------------

This processor is a Node.js bolt that filters the incoming event based on the 'where clause'.<br>
Where clause is a valid JavaScript that returns boolean true/false.<br>
Timestamp in meta is not updated.

* __Category:__ filter
* __Class:__ filter.where-clause
* __Version:__ 0.2

### API

* __condition__
    * __variable type:__ String
    * __possible values (examples):__ colors.value>500 (output name in the previous bolt is colors)
    * __limitation:__ It should be a valid JavaScript expression
    * __mandatory field__
	
* __output name__
    * __variable type:__ String
    * __possible values (examples):__ filter_result (output stream name to be emitted)
    * __mandatory field__
	
	
### Feature

* __Run-time evaluation (ScriptEngine):__ Yes
* __Batch window (Bucket):__ No
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ No
* __Group by:__ No
* __Input event type:__ Data
* __Output event type:__ Data


### Examples

#### Example 1

##### incoming events
* at T1, "person":{"age":25}
* at T2, "person":{"age":32}
* at T3, "person":{"age":17}


##### argument
* __condition:__ person.age > 25
* __output name:__ student

##### emitted events
* at T2, "student":{"age":32}
