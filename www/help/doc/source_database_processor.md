Passthrough From Database Processor
===================================

* This processor is an Apache Storm spout that reads records from given DB in batches and converts them into events that are forwarded to next bolt.
* Default batch size is set to 10.
* It has the capability to select the number of records to be fetched from DB.
* Timestamp in meta is updated as emitting time.

* __Category:__ source
* __Java class:__ com.sec.kanga.spout.DatabaseSpout
* __Version:__ 0.8

## API

|No.|required field      |variable type|possible values (examples)|Limitation                                                                                              |
|---|--------------------|-------------|--------------------------|--------------------------------------------------------------------------------------------------------|
|1  |Output (stream) name|string       |"employee"                |None                                                                                                    |
|2  |DB driver           |enum         |POSTGRESQL                |Proper database driver should be chosen.                                                                |
|3  |DB server host port |string       |"10.261.61.61:54322"      |The DB Connection URL should be correct and User can able to connect with DB with this URL from anywhere|
|4  |DB name             |string       |"kangabi"                 |DB Name should be followed by SQL naming standards                                                      |
|5  |DB user name        |string       |"kanga"                   |DB User Name should be followed by SQL naming standards                                                 |
|6  |DB password         |string       |"kanga123!"               |DB Password should be followed by SQL naming standards                                                  |
|7  |Table Name          |string       |"kanga_help'              |The table should be exist in the DB                                                                     |
|8  |Paging size         |int          |1000                      |It should be positive Integer                                                                           |
|9  |Sleeping time       |int          |X ms                      |It should be positive Integer                                                                           |

## Feature

|Category|Command                  |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type       |
|--------|-------------------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|------------------------|
|Source  |passthrough_from_database|No                                |No                   |No                    |No                                       |No      |No                |Rows ind DB     |Collection (Rows) / Data|

## Example

![Passthrough from database example][passthroughfromdatabase_example]

[passthroughfromdatabase_example]: images/source_passthroughfromdatabase_example.png