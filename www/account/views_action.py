# Create your views here.
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from account.services import UserService, AuthService
from account.forms import CreateUserForm, CreateRoleForm, EditUserForm, EditRoleForm, SuccessMessageForm
from account.models import Role
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse

# This is login method which check the authentication and set the user into session
def login(request):

    redirect_to = request.POST.get('return_uri', request.GET.get('return_uri', ''))
    #Checking if the user is already authenticated and in session
    if request.user.is_authenticated():
        return HttpResponseRedirect('/account/index.html')
    else:
        if request.method == 'POST':
            id = request.POST.get('username','')
            password = request.POST.get('password','')

            user = authenticate(username=id, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    permission = user.get_group_permissions()
                    print permission
                    user_service = UserService()
                    user_serach_index = user_service.get_user_serach_index(id)
                    # print 'user_serach_index ----> ',user_serach_index
                    request.session["permission"] = str(permission)
                    request.session["user_serach_index"] = str(user_serach_index)
                    return HttpResponseRedirect(redirect_to)
                else:
                    messages.add_message(request, messages.ERROR, 'User is not yet active.')
                    return render(request, 'account/login_two_columns.html')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid username or password.')
                return render(request, 'account/login_two_columns.html')

        if request.method == 'GET':
            redirect_to = request.GET.get('return_uri', '')
            return render(request, 'account/login_two_columns.html', {'return_uri': redirect_to})

    return render(request, 'account/login_two_columns.html')

# This method create the Users
def create_user(request):
    msg = ''
    msg_level = ''
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            try:
                user_service = UserService()
                user_service.addUser(form.cleaned_data['id'],form.cleaned_data['full_name'],form.cleaned_data['email_address'],form.cleaned_data['password'])
                msg_level = 'alert-success'
                msg = 'The User Successfully Added.'
            except:
                msg_level = 'alert-danger'
                msg = 'There is some error while creating the user.'
        else:
            initialData = {'form': form}
            csrfContext = RequestContext(request, initialData)
            return render_to_response('account/register.html', csrfContext)
    return render(request, 'account/success_message.html', {'msg': msg, 'msg_level': msg_level})

# This method use for adding the role
@login_required
@permission_required('account.add_role', raise_exception=True)
def add_role(request):
    if request.method == 'POST':
        form = CreateRoleForm(request.POST)
        if form.is_valid():
            permission_list = request.POST.getlist('selected_permission_list')
            role_list = request.POST.getlist('selected_role_list')
            print 'TESTing....',form.cleaned_data['restrict_search_timerange']
            try:
                auth_service = AuthService()
                auth_service.createRole(form.cleaned_data['role_name'],permission_list,role_list,
                                        form.cleaned_data['restrict_search_terms'],form.cleaned_data['restrict_search_timerange'],
                                        form.cleaned_data['userlevel_concurrent_searchjobs_limit'],form.cleaned_data['userlevel_concurrent_realtime_searchjobs_limit'],
                                        form.cleaned_data['rolelevel_concurrent_searchjobs_limit'],form.cleaned_data['rolelevel_concurrent_realtime_searchjobs_limit'],
                                        form.cleaned_data['limit_total_jobs_disk_quota'], form.cleaned_data['selected_indexes'],form.cleaned_data['selected_search_indexes'])
            except:
                return HttpResponse('There is some error while creating the role')
        else:
            initialData = {'form': form}
            csrfContext = RequestContext(request, initialData)
            return render_to_response('account/addrole.html', csrfContext)
    else:
        data = {
            'role_name':'',
            'restrict_search_timerange': -1,
            'userlevel_concurrent_searchjobs_limit': 3,
            'userlevel_concurrent_realtime_searchjobs_limit': 6,
            'rolelevel_concurrent_searchjobs_limit': 50,
            'rolelevel_concurrent_realtime_searchjobs_limit': 100,
            'limit_total_jobs_disk_quota': 100
        }
        form = CreateRoleForm(data)
        # return render(request, 'account/addrole.html')
        return render(request, 'account/addrole.html', {'form': form})

    return render(request, 'account/roles.html')

# This method use for adding the role
@login_required
@permission_required('auth.add_permission', raise_exception=True)
def add_permission(request):
    if request.method == 'POST':
        permission_name = request.POST.get('permission_name')
        permission_Code = request.POST.get('permission_Code')
        application_list = request.POST.get('application_list')
        content_list = request.POST.get('content_list')
        print permission_name, permission_Code, application_list, content_list
        try:
            auth_service = AuthService()
            auth_service.create_permission(permission_name, permission_Code, application_list, content_list)
        except:
            return HttpResponse('There is some error while creating the role')
    else:
        return render(request, 'account/addpermission.html')

    return render(request, 'account/permissions.html')

# This method use for editing the user details
@login_required
@permission_required('auth.change_user', raise_exception=True)
def edit_user(request, query_pk):

    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email_address = request.POST.get('email_address')
        password = request.POST.get('password','')
        role_list = request.POST.getlist('selected_role')
        try:
            user_service = UserService()
            user_service.updateUser(username,full_name,email_address,password, role_list)
        except:
                return HttpResponse('There is some error while editing user details')

    if request.method == 'GET':
        user = User.objects.get(username = query_pk)
        print user.groups.all()
        data = {
            'username': str(query_pk),
            'full_name': str(user.first_name),
            'email_address': str(user.email)
        }
        form = EditUserForm(data)

        auth_service = AuthService()
        choices = auth_service.getAllRole()
        form.fields['role'].choices =  choices
        form.fields['selected_role'].choices =  auth_service.fetch_user_role(query_pk)
        form.fields['username'].widget.attrs['readonly'] = True

        form.fields['full_name'].widget.attrs['class'] = 'form-control'
        form.fields['email_address'].widget.attrs['class'] = 'form-control'
        form.fields['full_name'].widget.attrs['class'] = 'form-control'
        form.fields['role'].widget.attrs['class'] = 'form-control'
        form.fields['selected_role'].widget.attrs['class'] = 'form-control'
        form.fields['username'].widget.attrs['class'] = 'form-control'
        form.fields['password'].widget.attrs['class'] = 'form-control'
        form.fields['confirm_password'].widget.attrs['class'] = 'form-control'
        return render(request, 'account/edituser.html', {'form': form})
    href = reverse('account:user-list')
    return HttpResponseRedirect(href)

# This method use for editing the role details
@login_required
@permission_required('account.change_role', raise_exception=True)
def edit_role(request, query_pk):

    if request.method == 'POST':
        role_name = query_pk
        restrict_search_terms = request.POST.get('restrict_search_terms', '')
        restrict_search_timerange = request.POST.get('restrict_search_timerange', '-1')
        userlevel_concurrent_searchjobs_limit = request.POST.get('userlevel_concurrent_searchjobs_limit', '3')
        userlevel_concurrent_realtime_searchjobs_limit = request.POST.get('userlevel_concurrent_realtime_searchjobs_limit', '6')
        rolelevel_concurrent_searchjobs_limit = request.POST.get('rolelevel_concurrent_searchjobs_limit', '50')
        rolelevel_concurrent_realtime_searchjobs_limit = request.POST.get('rolelevel_concurrent_realtime_searchjobs_limit', '100')
        limit_total_jobs_disk_quota = request.POST.get('limit_total_jobs_disk_quota','100')
        selected_indexes = request.POST.get('selected_indexes')
        selected_search_indexes = request.POST.get('selected_search_indexes')
        selected_permission_list = request.POST.getlist('selected_permission_list')
        role_list = request.POST.getlist('selected_role_list')

        try:
            auth_service = AuthService()
            auth_service.editRole(role_name,selected_permission_list,role_list, restrict_search_terms, restrict_search_timerange,
                                    userlevel_concurrent_searchjobs_limit,userlevel_concurrent_realtime_searchjobs_limit,
                                    rolelevel_concurrent_searchjobs_limit,rolelevel_concurrent_realtime_searchjobs_limit,
                                    limit_total_jobs_disk_quota, selected_indexes,selected_search_indexes)
        except Exception as e:
            print e
            return HttpResponse('There is some error while editing the role'+str(e))

        return HttpResponseRedirect('/account/role/list')

    if request.method == 'GET':
        role_name = query_pk

        group = Group.objects.get(name = role_name)
        role_detail = Role.objects.get(group_id = group.id)
        print 'in GET ----', role_detail.limit_total_jobs_disk_quota
        data = {
            'role_name': str(role_name),
            'restrict_search_terms': str(role_detail.restrict_search_terms),
            'restrict_search_timerange': str(role_detail.restrict_search_timerange),
            'userlevel_concurrent_searchjobs_limit': str(role_detail.userlevel_concurrent_searchjobs_limit),

            # TODO There is some error while adding below field. Need to fix this issue
            'userlevel_concurrent_realtime_searchjobs_limit': str(role_detail.Userlevel_concurrent_realtime_searchjobs_limit),
            'rolelevel_concurrent_searchjobs_limit': str(role_detail.rolelevel_concurrent_searchjobs_limit),
            'rolelevel_concurrent_realtime_searchjobs_limit': str(role_detail.rolelevel_concurrent_realtime_searchjobs_limit),
            'limit_total_jobs_disk_quota': str(role_detail.limit_total_jobs_disk_quota),
            'selected_indexes': str(role_detail.selected_indexes),
            'selected_search_indexes': str(role_detail.selected_search_indexes)
            }
        form = EditRoleForm(data)

        auth_service = AuthService()
        form.fields['role_list'].choices = auth_service.getAllRole()
        form.fields['selected_role_list'].choices = auth_service.fetch_inherit_role(group.id)

        form.fields['permission_list'].choices = auth_service.fetchAllPermission()
        form.fields['selected_permission_list'].choices = auth_service.fetchGroupPermission(group.id)

        form.fields['role_list'].widget.attrs['class'] = 'form-control'
        form.fields['permission_list'].widget.attrs['class'] = 'form-control'
        form.fields['selected_permission_list'].widget.attrs['class'] = 'form-control'
        form.fields['selected_role_list'].widget.attrs['class'] = 'form-control'

        return render(request, 'account/editrole.html', {'form': form})
    return render(request, 'account/editrole.html')

# This method use for recover the password
def recover_password(request):
    msg = ''
    msg_level = ''
    if request.method == 'POST':
        id = request.POST.get('id','')
        email_address = request.POST.get('email_address','')
        if (id != '' or email_address != ''):
            try:
                if(id != ''):
                    user = User.objects.get(username = id)
                    user_service = UserService()
                    user_service.recoverPassword(user)
                else:
                    user = User.objects.filter(email = email_address)
                    user_service = UserService()
                    user_service.sendMail(user[0])
                msg_level = 'alert-success'
                msg = 'Recovery mail has been sent to your registered email address.'
            except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
                print "Django Error ",e
                print 'user not exist'
                msg_level = 'alert-danger'
                msg = 'User ID/Email address does not registered with Kanga. Please Enter Correct User ID/Email address'
        else:
            return HttpResponse('Please Enter Correct User ID/Email Address')
    return render(request, 'account/success_message.html', {'msg': msg, 'msg_level': msg_level})

# This method use to change user password
def password_change(request):
    msg = ''
    if request.method == 'POST':
        new_password = request.POST.get('new_password','')
        hashcode = request.POST.get('hashcode','')
        try:
            user_service = UserService()
            user_service.changePassword(hashcode, new_password)
            msg = 'Password has been changed.'

        except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
            print "Django Error ",e
            msg = 'Please Enter Correct URL in Browser'

        data = {
            'message': msg
        }
        form = SuccessMessageForm(data)
        return render(request, 'account/success_message.html', {'form': form})

    return render(request, 'account/passwordchange.html')

# This method use for activate the user account
def activate_account(request):
    msg = ''
    if request.method == 'GET':
        hashcode = request.GET.get('hashcode','')
        print hashcode
        try:
            user_service = UserService()
            user_service.activateAccount(hashcode)
            msg = 'User has been activated.'
        except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
                print "Django Error ",e
                msg = 'Something wrong while activating user'
                return HttpResponse('Something wrong while activating user')
    data = {
            'message': msg
    }
    form = SuccessMessageForm(data)
    return render(request, 'account/success_message.html', {'form': form})
