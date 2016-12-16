Save to File Processor
=======================

* This processor is an Apache Storm bolt that writes the  incoming events to given Elasticsearch(ES) index.
* Bolt is capable of writing the message content of event as well as message + meta info of event to ES.
* JSON string is extracted out of event and written to ES.
* '@timestamp' which is mandatory for ES is copied from the 'timestamp' field of event.
* User can do the bulk indexing by providing the bulk action size like 1000, 5000 or depending on ES cluster setup.

* __Category:__ sink
* __Java class:__ com.sec.kanga.bolt.sink.SaveToFile
* __Version:__ 0.8

## API

|No.|required field  |variable type|possible values (examples)   |limitation                                                                                                       |
|---|----------------|-------------|-----------------------------|-----------------------------------------------------------------------------------------------------------------|
|1  |Output file path|string       |"/home/kanga/logs/sample.out"|The path should be exist into system and User should have correct permission to crearte new file on same location|

## Feature

|Category|Command     |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|--------|------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Sink    |save_to_file|No                                |No                   |No                    |No                                       |No      |No                |Data            |None             |

## Example

![Save to File example][savetofile_example]

[savetofile_example]: images/sink_savetofile_example.png