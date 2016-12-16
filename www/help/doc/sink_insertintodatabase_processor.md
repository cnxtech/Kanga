Insert into Database Processor
===================================

* This processor is an Apache Storm bolt that writes the event as a DB record into the specified DB table.
* Bolt is capable of writing the message content as well as message + meta info of event into DB table.
* DB table can either be created by user or auto created by processor based on the fields present in the first message.
* The field ordering between message and DB table is taken care by the bolt.

* __Category:__ sink
* __Java class:__ com.sec.kanga.bolt.sink.DatabaseSpout
* __Version:__ 0.8

## API

|No.|required field           |variable type|possible values (examples)|Limitation                                                                                     |
|---|-------------------------|-------------|--------------------------|-----------------------------------------------------------------------------------------------|
|1  |DB driver                |enum         |POSTGRESQL                |Supported DB driver.                                                                           |
|2  |DB server host port      |string       |"10.261.61.61:5432"       |Valid DB connection url in "Host:Port" format. DB should be accessible via same connection URL.|
|3  |DB name                  |string       |"kangabi"                 |Valid and existing name of DB as per SQL naming standards.                                     |
|4  |DB user name             |string       |"kanga"                   |Valid user name that can be used to connect to DB.                                             |
|5  |DB password              |string       |"abcd1234!"               |Valid user password that can be used to connect to DB.                                         |
|6  |DB table name            |string       |"employee_info"           |Valid table name as per SQL naming standards.                                                  |
|7  |Meta info                |boolean      |true/false                |Boolean true or false value                                                                    |
|8  |create table if not exist|boolean      |create table statement    |Boolean true or false value                                                                    |

## Feature

|Category|Command             |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|--------|--------------------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Sink    |insert_into_database|No                                |No                   |No                    |No                                       |No      |No                |Data/Collection |None             |

## Example

![Insert into database example][insertintodatabase_example]

[insertintodatabase_example]: images/sink_insertintodatabase_example.png