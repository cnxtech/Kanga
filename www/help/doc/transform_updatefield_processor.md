Update Field Processor
=======================

This processor is an Apache Storm bolt that changes the value of existing field in a data stream.<br>
A value of the updated field can be a constant (such as integer or String value),<br>
or a calculated result of  an JavaScript expression based on the fields in the previous historic data.

* __Category:__ transform
* __Java class:__ com.sec.kanga.bolt.transform.UpdateFieldBolt
* __Version:__ 0.8

## API

|No.|required field           |variable type|possible values (examples)                    |limitations                                                       |
|---|-------------------------|-------------|----------------------------------------------|------------------------------------------------------------------|
|1  |output stream name       |string       |"utility_meter"                               |None                                                              |
|2  |input field name         |string       |"utility_meter.velocity_kilometer_hour"       |It should be an existing field in an Event                        |
|3  |value                    |string       |"utility_meter.velocity_kilometer_hour[1]"    |It should be a valid Java Script expression                       |
|4  |where                    |string       |"utility_meter.velocity_kilometer_hour[0] < 0"|It should be a valid Java Script expression for logical comparison|
|5  |number of previous values|int          |1                                             |0 <= value <= 100                                                 |

## Feature

|Category      |Command     |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|--------------|------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Transformation|update_field|No                                |No                   |No                    |No                                       |No      |No                |Data            |Data             |

## Example

__Example #1: update_field_bolt(output_name="utility_meter", input_field_name="utility_meter.velocity_kilometer_hour", value="utility_meter.velocity_kilometer_hour[1]", where="utility_meter.velocity_kilometer_hour[0] < 0", num_prev_values=1)__

![Update field bolt example][updatefield_example]

[updatefield_example]: images/transform_updatefield_example.png