from django.core.mail import EmailMultiAlternatives


def send_mail(to,subject,body):
    msg = EmailMultiAlternatives(subject, to=[to])
    msg.attach_alternative(body, "text/html")
    msg.send()


def welcome_message(user,welcome_url):
    body = '<p>Hi '+user.username+',</p>' \
           '<p>Congratulations !! The samsung account has been created for Kanga Portal.</p>' \
           '<p>Please verify your account by below link.</p>' \
           '<p><a href="'+welcome_url+'">'+welcome_url+'</p>' \
           '<p>Thanks,</p><p>Kanga Admin</p>'
    return body


def recover_password_message(user,recover_url):
    body = '<p>Hi '+user.username+',' \
           '<p>Please click below link to generate new password. </p>' \
           '<p>'+recover_url+'</p><p>Thanks,</p><p>Kanga Admin</p>'
    return body