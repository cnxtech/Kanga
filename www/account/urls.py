from django.conf.urls import url

# from account import views
import account.views_page
import account.views_action
import account.views_utility_services
from account import views_login


urlpatterns = [

    # page
    url(r'^activation/$', account.views_login.activate_account, name='activateaccount'),
    url(r'^index/$', account.views_page.index, name='index'),
    url(r'^register/$', account.views_login.register, name='register'),
    url(r'^register/create-user/result/$', account.views_login.welcome, name='create-user-result'),
    url(r'^login/$', account.views_login.login, name='login'),
    url(r'^logout/$', account.views_login.logout, name='logout'),
    url(r'^forgot-password/$', account.views_login.forgot_password, name='forgot-password'),
    url(r'^recover-password/$', account.views_login.recover_password, name='recover-password'),
    url(r'^create-user/$', account.views_action.create_user, name='create-user'),
    url(r'^users/$', account.views_page.user_list, name='user-list'),
    url(r'^roles/$', account.views_page.role_list, name='role_list'),
    url(r'^permissions/$', account.views_page.permission_list, name='permission_list'),
    url(r'^users/details/([A-Za-z0-9_.^$*+?()[{\|]*)/$', account.views_action.edit_user, name='edit-user'),
    url(r'^roles/details/(\w+)/$', account.views_action.edit_role, name='edit-role'),
    url(r'^roles/add/$', account.views_action.add_role, name='add_role'),
    url(r'^permissions/add/$', account.views_action.add_permission, name='add_permission'),
    url(r'^new-password/$', account.views_action.password_change, name='password_change'),
    # restful api
    url(r'^services/permissions/$', account.views_utility_services.fetchAllPermission, name='fetchAllPermission'),
    url(r'^services/users/$', account.views_utility_services.fetch_all_user, name='fetch_all_user'),
    url(r'^services/roles/$', account.views_utility_services.fetchAllRole, name='fetchAllRole'),
    url(r'^services/applications/$', account.views_utility_services.get_application_list, name='get_application_list'),
    url(r'^services/users/details/$', account.views_utility_services.get_all_user_details, name='get_all_user_details'),
    url(r'^services/roles/details/$', account.views_utility_services.get_all_role_details, name='get_all_role_details'),
    url(r'^services/users/permissions/$', account.views_utility_services.get_all_user_permission, name='get_all_user_permission'),
    url(r'^services/permissions/details/$', account.views_utility_services.get_all_permission, name='get_all_permission'),
    url(r'^services/content-types/$', account.views_utility_services.get_content_type, name='get_content_type'),

]

