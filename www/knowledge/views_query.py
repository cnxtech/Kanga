from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from knowledge.forms import FieldExtractionForm, SavedQueryForm
from knowledge.models import *
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
import json


@login_required
def field_extractions(request):
    info = request.GET['info'] if 'info' in request.GET else ""
    warning = request.GET['warning'] if 'warning' in request.GET else ""
    return render(request, 'knowledge/field_extractions.html', {'info': info, 'warning': warning})

@login_required
def index(request):
    return render(request, 'knowledge/index.html')

@login_required
def field_extraction_list(request, group):
    if group and group != "all":
        fes = RealtimeQuery.objects.filter(user_id=User.objects.filter(group=Group.objects.get(group)))
    else:
        fes = RealtimeQuery.objects.all()
    fe_json_array = []
    node = {"data": fe_json_array}
    if '/workspace/streaming-query/' in request.META['HTTP_REFERER']:
        anchor_url = "/workspace/streaming-query/?wfid="
    else:
        anchor_url = "details/"
    anchor = lambda id, text: "<a id='"+str(id)+"' href='"+anchor_url+str(id)+"'>"+text.capitalize()+"</a>"
    actions = lambda id: "<a href='/workspace/streaming-query/?wfid="+str(id)+"'>Load</a> | <a href='/knowledge/streaming-queries/clone/?wfid="+str(id)+"'>Clone</a> | <a href='/workspace/streaming-query/download/?wfid="+str(id)+"'>Download</a> | " + '<a href="javascript:ajax_delete_topology(\'' + str(id) + '\')">Delete</a>'
    permission = lambda id: "<a href='permissions/"+str(id)+"/'>Permissions</a>"
    for fe in fes:
        last_running = "None" if not fe.last_running else fe.last_running
        fe_json_array.append(
            {
                "id": fe.id,
                "name": anchor(fe.id, fe.name),
                "description": fe.description.capitalize(),
                "running": str(fe.running).capitalize(),
                "last_running": last_running,
                "user_id": fe.user_id.username,
                "sharing": permission(fe.id),
                "actions": actions(fe.id),
            }
        )
    return HttpResponse(json.dumps(node), content_type='application/json')

def streaming_query_delete(request):
    result= {}
    id = request.POST.get("id", "")
    try:
        if RealtimeQuery.objects.filter(id=id).exists():
            query = RealtimeQuery.objects.get(id=id)
            query.delete()
            status = 'ok'
            msg = 'Query deleted successfully.'
    except Exception as e:
        status = 'failed'
        msg = 'Error occur :' + str(e)

    result = {
        'status': status,
        'message': msg
    }
    return HttpResponse(json.dumps(result), content_type='application/json')


def field_extraction_clone(request):
    wfid = request.GET.get("wfid", None)
    if wfid is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    fes = RealtimeQuery.objects.get(id=wfid)
    fes.id = None
    fes.name = "Copy of "+ fes.name
    fes.save()
    new_wfid = fes.id
    redirect_url = reverse('workspace:streaming-query') + '?wfid=' + str(new_wfid)
    return HttpResponseRedirect(redirect_url)


@login_required
def field_extraction_details(request, fe_id):
    fe = get_object_or_404(RealtimeQuery, id=fe_id)
    user = User.objects.get(id=fe.user_id.id)
    last_running = "None" if not fe.last_running else fe.last_running
    json_query = json.dumps(json.loads(fe.query),indent=4)
    query_mode = "Local Mode" if fe.local_mode else "Cluster Mode"
    if request.method == 'POST':
        data = {
            'query_description': fe.description,
            'query_name': fe.name,
            'query_option': fe.query_option,
        }
        # initial is require to check if the form data has changed
        f = FieldExtractionForm(request.POST, initial=data)
        if f.is_valid():
            if 'cancel' in request.POST:
                return HttpResponseRedirect('/knowledge/streaming-queries/')
            elif 'delete' in request.POST:
                fe.delete()
                msg = '['+fe.name+'] is successfully deleted'
                return HttpResponseRedirect('/knowledge/streaming-queries/?warning='+msg)
            elif f.has_changed():
                cd = f.cleaned_data
                fe.name = cd['query_name']
                fe.description = cd['query_description']
                fe.query_option = cd['query_option']
                fe.save()
            msg = '['+fe.name+'] is successfully saved!'
            return HttpResponseRedirect('/knowledge/streaming-queries/?info='+msg)
    else:
        # Get the query from model
        data = {
            'query_description': fe.description,
            'query_name': fe.name,
            'query_option': fe.query_option,
        }
        f = FieldExtractionForm(data)
    return render(request, 'knowledge/field_extraction_details.html',
                  {'form': f, 'fe': fe, 'user': user,
                   'last_running': last_running, 'json_query': json_query,
                   'query_mode':query_mode, 'query_option': fe.query_option})

@login_required
def query_list(request, group):
    if group and group != "all":
        queries = BatchQuery.objects.filter(user_id=User.objects.filter(group=Group.objects.get(group)))
    else:
        queries = BatchQuery.objects.all()
    query_json_array = []
    node = {"data" : query_json_array}
    anchor = lambda id, text: "<a id='"+str(id)+"' href='details/"+str(id)+"/'>"+text.capitalize()+"</a>"
    actions = lambda id: "<a href='/workspace/batch-query/?wfid="+str(id)+"'>Load</a> | <a href='/?clone=yes&wfid="+str(id)+"'>Clone</a>"
    permission = lambda id: "<a href='permissions/"+str(id)+"/'>Permissions</a>"
    status = lambda id: "<a href='permissions/"+str(id)+"/'>Enable</a> | Disable"
    for query in queries:
        scheduled_time = "None" if not query.scheduled_time else query.scheduled_time
        query_json_array.append(
            {
                "id": query.id,
                "name": anchor(query.id, query.name),
                "description": query.description.capitalize(),
                "scheduled_time": scheduled_time,
                "scheduled": query.scheduled,
                "user_id": query.user_id.username,
                "sharing": permission(query.id),
                "status": status(query.enabled),
                "actions": actions(query.id),
            }
        )
    return HttpResponse(json.dumps(node), content_type='application/json')

