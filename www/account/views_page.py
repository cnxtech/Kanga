from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    keys = request.session.keys()
    print keys
    for i in range(keys.__len__()):
        k = keys[i]
        s = 'Key : '+str(k)+' Value : '+str(request.session[k])+' \n'
        messages.add_message(request, messages.INFO, s)
    return render(request,'account/index.html')

def logout(request):
    auth_logout(request)
    msg = 'successfully logged out'
    redirect_to = request.POST.get('return_uri', request.GET.get('return_uri', '/'))
    return render(request,'account/login_two_columns.html', {'msg':msg,
                                                             'invalid': False,
                                                             'return_uri': redirect_to})

def registerUser(request):
    return render(request, 'account/register.html')


@login_required
def user_list(request):
    return render(request, 'account/users.html')

@login_required
def role_list(request):
    return render(request, 'account/roles.html')

@login_required
def permission_list(request):
    return render(request, 'account/permissions.html')

@login_required
def add_role(request):
    return render(request, 'account/addrole.html')

def forgot_password(request):
    return render(request, 'account/forgotpassword.html')