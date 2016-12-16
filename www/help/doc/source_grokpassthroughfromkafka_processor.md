Grok Passthrough From Kafka Processor
=====================================

This processor is an Apache Storm spout that reads logs from given Kafka topic,
perform the grok match and converts them into events that are forwarded to next bolt.
It supports two scenarios:

1. REALTIME : logs are read from last offset of Kafka topic
1. HISTORIC : logs are read from first offset of Kafka topic

Current read offset is maintained in Zookeeper for each topology. Timestamp in meta is updated as emitting time.

* __Category:__ source
* __Java class:__ com.sec.kanga.spout.GrokPassthroughFromKafka
* __Version:__ 0.8

## API

|No.|required field      |variable type|possible values (examples)            |Limitation                                                                                                                                                                                               |
|---|--------------------|-------------|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|1  |Zookeeper host port |string       |"10.260.20.30:2181, 10.261.20.40:2181"|Valid Host:Port comma separated list. Zookeeper should be accessible via same Host:Port list.                                                                                                            |
|2  |Kafka topic         |string       |"employee_info_topic"                 |Valid and existing Kafka topic name.                                                                                                                                                                     |
|3  |Output (stream) name|string       |"employee"                            |None                                                                                                                                                                                                     |
|4  |Scenario            |enum         |REALTIME                              |                                                                                                                                                                                                         |
|5  |gork_field_list     |String       |%{RESPONSE_CODE:responsecode}         |Enter the valid field list as %{KEY1:json_field}%{KEY2:json_field}<br>Special Char not allowed. The string which is impact on RegEx should not allowed<br>The KEY should be reside into grok_pattern_file|
|6  |gork_pattern_file   |String       |/home/kanga/patterns/grok_patterns    |The grok pattern file should be correct and processor should have correct access to read it                                                                                                              |

## Feature

|Category|Command                    |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type       |Output event type|
|--------|---------------------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|-----------------------|-----------------|
|Source  |grok_passthrough_from_kafka|No                                |No                   |No                    |No                                       |No      |No                |Single message in Kafka|Data             |

## Example

![Grok passthrough from Kafka example][grokpassthroughfromkafka_example]

[grokpassthroughfromkafka_example]: images/source_grokpassthroughfromkafka_example.png