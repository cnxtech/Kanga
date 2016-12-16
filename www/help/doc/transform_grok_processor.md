Grok Processor
----------------------

This processor is an Apache Storm bolt that decomposes a String field in a data stream into multiple String fields using the given grok pattern.<br>
Timestamp in meta is not updated.

* __Category:__ transform
* __Java class:__ com.sec.kanga.bolt.transform.GrokBolt
* __Version:__ 0.81

### API

* __input field name__
    * __variable type:__ String
    * __possible values (examples):__ access_log
    * __limitation:__ It should be an existing field in an event
    * __mandatory field__

* __grok pattern file__
    * __variable type:__ String
    * __possible values (examples):__ /home/kanga/patterns/grok_patterns
    * __limitation:__ The grok pattern file should be correct and processor should have correct access to read it
    * __mandatory field__
    
* __grok field list__
    * __variable type:__ String
    * __possible values (examples):__ %{RESPONSE_CODE:responsecode}
    * __limitation:__ Enter the valid field list as %{KEY1:json_field}%{KEY2:json_field}<br>Special Char not allowed. The string which is impact on RegEx should not allowed <br>The KEY should be reside into grok_pattern_file
    * __mandatory field__

* __remove source__
    * __variable type:__ boolean
    * __possible values (examples):__ true, false
    * __mandatory field__
    
* __output name__
    * __variable type:__ String
    * __possible values (examples):__ grok_result (output stream name to be emitted)
    * __mandatory field__


### Feature

* __Run-time evaluation (ScriptEngine):__ No
* __Batch window (Bucket):__ No
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ No
* __Group by:__ No
* __Input event type:__ Data or Collection
* __Output event type:__ Data or Collection


### Examples

#### Example 1

##### incoming events
* at T1, "log":{"access_log":"64.242.88.10 - - [07\/Mar\/2004:16:29:16 -0800] \"GET \/twiki\/bin\/edit\/Main\/Header_checks?topicparent=Main.ConfigurationVariables HTTP\/1.1\" 401 12851"}}}

##### argument
* __input field name:__ access_log
* __grok pattern file:__ src/test/resources/grok_patterns
* __grok field list:__ %{COMMONAPACHELOG}
* __remove source:__ false
* __output name:__ log

##### emitted events
* at T1, "log":{"request":"\/twiki\/bin\/edit\/Main\/Header_checks?topicparent=Main.ConfigurationVariables", "MONTH":"Mar", "COMMONAPACHELOG":"64.242.88.10 - - [07\/Mar\/2004:16:29:16 -0800] \"GET \/twiki\/bin\/edit\/Main\/Header_checks?topicparent=Main.ConfigurationVariables HTTP\/1.1\" 401 12851", "HOUR":16, "auth":"-", "ident":"-", "verb":"GET", "TIME":"16:29:16", "INT":-800,"YEAR":2004, "bytes":12851,"response":401, "clientip":"64.242.88.10", "MINUTE":29, "SECOND":16, "httpversion":"1.1", "MONTHDAY":7, "timestamp":"07\/Mar\/2004:16:29:16 -0800"}}}
