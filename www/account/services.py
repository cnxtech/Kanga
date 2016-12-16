__author__ = 'amit1.nagar'

from account.models import UserDetail, Role, UserActivation

from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import EmailMessage, EmailMultiAlternatives
# from django.db.models.signals import post_syncdb
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission
import string
from sets import Set
import random
from django.core.urlresolvers import reverse


class UserService():

    # This method add the user details
    def addUser(self,id, full_name, email_address, password):
        try:
            print 'Adding user......'
            new_user = User.objects.create_user(id, email_address, password, first_name = full_name)
            new_user.is_active = False
            new_user.save()
            new_cepuser = UserDetail(user=new_user)
            new_cepuser.save()
            activation_hashcode = str(password_generator(16))
            href = reverse('account:activateaccount')
            link = "http://localhost:8000" + href + "?hashcode=" + activation_hashcode

            UserActivation_detail = UserDetail(user=new_user, activation_hashcode = activation_hashcode)
            UserActivation_detail.save()
            self.add_default_threshold(id)

        except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
            print 'Django Exception :',e
            raise e

        # Sending validation mail. This call might fail if user enter wrong email address.
        try:
            html_content = '<p>Hi '+id+',</p>' \
                                       '<p>Congratulations !! The samsung account has been created for Kanga Portal.</p>' \
                                       '<p>Please verify your account by below link.</p>' \
                                       '<p><a>'+link+'</p>' \
                                       '<p>Thanks,</p><p>Kanga Admin</p>'

            msg = EmailMultiAlternatives('Account Created ', to=[email_address])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        except Exception as e:
            print 'Django Exception :',e

        return "user_added"

    # This method updates the user details
    def updateUser(self, username, full_name, email_address, password, role_list):
        try:
            user = User.objects.get(username = username)
            user.first_name = full_name
            user.email = email_address
            if(password != ''):
                user.set_password(password)
            user.save()

            user = User.objects.get(username = username)
            user.groups.clear()
            for i in range(role_list.__len__()):
                group = Group.objects.get( id=role_list[i] )
                group.user_set.add(user)

            user.save()
            return "user_updated"

        except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
            print 'Django Exception :',e
            raise e

    def recoverPassword(self,user):
        try:
            # raw_password = password_generator(6)
            # user.set_password(raw_password)
            # user.save()

            activation_hashcode = str(password_generator(16))
            href = reverse('account:password_change')
            link = "http://localhost:8000" + href + "?hashcode="+activation_hashcode
            UserActivation_detail = UserActivation.objects.get(username = user.username)

            print UserActivation_detail.passwordchange_hashcode
            UserActivation_detail.passwordchange_hashcode = activation_hashcode
            UserActivation_detail.save()

            html_content = '<p>Hi '+str(user.username)+',' \
                                       '<p>Please click below link to generate new password. </p>' \
                                       '<p>'+str(link)+'</p><p>Thanks,</p><p>Kanga Admin</p>'

            msg = EmailMultiAlternatives('Password Details ', to=[user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return "recover_password_successful"
        except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
            print "Django Exception ",e
            raise e

    def changePassword(self, hashcode, new_password):
        try:
            user_details = UserActivation.objects.get( passwordchange_hashcode=hashcode )
            user = User.objects.get(username = user_details.username)
            user.set_password(new_password)
            user.save()

        except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
            print "Django Exception ",e
            raise e

    def activateAccount(self, hashcode):
        try:
            user_details = UserDetail.objects.get( activation_hashcode=hashcode )
            user = user_details.user
            user.is_active = True
            user.save()
        except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
            print "Django Exception ",e
            raise e

    def get_user_permission(self,username):
        permisssion_list = []
        selected_roles_list = []
        try:
            user = User.objects.get(username = username)
            print user
            group_list = user.groups.all()
            print 'get_user_permission --- >',group_list
            for i in range(group_list.__len__()):
                group = Group.objects.get(name = group_list[i])

                permission = group.permissions.all()
                selected_roles = Role.objects.get(id = group.id).selected_roles.all()

                for i in range(permission.__len__()):
                    permisssion_list.append(str(permission[i]))

                for i in range(selected_roles.__len__()):
                    inheritance_group = Group.objects.get(id = selected_roles[i].group_id)
                    selected_roles_list.append(str(inheritance_group.name))
                    inheritance_permission = inheritance_group.permissions.all()

                    for i in range(inheritance_permission.__len__()):
                        permisssion_list.append(str(inheritance_permission[i]))

        except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
            print "Django Exception ",e
            # raise e
        return permisssion_list

    def get_user_roles(self,username):
        role_list = []
        try:
            user = User.objects.get(username = username)
            group_list = user.groups.all()
            print 'get_user_permission --- >',group_list
            for i in range(group_list.__len__()):
                group = Group.objects.get(name = group_list[i])
                role_list.append(group.name)

                selected_roles = Role.objects.get(id = group.id).selected_roles.all()
                for i in range(selected_roles.__len__()):
                    inheritance_group = Group.objects.get(id = selected_roles[i].group_id)
                    role_list.append(str(inheritance_group.name))

        except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
            print "Django Exception ",e
            # raise e
        return role_list

    def get_user_serach_index(self, username):
        user_search_index = Set()
        try:
            role_list = self.get_user_roles(username)
            # print 'ROLE List ------> ',role_list
            for i in range(role_list.__len__()):
                group = Group.objects.get(name = role_list[i])
                role_detail = Role.objects.get(id = group.id)
                user_search_index.add(role_detail.selected_search_indexes)

        except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
            print "Django Exception ",e
            # raise e
        print 'user_search_index --->',user_search_index
        return user_search_index



def password_generator(self,size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



class AuthService():

    # This method create the role
    def createRole(self,role_name, permission_list, role_list,
                   restrict_search_terms, restrict_search_timerange,
                   userlevel_concurrent_searchjobs_limit,userlevel_concurrent_realtime_searchjobs_limit,
                   rolelevel_concurrent_searchjobs_limit, rolelevel_concurrent_realtime_searchjobs_limit,
                   limit_total_jobs_disk_quota, selected_indexes, selected_search_indexes ):
        try:
            new_group = Group(name = role_name)
            new_group.save()
            for i in range(permission_list.__len__()):
                permission = Permission.objects.get(id = permission_list[i])
                new_group.permissions.add(permission)
            new_group.save()

            new_role = Role(group_id = new_group.id, id = new_group.id);
            new_role.restrict_search_terms = str(restrict_search_terms)
            new_role.restrict_search_timerange = str(restrict_search_timerange)
            new_role.userlevel_concurrent_searchjobs_limit = str(userlevel_concurrent_searchjobs_limit)
            new_role.Userlevel_concurrent_realtime_searchjobs_limit = str(userlevel_concurrent_realtime_searchjobs_limit)
            new_role.rolelevel_concurrent_searchjobs_limit = str(rolelevel_concurrent_searchjobs_limit)
            new_role.rolelevel_concurrent_realtime_searchjobs_limit = str(rolelevel_concurrent_realtime_searchjobs_limit)
            new_role.limit_total_jobs_disk_quota = str(limit_total_jobs_disk_quota)
            new_role.selected_indexes = str(selected_indexes)
            new_role.selected_search_indexes = str(selected_search_indexes)

            # TODO : Below code is not working for Inheritance the role and self join with same table. Need some time to fix this issue
            new_role.save()
            for i in range(role_list.__len__()):
                role = Role.objects.get(id=str(role_list[i]))
                print 'ROLE--------->',role
                new_role.selected_roles.add(role)

            new_role.save()
            return "role_added"

        except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
            print 'Django Exception :',e
            raise e

    # This method use for edit the role details
    def editRole(self, role_name, permission_list, role_list,
                   restrict_search_terms, restrict_search_timerange,
                   userlevel_concurrent_searchjobs_limit,userlevel_concurrent_realtime_searchjobs_limit,
                   rolelevel_concurrent_searchjobs_limit, rolelevel_concurrent_realtime_searchjobs_limit,
                   limit_total_jobs_disk_quota,selected_indexes, selected_search_indexes ):
        try:
            group = Group.objects.get(name = role_name)
            # old_permissions = group.permissions.all()
            # print old_permissions
            group.permissions = []
            # for j in range(old_permissions.__len__()):
            #     group.permissions.remove(old_permissions[j])

            for i in range(permission_list.__len__()):
                permission = Permission.objects.get(id = permission_list[i])
                group.permissions.add(permission)
            group.save()

            role = Role.objects.get(group_id = group.id)
            role.restrict_search_terms = str(restrict_search_terms)
            role.restrict_search_timerange = str(restrict_search_timerange)
            role.userlevel_concurrent_searchjobs_limit = str(userlevel_concurrent_searchjobs_limit)
            role.Userlevel_concurrent_realtime_searchjobs_limit = str(userlevel_concurrent_realtime_searchjobs_limit)
            role.rolelevel_concurrent_searchjobs_limit = str(rolelevel_concurrent_searchjobs_limit)
            role.rolelevel_concurrent_realtime_searchjobs_limit = str(rolelevel_concurrent_realtime_searchjobs_limit)
            role.selected_indexes = str(selected_indexes)
            role.limit_total_jobs_disk_quota = str(limit_total_jobs_disk_quota)
            role.selected_search_indexes = str(selected_search_indexes)
            role.save()

            # TODO : Below code is not working for Inheritance the role and self join with same table. Need some time to fix this issue
            role.selected_roles = []
            for i in range(role_list.__len__()):
                inheritance_role = Role.objects.get(id=role_list[i])
                role.selected_roles.add(inheritance_role)

            role.save()
            return "role_updated"

        except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
            print 'Django Exception :',e
            raise e

    # This method use to fetch all roles for list box
    def getAllRole(self):
        CHOICES = []
        try:
            role_list = Role.objects.all()
            for i in range(role_list.__len__()):
                group = Group.objects.get(id = role_list[i].group_id)
                s = ( str(group.id),group.name+" >>" )
                CHOICES.append(s)
            return CHOICES
        except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
            print 'Django Exception :',e
            return CHOICES

    # This method use to fetch user roles for list box
    def fetch_user_role(self, username):
        CHOICES = []
        try:
            user = User.objects.get(username = username)
            group_list = user.groups.all()
            for i in range(group_list.__len__()):
                group = Group.objects.get(name = group_list[i])
                s = ( str(group.id),"<< "+group.name )
                CHOICES.append(s)

            return CHOICES
        except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
            print 'Django Exception :',e
            return CHOICES

    # This method use to fetch all Permissions for list box
    def fetchAllPermission(self):
        CHOICES = []
        try:
            permission_list = Permission.objects.all()
            for i in range(permission_list.__len__()):
                s = ( str(permission_list[i].id), permission_list[i].name )
                CHOICES.append(s)

            return CHOICES
        except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
            print 'Django Exception :',e
            return CHOICES

    # This method use to fetch group Permissions for list box
    def fetchGroupPermission(self, group_id):
        CHOICES = []
        try:
            group = Group.objects.get(id = group_id)
            permission = group.permissions.all()
            for i in range(permission.__len__()):
                s = ( str(permission[i].id),permission[i].name )
                CHOICES.append(s)
            return CHOICES

        except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
            print 'Django Exception :',e
            return CHOICES

    # This method use to fetch inherit_role for list box
    def fetch_inherit_role(self, group_id):
        CHOICES = []
        try:
            role = Role.objects.get(id = group_id)
            inherit_role_list = role.selected_roles.all()
            for i in range(inherit_role_list.__len__()):
                group = Group.objects.get(id = inherit_role_list[i].id)
                s = ( str(inherit_role_list[i].id),group.name )
                CHOICES.append(s)
            return CHOICES

        except (ObjectDoesNotExist ,MultipleObjectsReturned) as e:
            print 'Django Exception :',e
            return CHOICES

    def create_permission(self, permission_name, permission_Code, application_list, content_list):
        try:
            content_type = ContentType.objects.get(app_label=application_list, model=content_list)
            new_permission = Permission.objects.get_or_create(codename=permission_Code, name=permission_name, content_type=content_type)
            return "permission_added"

        except (ObjectDoesNotExist ,MultipleObjectsReturned, Exception) as e:
            print 'Django Exception :',e
            raise e

