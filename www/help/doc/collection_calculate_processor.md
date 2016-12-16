Calculate Processor
===================

This processor is an Apache Storm bolt that calculates the basic statistics, such as sum, max, min, average & count on events of type collection. <br>
It can also calculate multiple statistics per groups, according to values of the specified 'GROUP_BY' fields. It allows users to select statistics to be calculated.<br>
It should be noted that this bolt accepts only events of type 'collection' which are produced by bolts like Segmentation bolt.

* __Category:__ collection
* __Java class:__ com.sec.kanga.bolt.collection.CalculateBolt
* __Version:__ 0.8

## API

|No.|required field          |variable type|possible values (examples)                                                                         |limitations                                                                                             |
|---|------------------------|-------------|---------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
|1  |aggregate functions     |string       |"sum,avg,max" User can provide comma separated aggregate function names for input field aggregation|Only sum,avg,min,max,count supported aggregation. Any other string or special chars should not supported|
|2  |input field             |string       |"salary"                                                                                           |The input field should have numeric value in the streams. Special chars are not supported               |
|3  |group by                |string       |"dept,grade" User can provide comma separated field names                                          |The multiple field should be comma separated. Special chars are not supported                           |
|4  |output (collection) name|string       |"salary_aggregation_result"                                                                        |None                                                                                                    |

## Feature

|Category  |Command  |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|----------|---------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Collection|calculate|No                                |Yes                  |No                    |No                                       |Yes     |No                |Collection      |Collection       |

## Example

![Calculate bolt example][calculate_example]

[calculate_example]: images/collection_calculate_example.png