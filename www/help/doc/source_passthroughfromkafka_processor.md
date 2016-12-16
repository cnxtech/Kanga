Passthrough From Kafka Processor
=====================================

This processor is an Apache Storm spout that reads logs from given Kafka topic and converts them into events that are forwarded to next bolt.
It supports two scenarios:

1. REALTIME : logs are read from last offset of Kafka topic
1. HISTORIC : logs are read from first offset of Kafka topic

Current read offset is maintained in Zookeeper for each topology. Timestamp in meta is updated as emitting time.

* __Category:__ source
* __Java class:__ com.sec.kanga.spout.PassthroughFromKafka
* __Version:__ 0.8

## API

|No.|required field      |variable type|possible values (examples)            |Limitation                                                                                   |
|---|--------------------|-------------|--------------------------------------|---------------------------------------------------------------------------------------------|
|1  |Zookeeper host port |string       |"10.260.20.30:2181, 10.261.20.40:2181"|Valid Host:Port comma separated list. Zookeeper should be accessible via same Host:Port list.|
|2  |Kafka topic         |string       |"employee_info_topic"                 |Valid and existing Kafka topic name.                                                         |
|3  |Output (stream) name|string       |"employee"                            |None                                                                                         |
|4  |Scenario            |enum         |REALTIME                              |None                                                                                         |

## Feature

|Category|Command               |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type       |Output event type|
|--------|----------------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|-----------------------|-----------------|
|Source  |passthrough_from_kafka|No                                |No                   |No                    |No                                       |No      |No                |Single message in Kafka|Data             |

## Example

![Passthrough from Kafka example][passthroughfromkafka_example]

[passthroughfromkafka_example]: images/source_passthroughfromkafka_example.png