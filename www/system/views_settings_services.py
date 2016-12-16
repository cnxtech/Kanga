from system.models import Config, Service
from django.core.urlresolvers import reverse
import datetime
import time
import json
from django.http import  HttpResponse, JsonResponse
from system.models import Service, Node
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from system import views
from elasticsearch import Elasticsearch
from workspace.views import get_all_es_host

# This method fetch all the status of all the node and return JSON Array
@login_required
def get_all_status(request):
    json_out = []
    try:
        node_list = Node.objects.all()
        for node in node_list:
            ip = node.ip
            child_status = []
            service_list = Service.objects.filter(node = node)
            for service in service_list:
                if(service.code == 'KAFKA'):
                    kafka_status = check_kafka_status(ip, str(service))
                    child_status.append(kafka_status)
                if(service.code == 'ZOOKEEPER'):
                    zookeeper_status = check_zookeeper_status(ip, str(service))
                    child_status.append(zookeeper_status)

            node_status = check_node_status(ip, str(node))
            node_status['children'] = child_status
            json_out.append(node_status)

    except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    json_out_data = '{ "data" :'+str(json.dumps(json_out))+'}'
    return HttpResponse(json_out_data, content_type='application/json')


def collect_metrics(request):
    query = ''
    range_filter = []
    index_type = ''
    index_name = ''
    if request.method == 'GET':
        print 'in GET loop'
        query = request.GET.get('query','')
        index_name = request.GET.get('index','')
        index_type = request.GET.get('type','')

        _from = request.GET.get('from','')
        _to = request.GET.get('to','')

        range_filter.append(_from)
        range_filter.append(_to)
        print index_type, index_name

    search_body = formulate_query(query,range_filter)
    print search_body
    res = search_api(index_name,index_type,search_body)
    data = json.loads(json.dumps(res))

    i = data['hits']['total']
    print 'Total Number of Docs ---->',i

    # if(json_query != ''):
    #     t_header = fetchAllColumn(multiindex)
    # else:
    #     t_header = prepareFields(data['hits']['hits'][1]['_source'])

    # print t_header
    json_out = []
    for j in range(i):
        # print data['hits']['hits'][j]['_source']
        json_out.append( data['hits']['hits'][j]['_source'])

    json_out_data = '{ "data" :'+str(json.dumps(json_out))+'}'

    return HttpResponse(json_out_data, content_type='application/json')


# This method fetch the status for Kafka
def check_kafka_status(ip, detail):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "kafka.node": ip
                        }
                    }
                ]
            }
        },
        "from": "0",
        "size": "5",
        "sort": [
            {
                "kafka.@timestamp": "desc"
            }
        ],
        "facets": {}
    }

    res = search_api('monitoring_metrics', 'kafka', query)
    data = json.loads(json.dumps(res))
    json_out = data['hits']['hits'][0]['_source']
    collection_time = json_out['@timestamp']
    status = 'green'

    i = len(data['hits']['hits'])
    messagesin_PerSec_list = []
    bytesOut_PerSec_list = []
    bytesIn_PerSec_list = []

    for j in range(i):
        messagesin_PerSec_list.append( data['hits']['hits'][j]['_source']['MessagesInPerSec']['OneMinuteRate'])
        bytesIn_PerSec_list.append( data['hits']['hits'][j]['_source']['BytesInPerSec']['OneMinuteRate'])
        bytesOut_PerSec_list.append( data['hits']['hits'][j]['_source']['BytesOutPerSec']['OneMinuteRate'])

    metric = {
        'MessagesIn/Sec' : messagesin_PerSec_list,
        'BytesOut/Sec' : bytesOut_PerSec_list,
        'BytesIn/Sec': bytesIn_PerSec_list
    }

    ts = time.time()
    status = {
        'ip' : ip,
        'service' : 'kafka',
        'status' : status,
        'detail' : detail,
        'metrics' : metric,
        'collection_time' : collection_time,
        'current_time' : datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    }
    return status


# This method fetch the status for zookeeper
def check_zookeeper_status(ip, detail):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "zookeeper.node": ip
                        }
                    }
                ]
            }
        },
        "from": "0",
        "size": "75",
        "sort": [
            {
                "zookeeper.@timestamp": "desc"
            }
        ],
        "facets": {}
    }

    res = search_api('monitoring_metrics', 'zookeeper', query)
    data = json.loads(json.dumps(res))
    json_out = data['hits']['hits'][1]['_source']
    collection_time = json_out['@timestamp']
    status = 'green'
    i = len(data['hits']['hits'])
    print 'length of Result ---->',i
    zk_avg_latency_list = []
    zk_max_latency_list = []
    zk_min_latency_list = []
    zk_watch_count_list = []
    zk_packets_sent_list = []
    zk_approximate_data_size_list = []

    for j in range(i):
        zk_avg_latency_list.append( data['hits']['hits'][j]['_source']['mntr']['zk_avg_latency'])
        zk_max_latency_list.append( data['hits']['hits'][j]['_source']['mntr']['zk_max_latency'])
        zk_min_latency_list.append( data['hits']['hits'][j]['_source']['mntr']['zk_min_latency'])
        zk_watch_count_list.append( data['hits']['hits'][j]['_source']['mntr']['zk_watch_count'])
        zk_packets_sent_list.append( data['hits']['hits'][j]['_source']['mntr']['zk_packets_sent'])
        zk_approximate_data_size_list.append( data['hits']['hits'][j]['_source']['mntr']['zk_approximate_data_size'])

    metric = {
        'zk Avg latency' : zk_avg_latency_list,
        'zk Max latency' : zk_max_latency_list,
        'zk Min latency': zk_max_latency_list,
        'zk Watch Count': zk_watch_count_list,
        'zk Packet Sent': zk_packets_sent_list,
        'zk Approximate Data Size': zk_approximate_data_size_list
    }

    ts = time.time()
    status = {
        'ip' : ip,
        'service' : 'zookeeper',
        'status' : status,
        'detail' : detail,
        'metrics' : metric,
        'collection_time' : collection_time,
        'current_time' : datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    }
    return status

