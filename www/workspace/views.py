from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.http.response import HttpResponseRedirect
from django.conf import settings
from knowledge.models import RealtimeQuery, BatchQuery
from datetime import datetime
import json
import os
import socket
import time
import logging
from sets import Set
from system.models import Service, DatabaseService
import re
import yaml

def index(request):
    return render(request, 'workspace/index.html')


@login_required
def streaming_query(request):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    context = {'IP': ip}
    print ip
    return render(request, 'workspace/streaming-query.html', context)

@login_required
def notebook(request):
    hosts = Service.objects.filter(code=Service.JUPYTER).distinct()
    return render(request, 'workspace/notebook.html', { 'port' : hosts[0].port, 'hostname': hosts[0].node.ip })

@login_required
def build_query(request):
    return render(request, 'workspace/querybuilder.html')

def add_data_save(request):
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        description = request.POST['description']
        data = request.POST['data']
        if RealtimeQuery.objects.filter(id=id).exists():
            fe = RealtimeQuery.objects.get(id=id)
            fe.name = name
            fe.query = data
            fe.description = description
            fe.save()
            return JsonResponse({'status': 'updated OK', 'id': fe.id})
        else:
            fe = RealtimeQuery.objects.create(name=name, query=data, description=description, user_id=request.user)
            return JsonResponse({'status': 'saved OK', 'id': fe.id})

def add_data_detail(request):
    if request.method == 'POST':
        id = request.POST['id']

        if RealtimeQuery.objects.filter(id=id).exists():
            query = RealtimeQuery.objects.get(id=id)
            return JsonResponse(
                {'id': query.id, 'name': query.name, 'description': query.description, 'data': query.query})
        else:
            return JsonResponse({'status': '404', 'message': 'Query Not Found'})

