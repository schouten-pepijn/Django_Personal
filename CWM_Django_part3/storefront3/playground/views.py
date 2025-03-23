from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.core.cache import cache
from templated_mail.mail import BaseEmailMessage
from .tasks.tasks import notify_customer
import requests


def say_hello(request):
    try:
        send_mail('subject', 'message', 'tjY4o@example.com', ['tjY4o@example.com'])

        mail_admins('subject', 'message', html_message='message')

        email = EmailMessage('subject', 'message', 'tjY4o@example.com', ['tjY4o@example.com'])
        email.attach_file('playground/media/princess.png')
        email.send()

        message = BaseEmailMessage(
            template_name='emails/hello.html',
            context = {'name': 'Pepijn'}
        )
        message.send(['tjY4o@example.com'])
      
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

    notify_customer.delay('message')

    return render(request, 'hello.html', {'name': 'Pepijn'})

def cached_hello(request):
    key = 'httpbin_result'
    if cache.get(key) is None:
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        cache.set(key, data)
    return render(request, 'hello.html', {'name': 'Pepijn'})