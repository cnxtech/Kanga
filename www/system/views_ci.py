from django.shortcuts import render
from django.http import  HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from system.models import JobScript
import json


@login_required
def job_scripts(request):
    return render(request,'system/job_scripts.html')