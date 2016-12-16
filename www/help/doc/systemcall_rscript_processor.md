R Script Processor
==================

This processor is an Apache Storm bolt that executes R script using input and output file.

* __Category:__ systemcall
* __Java class:__ com.sec.kanga.bolt.systemcall.RScriptBolt
* __Version:__ 0.8

## API

|No.|required field       |variable type|possible values (examples)|limitations                                                               |
|---|---------------------|-------------|--------------------------|--------------------------------------------------------------------------|
|1  |output (data) name   |string       |"utility_meter"           |None                                                                      |
|2  |Input Channel        |string       |TUPLE                     |Only TUPLE is supported for this version                                  |
|3  |Input File Path      |string       |"/home/kanga/r/input.txt" |It should be valid Linux file path                                        |
|4  |Output File Path     |string       |"/home/kanga/r/output.txt"|It should be valid Linux file path                                        |
|5  |R File Path          |string       |"/home/kanga/r/logic.r"   |It should be valid Linux file path and R file<br>R file should be prepared|
|6  |Maximum Buffer Size  |int          |10                        |0 <= value <= 1000                                                        |
|7  |Maximum Buffer Second|int          |5                         |0 <= value <= 60                                                          |

## Feature

|Category   |Command|Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|-----------|-------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|System Call|rscript|No                                |No                   |No                    |No                                       |No      |No                |Data            |Data             |

## Example

__Example #1: R_script_bolt(output_name="utility_meter", input_channel="TUPLE", input_file_path="/home/kanga/r/input.txt", output_file_path="/home/kanga/r/output.txt", r_file_path="/home/kanga/r/logic.r", 0, 0)__

![R Script example][rscript_example]

[rscript_example]: images/systemcall_rscript_example.png