from django.conf.urls import patterns, url
from monitor import views_services, views




urlpatterns = patterns('',
    #page
    url(r'^$', views.index, name='index'),
    url(r'^storm/settings/$', views.storm_settings, name='storm-settings'),
    url(r'^jobs/streaming-queries/$', views.streaming_queries_history, name='streaming-queries-history'),
    url(r'^jobs/batch-queries/$', views.batch_queries_history, name='batch-queries-history'),




    url(r'^running-queries/$', views.topology_summary, name='running-queries'),
    url(r'^running-queries/$', views.topology_summary, name='topology-summary'),
    url(r'^topologies/recent/$', views.topology_summary, name='recent-topology-summary'),


    url(r'^registered-queries/$', views.registered_topology, name='registered-queries'),


    # url(r'^topology/kill/(?P<id>[\W\w\d-]+)/$', views.kill_topology, name='kill-topology'),
    # url(r'^topology/activate/(?P<id>[\W\w\d-]+)/$', views.activate_topology, name='activate-topology'),
    # url(r'^topology/deactivate/(?P<id>[\W\w\d-]+)/$', views.deactivate_topology, name='deactivate-topology'),
    # restful api
    url(r'^services/storm/topologies/$', views_services.storm_topology_summary, name='api-storm-topology-summary'),
    url(r'^services/storm/topologies/(?P<id>[\W\w\d-]+)/$', views_services.storm_topology_details, name='api-storm-topology-details'),
    url(r'^services/storm/clusters/$', views_services.storm_cluster_summary, name='api-storm-cluster-summary'),
    url(r'^services/storm/supervisors/$', views_services.storm_supervisors_summary, name='api-storm-supervisors-summary'),
    url(r'^services/storm/nimbus/configuration/$', views_services.storm_nimbus_configuration, name='api-storm-nimbus-configuration'),
    url(r'^services/topology/kill/(?P<id>[\W\w\d-]+)/$', views_services.kill_topology, name='api-kill-topology'),
    url(r'^services/topology/stat/(?P<id>[\W\w\d-]+)/$', views_services.topology_stat, name='api-topology-stat'),
)

