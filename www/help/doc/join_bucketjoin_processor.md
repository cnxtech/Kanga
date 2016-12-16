BucketJoin Processor
----------------------

This processor is an Apache Storm bolt that joins two sets of data streams using the specified join key.<br>
The events in a time window are joined, with a join option such as INNER, LEFT or RIGHT OUTER, and FULL OUTER.<br>
Timestamp in meta is updated to current time.

* __Category:__ join
* __Java class:__ com.sec.kanga.bolt.join.BucketJoinBolt
* __Version:__ 0.81

### API

* __join type__
    * __variable type:__ enum
    * __possible values (examples):__ INNER
    * __limitation:__ One of INNER, LEFT_OUTER, RIGHT_OUTER, FULL_OUTER
    * __mandatory field__

* __join time__
    * __variable type:__ int
    * __possible values (examples):__ 3
    * __limitation:__ If window_unit is SECOND:<br>0 < window_size <= 3600<br>if window_unit is MINUTE:<br>0 < window_size <= 60<br>If window_unit is HOUR:<br>0 < window_size <= 1
    * __mandatory field__
    
* __join type unit__
    * __variable type:__ enum
    * __possible values (examples):__ SECOND
    * __limitation:__ One of SECOND, MINUTE, HOUR
    * __mandatory field__

* __join key__
    * __variable type:__ String
    * __possible values (examples):__ id
    * __limitation:__ It should be the existing field in both stream name
    * __mandatory field__
    
* __left data name__
    * __variable type:__ String
    * __possible values (examples):__ heights
    * __limitation:__ It should be one of incoming event's data names
    * __mandatory field__

* __right data name__
    * __variable type:__ String
    * __possible values (examples):__ weights
    * __limitation:__ It should be one of incoming event's data names<br>It should not be same as 'left data name'
    * __mandatory field__
    
* __output name__
    * __variable type:__ String
    * __possible values (examples):__ join_result (output stream name to be emitted)
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
* at T1, "left":{"k1":"k1a", "id":"A"}
* at T2, "right":{"k2":"k2a", "id":"A"}
* at T3, "right":{"k2":"k2b", "id":"B"}
* at T4, "left":{"k1":"k1b", "id":"B"}
* at T5, "left":{"k1":"k1c", "id":"C"}
* at T6, "right":{"k2":"k2d", "id":"D"}
* at T7, system time tick

##### argument
* __join type:__ INNER
* __join time:__ 7
* __join type unit:__ SECOND
* __join key:__ id
* __left data name:__ left
* __right data name:__ right
* __output name:__ JOIN

##### emitted events
* at T7, "JOIN":[{"k1":"k1a", "k2":"k2a", "id":"A"},{"k1":"k1b", "k2":"k2b", "id":"B"}]