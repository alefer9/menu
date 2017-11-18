
# future
from __future__ import absolute_import 
from celery import shared_task
# Django
from django.utils.html import strip_tags
from django.core.mail import (
	EmailMultiAlternatives, send_mail
)
from django.template.loader import render_to_string

# Celery
from celery.decorators import task

from delivery.celery import app


# Sending email Task
@app.task
def enviar_mail(subject, content, to):
    send_mail(subject, content, 'noreply@mail.com', [to], fail_silently=False)

