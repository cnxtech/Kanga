Save to Kafka Processor
=======================

* This processor is an Apache Storm bolt that writes the incoming events to given Kafka topic.
* Bolt is capable of writing the message content of event as well as message + meta info of event to Kafka topic.
* JSON string is extracted out of event and written to Kafka topic.
* This bolt has the capability to batch the incoming messages based on time and number of messages.

* __Category:__ sink
* __Java class:__ com.sec.kanga.bolt.sink.SaveToKafka
* __Version:__ 0.8

## API

|No.|required field                        |variable type|possible values (examples)            |Limitation                                                                                      |
|---|--------------------------------------|-------------|--------------------------------------|------------------------------------------------------------------------------------------------|
|1  |Kafka topic                           |string       |"employee_info_log"                   |Valid Kafka topic                                                                               |
|2  |Kafka broker list                     |string       |"10.210.20.30:9092, 10.210.20.40:9092"|Valid Host:Port comma separated list. Kafka server should be accessible via same Host:Port list.|
|3  |Kafka queue buffering max milliseconds|integer      |5000                                  |Time in milliseconds. Should be greater that zero.                                              |
|4  |Kafka batch number of messages        |integer      |200                                   |Should be greater that zero.                                                                    |
|5  |meta info                             |boolean      |true/false                            |Boolean true or false value                                                                     |

## Feature

|Category|Command      |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|--------|-------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Sink    |save_to_kafka|No                                |Yes (bulk pub)       |No                    |No                                       |No      |No                |Data/Collection |None             |

## Example

![Save to Kafka example][savetokafka_example]

[savetokafka_example]: images/sink_savetokafka_example.png