# This method fetch the status for Node
def check_node_status(ip, detail):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "os.node": ip
                        }
                    }
                ]
            }
        },
        "from": "0",
        "size": "75",
        "sort": [
            {
                "os.@timestamp": "desc"
            }
        ],
        "facets": {}
    }

    res = search_api('monitoring_metrics', 'os', query)
    data = json.loads(json.dumps(res))
    json_out = data['hits']['hits'][0]['_source']
    i = len(data['hits']['hits'])

    memory_utilization = json_out['mem']['percent']
    cpu_idle = json_out['cpu']['idle']
    collection_time = json_out['@timestamp']

    status = 'red'
    print memory_utilization,cpu_idle
    if( memory_utilization < 50 and cpu_idle > 50 ):
        status = 'green'
    if( 50 < memory_utilization < 80 and  50 < cpu_idle < 80 ):
        status = 'yellow'

    cpu_idle_list = []
    cpu_user_list = []
    cpu_system_list = []
    free_memory_list = []
    used_memory_list = []
    memory_percent_list = []
    for j in range(i):
        cpu_idle_list.append( data['hits']['hits'][j]['_source']['cpu']['idle'])
        cpu_user_list.append( data['hits']['hits'][j]['_source']['cpu']['user'])
        cpu_system_list.append( data['hits']['hits'][j]['_source']['cpu']['system'])

        free_memory_list.append( data['hits']['hits'][j]['_source']['mem']['free']/1000000)
        used_memory_list.append( data['hits']['hits'][j]['_source']['mem']['used']/1000000)
        memory_percent_list.append( data['hits']['hits'][j]['_source']['mem']['percent'])

    metric = {
        'CPU Idle' : cpu_idle_list,
        'CPU User' : cpu_user_list,
        'CPU System' : cpu_system_list,
        'Used Memory(MB)' : used_memory_list,
        'Free Memory(MB)' : free_memory_list,
        'Memory Utilization %' : memory_percent_list
    }

    ts = time.time()
    status = {
        'ip' : ip,
        'service' : 'node',
        'status' : status,
        'detail' : detail,
        'metrics' : metric,
        'collection_time' : collection_time,
        'current_time' : datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    }
    return status

def formulate_query(query_string, range_filter):

    if(query_string == ''):
        query = ' "query": { "match_all" :{}}'

    else:
        query = '"query":{"query_string":{"query":"'+str(query_string)+'"}}'

    if(range_filter[0] != '' or range_filter[1] != ''):
        filter = '"filter":{"bool":{"must":[{"range":{"@timestamp":{"gte": "'+str(range_filter[0])+'" ,"lte":"'+str(range_filter[1])+'" }}}]}}'
    else:
        filter = '"filter":{}'

    search_body = '{"from":0,"size":100000, '+query+','+filter+', "sort": { "@timestamp": { "order": "desc" }}}'
    return search_body

def search_api(index_name, index_type, search_body):
    es = Elasticsearch(hosts=get_all_es_host())
    res = es.search(index=str(index_name),doc_type=str(index_type),body=search_body)
    return res


###################################################################################################################################################


























# This method fetch all the config info from config Table
def api_get_all_config(request):
    config_list_json = []
    try:
        config_file_list = Config.objects.all()
        for config in config_file_list:
            service = Service.objects.get (name = config.service_id)
            href = reverse('system:config',kwargs={'query_pk':str(config.id)})
            json_data = {
                "service":'<a href='+ href + '>'+str(service)+'</a>',
                "filename":config.filename,
                "ip": service.node.ip
            }
            config_list_json.append(json_data)

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    json_out_data = '{ "data" :'+str(json.dumps(config_list_json))+'}'
    return HttpResponse(json_out_data,  content_type="application/json")

# This method fetch specific for config Table
def get_config(request, query_pk):
    config_list_json = []
    try:
        config_file_list = Config.objects.all()
        for config in config_file_list:
            service = Service.objects.get (name = config.service_id)
            href = reverse('system:config',kwargs={'query_pk':str(config.id)})
            json_data = {
                "service":'<a href='+ href + '>'+str(service)+'</a>',
                "filename":config.filename,
                "ip": service.node.ip
            }
            if(service.code.lower() == query_pk.lower()):
                config_list_json.append(json_data)

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    json_out_data = '{ "data" :'+str(json.dumps(config_list_json))+'}'
    return HttpResponse(json_out_data,  content_type="application/json")

# This method fetch config based on query string
def api_get_config(request, query_pk):
    try:
        config_file_list = Config.objects.filter(id = str(query_pk))
        for config in config_file_list:
            service = Service.objects.get(name = config.service_id)
            json_data = {
                "ip":service.node.ip,
                "host":service.node.hostname,
                "service":str(config.service_id),
                "filename":config.filename,
                "content":str(config.content)
            }

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    json_out_data = '{ "data" :'+str(json.dumps(json_data))+'}'
    return HttpResponse(json_out_data,  content_type="application/json")
