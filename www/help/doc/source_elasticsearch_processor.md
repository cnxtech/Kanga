ElasticSearch Processor
=======================

* This processor is an Apache Storm spout that reads records from Elasticsearch node in batches and converts them into events that are forwarded to next bolt.
* Default batch size is set to 1000 records.
* Timestamp in meta is updated as emitting time.

* __Category:__ source
* __Java class:__ com.sec.kanga.spout.ElasticSearchSpout
* __Version:__ 0.8

## API

|No.|required field      |variable type|possible values (examples)            |Limitation                                                                                                            |
|---|--------------------|-------------|--------------------------------------|----------------------------------------------------------------------------------------------------------------------|
|1  |Output (stream) name|string       |"employee"                            |None                                                                                                                  |
|2  |ES node list        |string       |"10.261.21.20:9300, 10.261.21.21:9300"|The IP:Port should be correct and the given ES service should be accessible. Otherwise it throws errors.              |
|3  |ES cluster name     |string       |"kanga_es_cluster"                    |The given ES clsuter name should be correct.                                                                          |
|4  |ES index name       |string       |"emp_log_index"                       |It should already exist.                                                                                              |
|5  |ES document         |string       |"emp_log_doc"                         |It should already exist.                                                                                              |
|6  |ES query ID         |string       |10                                    |Query ID should already exist in DB. User should formulate the ES query in search app first and use that query ID here|
|7  |Paging size         |int          |1000                                  |It should be a positve Integer                                                                                        |
|8  |Sleeping time       |int          |X ms                                  |It should be a positve Integer                                                                                        |

## Feature

|Category|Command                       |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|--------|------------------------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Source  |passthrough_from_elasticsearch|No                                |No                   |No                    |No                                       |No      |No                |Hits in ES      |Collection (Hits)|

## Example

![Elasticsearch spout example][elasticsearchspout_example]

[elasticsearchspout_example]: images/source_elasticsearch_example.png