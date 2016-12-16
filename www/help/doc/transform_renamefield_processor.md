Rename Field Processor
=======================

This processor is an Apache Storm bolt that substitutes the name of a field in a data stream.

* __Category:__ transform
* __Java class:__ com.sec.kanga.bolt.transform.RenameFieldBolt
* __Version:__ 0.8

## API

|No.|required field      |variable type|possible values (examples)           |limitations                                                  |
|---|--------------------|-------------|-------------------------------------|-------------------------------------------------------------|
|1  |output stream name  |string       |"utility_meter"                      |None                                                         |
|2  |input field name(s) |string       |"utility_meter.velocity_meter_second"|Comma separated<br>They should be existing fields in an Event|
|3  |output field name(s)|string       |'utility_meter.velocity_ms"          |Comma separated<br>They should not exist in an Event         |

## Feature

|Category      |Command     |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|--------------|------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Transformation|rename_field|No                                |No                   |No                    |No                                       |No      |No                |Data            |Data             |

## Example

__Example #1: rename_field_bolt(output_name="utility_meter", input_field_name="utility_meter.velocity_meter_second", output_field_name="utility_meter.velocity_ms")__

![Rename field bolt example][renamefield_example]

[renamefield_example]: images/transform_renamefield_example.png