def add_data_download(request):
    id = request.GET.get("wfid", None)

    if RealtimeQuery.objects.filter(id=id).exists():
        query = RealtimeQuery.objects.get(id=id)

        response = HttpResponse(content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename="%s.json"' % id
        response.write(json.dumps({'id': query.id, 'name': query.name, 'description': query.description, 'data': query.query}))
        return response
    else:
        return JsonResponse({'status': '404', 'message': 'Query Not Found'})



def query_save(request):
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        description = request.POST['description']
        data = request.POST['data']

        if BatchQuery.objects.filter(id=id).exists():
            query = BatchQuery.objects.get(id=id)
            query.name = name
            query.query = data
            query.description = description
            query.save()
            return JsonResponse({'status': 'updated OK', 'id': query.id})
        else:
            query = BatchQuery.objects.create(name=name, query=data, description=description, user_id=request.user)
            return JsonResponse({'status': 'saved OK', 'id': query.id})

def query_detail(request):
    if request.method == 'POST':
        id = request.POST['id']

        if BatchQuery.objects.filter(id=id).exists():
            query = BatchQuery.objects.get(id=id)
            return JsonResponse(
                {'id': query.id, 'name': query.name, 'description': query.description, 'data': query.query})
        else:
            return JsonResponse({'status': '404', 'message': 'Query Not Found'})

def api_query_remove(request):
    if request.method == 'POST':
        id = request.POST['id']

        if Query.objects.filter(id=id).exists():
            q = Query.objects.get(id=id)
            q.delete()
            return JsonResponse({'status': 'Remove OK'})
        else:
            return JsonResponse({'status': 'Remove Failed'})


def api_query_list(request):
    if request.method == 'GET':
        queries = Query.objects.all()
        query_json_array = []
        node = {"data": query_json_array}

        for query in queries:
            query_json_array.append(
                {
                    "id": query.id,
                    "name": query.name,
                    "created": query.created,
                    "updated": query.updated,
                    "owner": "SRIN"
                }
            )

        return HttpResponse(json.dumps(node), content_type='application/json')


def api_component_toolbox(request):
    if request.method == 'GET':
        f = open(os.path.join(settings.BASE_DIR, 'static/uiapp/json/system_component.json'))
        json_string = f.read()
        f.close()
        return JsonResponse(json.loads(json_string), safe=False)


def api_saved_query_list(request):
    if request.method == 'GET':
        f = open(os.path.join(settings.BASE_DIR, 'static/uiapp/json/saved_query_list.json'))
        json_string = f.read()
        f.close()
        return JsonResponse(json.loads(json_string), safe=False)


def api_save_query(request):
    if request.method == 'POST':
        f = open(os.path.join(settings.BASE_DIR, 'static/uiapp/json/saved_query_list.json'))
        json_string = f.read()
        f.close()
        return JsonResponse(json.loads(json_string), safe=False)

def topic_list(request):
    if request.method == 'GET':
        f = open(os.path.join(settings.BASE_DIR, 'static/uiapp/json/topic_list.json'))
        json_string = f.read()
        f.close()
        return JsonResponse(json.loads(json_string), safe=False)

def is_agg(query):
    try:
        if (query['aggs'] != ''):
            return True
        else:
            print 'in els'
            return False
    except (KeyError, TypeError):
        return False

def api_doc_details(request):
    index_name = request.GET.get('index_name','')
    host_list = get_all_es_host()
    es = Elasticsearch(hosts=host_list)
    idx_client = IndicesClient(es)

    mapping_res = idx_client.get_mapping(index=str(index_name))
    doctype_list = []
    for key, value in mapping_res[str(index_name)]['mappings'].iteritems():
        json_data = {
            "doc_name": str(key),
            "value":value
        }
        doctype_list.append(json_data)

    json_out_data = '{ "data" :'+str(json.dumps(doctype_list))+'}'
    return HttpResponse(json_out_data, content_type="application/json")

@login_required
def save_query(request):
    if request.method == 'POST':
        index = request.POST['index']
        query = request.POST['query']
        doc_type = request.POST['doc_type']
        query_name = request.POST['query_name']
        description = request.POST['description']
        selected_fields = request.POST.getlist('selected_fields[]')

        fields = []
        for s in selected_fields:
            fields.append(str(s))

        try:
            search = index+','+doc_type
            query = SavedSearch.objects.create(name=query_name, search=search, dsl=query, description=description, user_id=request.user, selected_fields = fields)
            return JsonResponse({'status': 'saved OK', 'query_name': query_name})
        except Exception as e:
            print 'Django Exception :',e
            return HttpResponse('There is some error while saving the query '+str(e))

@login_required
def update_query(request):
    if request.method == 'POST':
        index = request.POST['index']
        doc_type = request.POST['doc_type']
        query = request.POST['query']
        query_name = request.POST['query_name']
        updated_query_name = request.POST['updated_query_name']
        description = request.POST['description']
        selected_fields = request.POST.getlist('selected_fields[]')

        fields = []
        for s in selected_fields:
            fields.append(str(s))
        try:
            if SavedSearch.objects.filter(name=query_name).exists():
                sq = SavedSearch.objects.get(name=str(query_name))
                sq.dsl = query
                sq.search = index+','+doc_type
                sq.description = description
                sq.name = updated_query_name
                sq.selected_fields = fields
                sq.save()
                return JsonResponse({'status': 'updated OK', 'id': sq.id})
        except Exception as e:
            print 'Django Exception :',e
            return HttpResponse('There is some error while saving the query '+str(e))

def applyUserVars(data, user_vars):
    for key, value in user_vars.iteritems():
        print key, value
        pattern = r'\$' + key + '([\'\s\,")])'
        pattern_obj = re.compile(pattern, re.MULTILINE)
        replacement_string = value + "\\1"
        data = pattern_obj.sub(replacement_string, data)
    return data

@login_required
def search_query(request):
    if request.method == 'GET':
        index = request.GET.get('index','')
        query = request.GET.get('query','')
        doc_type = request.GET.get('doc_type','')
        user_vars = json.loads(request.GET.get('user_vars',''))
        try:
            query = applyUserVars(query, user_vars)
            print(str(index))
            print(str(doc_type))
            print query
            # print(str(query))
            host_list = get_all_es_host();
            es = Elasticsearch(hosts=host_list)
            res = es.search(index=str(index),doc_type=str(doc_type), body=query)
        except Exception as e:
            print str(e)
            if(len(str(e)) >5000) :
                error_msg = str(e)[0:5000]+'...'
            else:
                error_msg = str(e)
            return HttpResponse(error_msg, status=404)

        data = json.loads(json.dumps(res))
        agg_json_out =[]
        if 'aggs' in query:
            agg_json_out = parseAggregation(res, query)

        i = len(data['hits']['hits'])
        print 'Total Number of Docs ---->',len(data['hits']['hits'])
        json_out = []
        for j in range(i):
            json_out.append( data['hits']['hits'][j]['_source'])

        json_out_data = '{ "data" :'+str(json.dumps(json_out))+',  "aggregationResult" :'+str(json.dumps(agg_json_out))+'}'
        return HttpResponse(json_out_data, content_type="application/json")



def get_all_es_host():
    host_list = []
    try:
        es_services = Service.objects.filter(code = 'ELASTICSEARCH')
        for es in es_services:
            instance = str(es.node_id)+':'+str(es.port)
            host_list.append(instance)

    except Exception as e:
        print 'Django Exception :',e

    return list( set(host_list) )

def is_agg(query):
    print 'in Test....'
    try:
        if 'aggs' in query:
            return True
        else:
            return False
    except (KeyError, TypeError):
        return False


def parseAggregation(jsonResult, query):
    json_out = []
    fields = []
    aggregate_results = []

    q = json.loads(query)
    findField(q["aggs"], fields)
    print fields
    recursionBucket(jsonResult['aggregations']['groupByString'],'root', aggregate_results)

    for data in aggregate_results:
        j={}
        field_value = data['key'].split('.')
        field_value.remove('root')

        print field_value, fields
        i = 0
        for f in fields:
            j[f] = field_value[i]
            i = i+1
        j['value'] = data['aggValue']
        json_out.append(j)

    return json_out


def recursionBucket(json_data, k, aggregate_results):
    i = len(json_data['buckets'])
    for j in range(i):
        v = json_data['buckets'][j]
        if 'groupByString' in  v:
            key = k+'.'+str(v['key'])
            recursionBucket(v['groupByString'],key, aggregate_results)
        else:
            key = k+'.'+str(v['key'])
            json_out={
                "key": key,
                "key_value":v['key'],
                "aggValue" : v['aggregationOn']['value']
            }
            aggregate_results.append(json_out)


def findField(json, fields):
    if 'groupByString' in  json:
        fields.append(json["groupByString"]["terms"]["field"])
        findField(json["groupByString"]["aggs"],fields)