@login_required
def search_list(request, group):
    if group and group != "all":
        searches = SavedSearch.objects.filter(user_id=User.objects.filter(group=Group.objects.get(group)))
    else:
        searches = SavedSearch.objects.all()
    search_json_array = []
    node = {"data" : search_json_array}
    anchor = lambda id, text: "<a id='"+str(id)+"' href='/workspace/search/?wfid="+str(id)+"'>"+text.capitalize()+"</a>"
    actions = lambda id: "<a href='/workspace/search/?wfid="+str(id)+"'>Load</a> | <a href='/?clone=yes&wfid="+str(id)+"'>Clone</a>"
    permission = lambda id: "<a href='permissions/"+str(id)+"/'>Permissions</a>"
    status = lambda id: "<a href='permissions/"+str(id)+"/'>Enable</a> | Disable"
    for search in searches:
        scheduled_time = "None" if not search.scheduled_time else search.scheduled_time
        search_json_array.append(
            {
                "id": search.id,
                "name": anchor(search.id, search.name),
                "description": search.description.capitalize(),
                "scheduled_time": scheduled_time,
                "scheduled": search.scheduled,
                "user_id": search.user_id.username,
                "sharing": permission(search.id),
                "status": status(search.enabled),
                "actions": actions(search.id),
            }
        )
    return HttpResponse(json.dumps(node), content_type='application/json')

@login_required
def search_list_v2(request, group):
    if group and group != "all":
        searches = SavedSearch.objects.filter(user_id=User.objects.filter(group=Group.objects.get(group)))
    else:
        searches = SavedSearch.objects.all()
    search_json_array = []
    node = {"data" : search_json_array}
    anchor = lambda id, text: "<a id='"+str(id)+"' href='/workspace/search/?wfid="+str(id)+"'>"+text.capitalize()+"</a>"
    actions = lambda id: "<a href='/workspace/search/?wfid="+str(id)+"'>Load</a> | <a href='/?clone=yes&wfid="+str(id)+"'>Clone</a>"
    permission = lambda id: "<a href='permissions/"+str(id)+"/'>Permissions</a>"
    status = lambda id: "<a href='permissions/"+str(id)+"/'>Enable</a> | Disable"
    for search in searches:
        scheduled_time = "None" if not search.scheduled_time else search.scheduled_time
        search_json_array.append(
            {
                "id": search.id,
                "name": search.name,
                "description": search.description.capitalize(),
                "scheduled_time": scheduled_time,
                "scheduled": search.scheduled,
                "user_id": search.user_id.username,
                "sharing": search.id,
                "status": search.enabled,
                "actions": search.id,
            }
        )
    return HttpResponse(json.dumps(node), content_type='application/json')



@login_required
def search_details(request, search_id):
    search = get_object_or_404(BatchQuery, id=search_id)
    user = User.objects.get(id=search.user_id.id)
    scheduled = "None" if not search.scheduled else search.scheduled
    json_search = json.dumps(json.loads(search.search),indent=4)
    if request.method == 'POST':
        data = {
            'search_description': search.description,
            'search_name': search.name,
        }
        # initial is require to check if the form data has changed
        f = SavedQueryForm(request.POST, initial=data)
        if f.is_valid():
            if f.has_changed():
                cd = f.cleaned_data
                search.name = cd['search_name']
                search.description = cd['search_description']
                search.save()
            msg = '['+search.name+'] is successfully saved!'
            return HttpResponseRedirect('/knowledge/searches/?msg='+msg)
    else:
        # Get the search from model
        data = {
            'search_description': search.description,
            'search_name': search.name,
        }
        f = SavedQueryForm(data)
    return render(request, 'knowledge/search_details.html',
                  {'form': f, 'search': search, 'user': user, 'scheduled': scheduled, 'json_search': json_search})


@login_required
def search_permissions(request, search_id):
    search = get_object_or_404(BatchQuery, id=search_id)
    user = User.objects.get(id=search.user_id.id)
    groups = Group.objects.all()
    for group in groups:
        search_perm = BatchQueryPermission.objects.filter(search=search,group=group)
        if not search_perm:
            BatchQueryPermission.objects.create(search=search,group=group)
    search_perms = BatchQueryPermission.objects.filter(search=search)
    if request.method == 'POST':
        for search_perm in search_perms:
            search_perm.readable = False
            search_perm.writable = False
            search_perm.save()
        perms_write = request.POST.getlist("perms_write")
        perms_read = request.POST.getlist("perms_read")
        for read in perms_read:
            search_perm = BatchQueryPermission.objects.get(search=search,group=Group.objects.get(id=read))
            search_perm.readable = True
            search_perm.save()
        for write in perms_write:
            search_perm = BatchQueryPermission.objects.get(search=search,group=Group.objects.get(id=write))
            search_perm.writable = True
            search_perm.save()
        msg = 'permission setting of ['+search.name+'] is successfully saved!'
        return HttpResponseRedirect('/knowledge/searches/?msg='+msg)
    return render(request, 'knowledge/searches_permissions.html',
                  {'search': search, 'search_perms': search_perms})






















