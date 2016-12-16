from django.conf.urls import patterns, url
from django.conf.urls.static import static
from kanga import settings
from knowledge import views_query


urlpatterns = patterns('',
    url(r'^$', views_query.index, name='index'),
    # page
    url(r'^streaming-queries/$', views_query.field_extractions, name='field_extractions'),
    url(r'^streaming-queries/details/(?P<fe_id>\d+)/', views_query.field_extraction_details, name='query_details'),
    url(r'^streaming-queries/clone/', views_query.field_extraction_clone, name='query_clone'),
    url(r'^streaming-queries/delete/', views_query.streaming_query_delete, name='query_delete'),
    url(r'^streaming-queries/group/(\w+)/$', views_query.field_extraction_list, name='field_extraction_list'), # json
    url(r'^batch-queries/group/(\w+)/$', views_query.query_list, name='query_list'), # json
    url(r'^searches/group/(\w+)/$', views_query.search_list, name='search_list'), # json
    url(r'^searches/group_v2/(\w+)/$', views_query.search_list_v2, name='search_list'), # json
    )

