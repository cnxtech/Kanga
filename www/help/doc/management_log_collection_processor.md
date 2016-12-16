Log Collection Processor
----------------------

This processor is an Apache Storm bolt that perform elasticsearch query execution on incoming input stream, compresses the result in a file, stores it in a Web accessible location and forwards its URL to the next bolt.<br>

* __Category:__ management
* __Java class:__ com.sec.kanga.agent.collector.LogCollectorBolt
* __Version:__ 0.81

### API

this.nodeList = StrSplitter.split(esNodeList);
		this.clusterName = clusterName;
		this.hostPort = esSQLPluginHostPort;
		this.batchSize = batchSize;

* __node_list__
    * __variable type:__ String
    * __possible values (examples):__ 10.261.21.10:9300
    * __limitation:__ The elasticsearch node must be up and running. Multiple fields should be separated by comma and special characters are not supported. 
    * __mandatory field__

* __cluster_name__
    * __variable type:__ String
    * __possible values (examples):__ elasticsearch
    * __limitation:__ It should be a valid cluster name.
    * __mandatory field__


* __batch_size__
    * __variable type:__ int
    * __possible values (examples):__ 5000
    * __limitation:__ Value must not be negative.
    * __mandatory field__

* __sql plugin host port__
    * __variable type:__ String
    * __possible values (examples):__ 10.261.21.10:9300
    * __limitation:__ The plugin must be up and running.
    * __mandatory field__
	
	
### Feature

* __Run-time evaluation (ScriptEngine):__ No
* __Batch window (Bucket):__ No
* __Sliding window (Queue):__ No
* __Access previous values through expression:__ No
* __Group by:__ No
* __Input event type:__ Data
* __Output event type:__ Data


### Examples

##### incoming events
* at T1, "logrequest":{"id":12345, "query":"select * from xyz limit 10000"}


##### emitted events
* at T1, "logresponse":{"id":12345, "url":"http://10.261.21.20/static/data/logrequest_12345.zip", "result":1}
