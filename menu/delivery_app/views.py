# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response, HttpResponse
from django.views.generic import CreateView, ListView, UpdateView
from .models import Menu, Menu_options, Options, Request_menu, User
from .forms import MenuForm, OptionsForm, RequestForm
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from pprint import pprint
from .tasks import enviar_mail
from django.urls import reverse

# Sending email function
def Send_menu(self, **kwargs):
	model= Menu
	users= User.objects.exclude(role='Administrator')

	# Getting a pk of the menu selected
	pk = kwargs['pk']
	menu= Menu.objects.get(id=pk)

	# Creating the message of menu
	description = 'Hola!\nDejo el menú de hoy :)\n\n'
	count = 1
	for menu in menu.options.all():
		description += 'Opcion '+str(count)+': '+str(menu)+'\n'
		count += 1
	description += 'Tengan lindo día!\n\n'
	description += 'Para ordenar algo del menu ingresa a este link: http://'+self.get_host()+''+reverse('request_create')

	# Sending email to all of users (loop)
	for user in users:
		print(user.email)

		# Function to send email
		enviar_mail.delay("Cornershop menu of the day", description, user.email)
	return HttpResponse("Email sent successfully...")

# List of menu's class
class MenuList(ListView):
	model= Menu
	template_name= "delivery_app/menu_list.html"
	def get_context_data(self, **kwargs):
		context = super(MenuList, self).get_context_data(**kwargs)
		return context

# Create a menu class
class MenuCreate(CreateView):
	model= Menu
	template_name= "delivery_app/menu_create.html"
	form_class= MenuForm
	success_url = '/delivery_app/menu/list/'
	
# Create an options of one menu class
class OptionsCreate(CreateView):
	model= Options
	template_name= "delivery_app/options_create.html"
	form_class= OptionsForm
	success_url = '/delivery_app/menu/create/'

# Create a request of menu class
class RequestCreate(CreateView):
	model= Request_menu
	template_name= "delivery_app/request_create.html"
	form_class= RequestForm
	success_url = '/delivery_app/menu/request/list'

# Editing an menu
class MenuUpdate(UpdateView):
    model = Menu
    template_name = 'delivery_app/menu_update.html'
    form_class = MenuForm
    success_url = '/delivery_app/menu/list/'

# index function
def index(request):
    return render(request, 'delivery_app/index.html')

# List of requests
class RequestList(ListView):
	model= Request_menu
	template_name= "delivery_app/request_list.html"

	# Filtering depending on which user is
	def get_queryset(self): 
		queryset = super(RequestList, self).get_queryset()
		if self.request.user.id==1:
			return Request_menu.objects.all()
		else:
			return Request_menu.objects.filter(user=self.request.user)

	def get_context_data(self, **kwargs):
		context = super(RequestList, self).get_context_data(**kwargs)
		return context

# Editing an request
class RequestUpdate(UpdateView):
    model = Request_menu
    template_name = 'delivery_app/request_update.html'
    form_class = RequestForm
    success_url = '/delivery_app/menu/list/'