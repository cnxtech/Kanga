Percentile Filter Processor
===========================

This processor is an Apache Storm bolt that filters an event based on given percentile. <br>
User should provide inputs like : Field, Side, %. There are 3 options for Side : Upper, Lower, Both and the field must be numeric value.<br>
First It will sort the fields and based on Side, then it will omit the events from collection and emit the reaming collection to the next bolt.<br>
It should be noted that this bolt accepts only events of type 'collection' which are produced by bolts like Segmentation bolt.

* __Category:__ collection
* __Java class:__ com.sec.kanga.bolt.collection.PercentileFilterBolt
* __Version:__ 0.8

## API

|No.|required field          |variable type|possible values (examples)          |limitation                                                                              |
|---|------------------------|-------------|------------------------------------|----------------------------------------------------------------------------------------|
|1  |input field             |string       |"value"                             |The input field should have numeric value in the stream. Special chars are not supported|
|2  |side                    |enum         |both, upper, lower                  |None                                                                                    |
|3  |percentile              |double       |0.2 (=20%). should be below than 1.0|Value between 0.0< x<1.0<br>Special chars are not supported                             |
|4  |type                    |enum         |Inclusive or Exclusive              |None                                                                                    |
|5  |output (collection) name|string       |"colors"                            |None                                                                                    |

## Feature

|Category  |Command          |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|----------|-----------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Collection|percentile_filter|No                                |Yes                  |No                    |No                                       |No      |No                |Collection      |Collection       |

## Example

![Percentile filter example][percentile_filter_example]

[percentile_filter_example]: images/collection_percentilefilter_example.png