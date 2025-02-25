from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError

def say_hello(request):
    try:
        send_mail('subject', 'message', 'tjY4o@example.com', ['tjY4o@example.com'])
        mail_admins('subject', 'message', html_message='message')
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

    return render(request, 'hello.html', {'name': 'Mosh'})
