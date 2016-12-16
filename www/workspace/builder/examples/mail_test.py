from django.core.mail import EmailMultiAlternatives
from datetime import datetime
import os

def send_mail(to,subject,body):
    msg = EmailMultiAlternatives(subject, to=[to], from_email='sean.h.kim@host.com')
    msg.attach_alternative(body, "text/html")
    msg.send()


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    server_list = ['10.251.21.176']
    kafka_port = '9092'
    topic_name = 'cnc_tool_1_temperature'
    consumer_name = 'sean.h.kim'
    email_address = consumer_name+"@samsung.com"
    message = "alert. please check."
    subject = "test mail => "+message
    body = "Good day! Now is "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    send_mail(email_address,subject,body)
    print 'mail sent'


if __name__ == "__main__":
    main()

