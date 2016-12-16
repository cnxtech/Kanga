from account.services import UserService

__author__ = 'amit1.nagar'
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import Permission, User, Group, ContentType
import json
from account.models import UserDetail, Role
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from sets import Set

# This method fetch all the Permissions
def fetchAllPermission(request):
    permission_list_json = []
    try:
        permission_list = Permission.objects.all()
        for i in range(permission_list.__len__()):
            json_data = {
                "key":str(permission_list[i].id),
                "value":permission_list[i].name
            }
            permission_list_json.append(json_data)

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    return HttpResponse(json.dumps(permission_list_json), content_type="application/json")

# This method fetch all the Users
def fetch_all_user(request):
    user_list_json = []
    try:
        user_list = UserDetail.objects.all()
        for i in range(user_list.__len__()):
            user = User.objects.get(id = user_list[i].user_id)
            json_data = {
                "key":str(user.id),
                "value":user.username
            }
            user_list_json.append(json_data)

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    return HttpResponse(json.dumps(user_list_json), content_type="application/json")

# This method fetch all the User Details
def get_all_user_details(request):
    user_list_json = []
    try:
        user_list = UserDetail.objects.all()
        for i in range(user_list.__len__()):
            user = User.objects.get(id = user_list[i].user_id)
            l = user.groups.values_list('name',flat=True)

            json_data = {
                # "key":str(user.id),
                "user_name": '<a href="#">'+user.username+'</a>',
                "groups":str(l),
                "first_name":str(user.first_name),
                "email":str(user.email)
            }
            user_list_json.append(json_data)

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    json_out_data = '{ "data" :'+str(json.dumps(user_list_json))+'}'
    return HttpResponse(json_out_data,  content_type="application/json")

# This method fetch all the Roles Details
def get_all_role_details(request):
    try:
        role_list = Role.objects.all()
        role_list_json = []

        for i in range(role_list.__len__()):

            group = Group.objects.get(id = role_list[i].group_id)
            permisssion_list = Set()
            selected_roles_list = []
            permission = group.permissions.all()
            restrict_search_terms = role_list[i].restrict_search_terms
            selected_indexes = role_list[i].selected_indexes
            selected_search_indexes = role_list[i].selected_search_indexes
            selected_roles = role_list[i].selected_roles.all()

            for i in range(permission.__len__()):
                permisssion_list.add(str(permission[i]))

            for i in range(selected_roles.__len__()):
                inheritance_group = Group.objects.get(id = selected_roles[i].group_id)
                selected_roles_list.append(str(inheritance_group.name))
                inheritance_permission = inheritance_group.permissions.all()

                for i in range(inheritance_permission.__len__()):
                    permisssion_list.add(str(inheritance_permission[i]))

            json_data = {
                "group_name": '<a href="#">'+group.name+'</a>',
                "permissions": str(permisssion_list),
                "selected_roles": str(selected_roles_list),
                "restrict_search_terms" : restrict_search_terms,
                "selected_indexes" : selected_indexes,
                "selected_search_indexes" : selected_search_indexes
            }
            role_list_json.append(json_data)

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    json_out_data = '{ "data" :'+str(json.dumps(role_list_json))+'}'
    return HttpResponse(json_out_data, content_type="application/json")

# This method fetch all the Role
def fetchAllRole(request):
    try:
        role_list = Role.objects.all()
        role_list_json = []

        for i in range(role_list.__len__()):
            group = Group.objects.get(id = role_list[i].group_id)
            json_data = {
                "key":str(group.id),
                "value":group.name
            }
            role_list_json.append(json_data)

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    return HttpResponse(json.dumps(role_list_json), content_type="application/json")


# This method fetch all the Role
def get_all_permission(request):
    try:
        permission_list = Permission.objects.all()
        permission_list_json = []

        for i in range(permission_list.__len__()):
            content_type = ContentType.objects.get(id = permission_list[i].content_type_id)
            json_data = {
                "name":str(permission_list[i].name),
                "content_type":content_type.name,
                "app_label":content_type.app_label,
                "codename":permission_list[i].codename
            }
            permission_list_json.append(json_data)
        json_out_data = '{ "data" :'+str(json.dumps(permission_list_json))+'}'

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    return HttpResponse(json_out_data, content_type="application/json")

def get_all_user_permission(request):
    user_service = UserService()
    l = user_service.get_user_roles('aaa1')
    print l
    return HttpResponse(l)

# This method fetch all the Role
def get_application_list(request):
    try:
        application_list = ContentType.objects.values_list('app_label', flat=True).distinct()
        application_list_json = []

        for i in range(application_list.__len__()):
            json_data = {
                "key":str(application_list[i]),
                "value":application_list[i]
            }
            application_list_json.append(json_data)

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    return HttpResponse(json.dumps(application_list_json), content_type="application/json")

def get_content_type(request):
    content_list_json = []
    try:
        app_label = request.GET.get('application_list','');
        print app_label
        content_list = ContentType.objects.filter(app_label = app_label)
        print content_list

        for i in range(content_list.__len__()):
            json_data = {
                "key":content_list[i].model,
                "value":str(content_list[i].model)
            }
            content_list_json.append(json_data)

    except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
        print 'Django Exception :',e

    return HttpResponse(json.dumps(content_list_json), content_type="application/json")