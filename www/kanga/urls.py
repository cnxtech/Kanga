from django.conf.urls import patterns, include, url
from django.contrib import admin
from account import views_login
# import socketio.sdjango
from django.views.generic.base import RedirectView

# socketio.sdjango.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kanga.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^kanga-admin/', include(admin.site.urls), name='admin-tool'),
    url(r'^help/', include('help.urls', namespace="help")),
    url(r'^knowledge/', include('knowledge.urls', namespace="knowledge")),
    url(r'^workspace/', include('workspace.urls', namespace="workspace")),
    url(r'^account/', include('account.urls', namespace="account")),
    url(r'^system/', include('system.urls', namespace="system")),
    url(r'^monitor/', include('monitor.urls', namespace="monitor")),
    url(r'^$', views_login.index, name='index'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),

)
