from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.contrib.auth.models import Group, User
from system.models import JobScript
import json


@login_required
def api_job_scripts(request):
    scripts = JobScript.objects.all()
    scripts_json_array = []
    node = {"data": scripts_json_array}
    if '/workspace/streaming-query/' in request.META['HTTP_REFERER']:
        anchor_url = "/workspace/streaming-query/?wfid="
    else:
        anchor_url = "details/"
    anchor = lambda id, text: "<a id='"+str(id)+"' href='"+anchor_url+str(id)+"'>"+text.capitalize()+"</a>"
    for scripts in scripts:
        last_running = "None" if not scripts.last_running else scripts.last_running
        scripts_json_array.append(
            {
                "id": scripts.id,
                "name": anchor(scripts.id, scripts.name),
                "description": scripts.description.capitalize(),
                "created": str(scripts.created),
                "updated": str(scripts.updated),
                "user_id": scripts.user_id.username,
            }
        )
    return HttpResponse(json.dumps(node), content_type='application/json')
