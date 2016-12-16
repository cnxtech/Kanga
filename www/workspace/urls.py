from django.conf.urls import patterns, include, url
from workspace import views, views_subprocess
import help.views_services
from workspace.builder import builder

urlpatterns = [
    # page
    url(r'^$', views.index, name='index'),
    url(r'^streaming-query/$', views.streaming_query, name='streaming-query'),
    url(r'^batch-query/$', views.build_query, name='build_query'),

    # actions
    url(r'^streaming-query/save/', views.add_data_save, name='uiapp-query-save'),
    url(r'^streaming-query/detail/', views.add_data_detail, name='uiapp-query-detail'),
    url(r'^streaming-query/download/', views.add_data_download, name='uiapp-query-download'),
    url(r'^streaming-query/getKafkaInfoInMacro/', views_subprocess.get_kafka_info_in_macro, name='uiapp-get-kafka-info'),
    url(r'^batch-query/save/', views.query_save, name='uiapp-query-save'),
    url(r'^batch-query/detail/', views.query_detail, name='uiapp-query-detail'),
    url(r'^streaming-query/toolbox/', help.views_services.processors, name='processors'),

    url(r'^queries/save/$', views.save_query, name='uiapp-query-save'),
    url(r'^queries/update/$', views.update_query, name='uiapp-query-update'),

    # restful api
    url(r'^services/realtime-queries/validation/(?P<realtimequery_id>\d+)/$', views_subprocess.realtimequery_validate, name='subprocess-realtimequery-validate'),
    url(r'^services/realtime-queries/launch/(?P<realtimequery_id>\d+)/$', views_subprocess.realtimequery_launch, name='subprocess-realtimequery-launch'),
    url(r'^services/kafka/topics/$', views.topic_list, name='kafka-topic-list'),

    # # TODO - The below url will modify once we integrate with Save Query.
    # url(r'^get_all_fields/$', views_report.get_all_fields, name='get_all_fields'),
    # url(r'^get_table_json/$', views_report.get_table_json, name='get_table_json'),
    # url(r'^test_json_query/$', views.builder, name='builder'),
    # url(r'^queryBackend/$', views.execute_json_query, name='queryBackend'),
    # url(r'^fetch/result/$', views.fetchResults, name='fetchResults'),
    url(r'^services/realtime-queries/remote-launch/$', builder.submit_topology_from_deployment_server_call, name='api-submit-topology-from-deployment-server-call'),

]

