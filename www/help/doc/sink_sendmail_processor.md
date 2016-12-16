Send Mail Processor
====================

* This processor is an Apache Storm bolt that sends the incoming events via e-mail.
* JSON string is extracted out of event and written to the e-mail content.

* __Category:__ sink
* __Java class:__ com.sec.kanga.bolt.sink.SendEmail
* __Version:__ 0.8

## API

|No.|required field|variable type|possible values (examples)|Limitation                                                   |
|---|--------------|-------------|--------------------------|-------------------------------------------------------------|
|1  |host          |string       |"smtp.samsung.com"        |Valid and existing SMTP host that can be used to send emails.|
|2  |port          |int          |25                        |Valid SMTP port.                                             |
|3  |to            |string       |"choonoh.lee@samsung.com" |Valid email id of recipient.                                 |
|4  |subject       |string       |"system alert"            |Valid email subject string                                   |

## Feature

|Category|Command  |Run-time evaluation (ScriptEngine)|Batch window (Bucket)|Sliding window (Queue)|Access previous values through expression|Group by|Crontab expression|Input event type|Output event type|
|--------|---------|----------------------------------|---------------------|----------------------|-----------------------------------------|--------|------------------|----------------|-----------------|
|Sink    |send_mail|No                                |No                   |No                    |No                                       |No      |No                |Data            |None             |

## Example

![Send mail example][sendmail_example]

[sendmail_example]: images/sink_sendmail_example.png