Save to Elasticsearch Processor
================================

* This processor is an Apache Storm bolt that writes the  incoming events to given Elasticsearch(ES) index.
* Bolt is capable of writing the message content of event as well as message + meta info of event to ES.
* JSON string is extracted out of event and written to ES.
* '@timestamp' which is mandatory for ES is copied from the 'timestamp' field of event.
* User can do the bulk indexing by providing the bulk action size like 1000, 5000 or depending on ES cluster setup.

* __Category:__ sink
* __Java class:__ com.sec.kanga.bolt.sink.SaveToElasticsearch
* __Version:__ 0.8

## API

|No.|required field  |variable type|possible values (examples)            |Limitation                                                                            |
|---|----------------|-------------|--------------------------------------|--------------------------------------------------------------------------------------|
|1  |ES index name   |string       |"emp_log_index"                       |Valid ES index name                                                                   |
|2  |ES document name|string       |"emp_log_doc"                         |Valid ES document name                                                                |
|3  |ES cluster name |string       |"kanga_es_cluster"                    |Valid and existing ES cluster name                                                    |
|4  |ES node list    |string       |"10.261.21.20:9300, 10.261.21.21:9300"|Valid Host:Port comma separated list. ES should be accessible via same Host:Port list.|
|5  |Meta info       |boolean      |true/false                            |Boolean true or false value                                                           |
|6  |Number of Docs  |int          |1000                                  |Valid positive integer value                                                          |
|7  |Flush Size      |int          |50                                    |Valid positive integer value. This value is in MB                                     |
|8  |Flush Interval  |int          |5                                     |Valid positive integer value. This value is in Second                                 |

## Feature

|Category|Command              |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|--------|---------------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Sink    |save_to_elasticsearch|No                                |No                   |No                    |No                                       |No      |No                |Data/Collection |None             |

## Example

![Save to Elasticsearch example][savetoelasticsearch_example]

[savetoelasticsearch_example]: images/sink_savetoelasticsearch_example.png