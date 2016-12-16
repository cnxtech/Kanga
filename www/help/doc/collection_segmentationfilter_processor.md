Segmentation Filter Processor
===========================

This processor is an Apache Storm bolt that filters the event by given field(s) segments and emit the array of accumulated events to the next Bolt.<br>
User can provide field(s) like filter that can work as composite key like (f1+f2+f3...fn) to define the segment.<br>
It should be noted that this bolt produces events of type 'collection'.

* __Category:__ collection
* __Java class:__ com.sec.kanga.bolt.collection.SegmentationBolt
* __Version:__ 0.8

## API

|No.|required field          |variable type|possible values (examples)                                     |limitation                                                               |
|---|------------------------|-------------|---------------------------------------------------------------|-------------------------------------------------------------------------|
|1  |input field(s)          |string       |"color" (User can enter comma separated multiple fields too )  |Multiple field should be comma separated. Special chars are not supported|
|2  |output (collection) name|string       |"colors" (User can put any meaning full output collection name)|None                                                                     |

## Feature

|Category  |Command            |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|----------|-------------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Collection|segmentation_filter|No                                |Yes                  |No                    |No                                       |No      |No                |Data            |Collection       |

## Example

![Segmentation filter example][segmentation_filter_example]

[segmentation_filter_example]: images/collection_segmentation_filter_example.png