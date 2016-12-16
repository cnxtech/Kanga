Add Field Processor
===================

This processor is an Apache Storm bolt that appends additional field into a data stream.<br>
A value of the additional field can be a constant (such as integer or String value), <br>
or a calculated result of  an JavaScript expression based on the fields in the previous historic data.

* __Category:__ transform
* __Java class:__ com.sec.kanga.bolt.transform.AddFieldBolt
* __Version:__ 0.8

## API

|No.|required field           |variable type|possible values (examples)           |limitation                                             |
|---|-------------------------|-------------|-------------------------------------|-------------------------------------------------------|
|1  |output stream name       |string       |"utility_meter"                      |None                                                   |
|2  |input field name         |string       |"utility_meter.velocity_meter_second"|It should be the name of non-existing field in an Event|
|3  |value                    |string       |"velocity_kilometer_hour * 0.277778" |It should be a valid JavaScript expression             |
|4  |number of previous values|int          |0                                    |0 <= value <= 100                                      |

## Feature

|Category      |Command  |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|--------------|---------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Transformation|add_field|Yes                               |No                   |No                    |Yes                                      |No      |No                |Data            |Data             |

## Example

__Example #1: add_field_bolt(output_name="utility_meter", input_field_name="utility_meter.velocity_meter_second", value="velocity_kilometer_hour * 0.277778", num_prev_values=0)__

![Add field bolt example][addfield_example]

[addfield_example]: images/transform_addfield_example.png