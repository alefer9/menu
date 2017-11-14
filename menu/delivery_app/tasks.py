from __future__ import absolute_import 
from celery import shared_task
# from celery.registry import Task
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery.decorators import task
from delivery.celery import app
from django.core.mail import send_mail

# Sending email Task
@app.task
def enviar_mail(asunto, contenido, destinatario):
    send_mail(asunto, contenido, 'noreply@mail.com', [destinatario], fail_silently=False)

