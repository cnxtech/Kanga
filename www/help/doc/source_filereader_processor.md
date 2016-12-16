File Reader Processor
=====================

* This processor is an Apache Storm spout that reads lines from a given input file and converts them into events that are forwarded to next bolt.
* It tail's the input file that is, once the entire content of the file is read wait's for the new lines to be added.
* Timestamp in meta is updated as emitting time.

* __Category:__ source
* __Java class:__ com.sec.kanga.spout.FileReaderSpout
* __Version:__ 0.8

## API

|No.|required field      |variable type|possible values (examples)   |Limitation                                                                                                                      |
|---|--------------------|-------------|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------|
|1  |Output (stream) name|string       |"employee"                   |None                                                                                                                            |
|2  |Input file path     |string       |"/home/kanga/logs/sample.out"|Input path should be correct and file should be resides into that location<br>The processor should have read access for the file|
|3  |Data Rate           |long         |X ms                         |It should be positive integer                                                                                                   |
|4  |Sleeping time       |long         |X ms                         |It should be positive integer                                                                                                   |

## Feature

|Category|Command              |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type |
|--------|---------------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|------------------|
|Source  |passthrough_from_file|No                                |No                   |No                    |No                                       |No      |No                |Lines in file   |Collection (Lines)|

## Example

![File reader example][filereader_example]

[filereader_example]: images/source_filereader_example.png