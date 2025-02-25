from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from .tasks.tasks import notify_customer

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

    return render(request, 'hello.html', {'name': 'Mosh'})
