from django.conf.urls import patterns, url
from system import views,\
                    views_services, views_settings_services, \
                    views_ci,views_ci_services, views_plugins


urlpatterns = patterns('',
    # page
    url(r'^$', views.index, name='index'),
    url(r'^plugins/$', views.plugins, name='plugins'),
    url(r'^summary/$', views.summary, name='summary'),
    url(r'^connected_device/$',views.connected_devices, name='connected-devices'),
    url(r'^connected_device/details/$',views.connected_device_details, name='connected-device-details'),
    url(r'^connected_device/list/$',views.get_deviceList, name='get-connected-device-list'),
    url(r'^connected_device/add/$',views.set_device, name='add-connected-device'),
    url(r'^connected_device/delete/$',views.delete_device, name='delete-connected-device'),
    url(r'^connected_device/status/$',views.api_get_devicesStatus, name='api-get-connected-device-status'),
    url(r'^connected_device/details/status/$',views.api_get_device_details, name='api-get-connected-device-details'),
    url(r'^plugins/base/$',views.api_remote_downdload_library, name='api-remote-download-library'),

    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/ip/$', views.ip_settings, name='ip-settings'),
    # url(r'^settings/(?P<ip>[\w|\d|.|_|-|\W]+)/$', views.settings, name='settings'),
    url(r'^plugins/register/$',views_plugins.plugins_register, name='plugins-register'),
    url(r'^plugins/library/$',views_plugins.plugins_library, name='plugins-library'),
    url(r'^plugins/history/$',views_plugins.plugins_registry_history, name='plugins-history'),


    # restful api
    # url(r'^services/node/services/status/$', views_services.get_services_status, name='api-services-status'),
    # url(r'^services/node/service/command/$', views_services.run_command, name='api-run-command'),
    url(r'^services/plugins/upload/$',views_plugins.upload,name='upload'),
    url(r'^services/plugins/check/$',views_plugins.check,name='check'),
    url(r'^services/plugins/delete/$',views_plugins.delete,name='delete'),
    url(r'^services/plugins/history/$',views_plugins.get_plugins_registry_history,name='api-plugins-history'),
    url(r'^services/plugins/library/$',views_plugins.get_plugins_library,name='api-plugins-library'),
    url(r'^services/plugins/download/(?P<ref>[\w|\d|.|_|-|\W]+)/(?P<id>[\w|\d|.|_|-|\W]+)/$',views_plugins.download_plugins_library,name='api-plugins-download-library'),
    url(r'^services/plugins/uninstall/(?P<library_id>[\w|\d|.|_|-|\W]+)/$',views_plugins.uninstall_plugins_library,name='api-plugins-uninstall-library'),
    url(r'^services/plugins/verify/$',views_plugins.verify_plugins,name='api-verify-plugins'),
    url(r'^services/plugins/register/$',views_plugins.register_plugins,name='api-register-plugins'),
    url(r'^services/plugins/install/$',views_plugins.install_plugins,name='api-install-plugins'),
    url(r'^services/settings/$', views_services.get_config_list, name='api-settings-config-list'),
    url(r'^services/settings/content/$', views_services.config, name='api-settings-config'),


)

