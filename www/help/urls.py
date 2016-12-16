from django.conf.urls import patterns, url
from help import views, views_services
from help import init_data

urlpatterns = patterns('',
    # page
    url(r'^tutorials/$', views.tutorials, name='tutorials'),
    url(r'^tutorials/(?P<command_id>\w+)/$', views.tutorials, name='tutorials'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^recommended-process/$', views.recommended_process, name='recommended-process'),
    url(r'^$', views.index, name='index'),
    # Restful api
    url(r'^services/commands/category/$', views_services.filter_categories, name='categories-all'),
    url(r'^services/commands/category/(?P<category_id>\w+)/$', views_services.filter_categories, name='filter_categories'),
    url(r'^services/commands/label/(.*)/$', views_services.filter_labels, name='filter_labels'),
    url(r'^services/processors/$', views_services.processors, name='processors'),
    url(r'^services/help/doc/$', views_services.help_doc, name='uiapp-help-doc'),
    # data initialization in database
    url(r'^initdata/$', init_data.create, name='initdata'),
)