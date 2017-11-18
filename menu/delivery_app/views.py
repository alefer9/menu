# -*- coding: utf-8 -*-
# future
from __future__ import unicode_literals

#Django
from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import redirect, render, render_to_response, HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse 
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

from .models import Menu, Menu_options, Options, Request_menu, User

from .forms import MenuForm, OptionsForm, RequestForm, UserForm

from .tasks import enviar_mail

def logout_view(request):
	if request.user.is_authenticated:
		logout(request)
		request.session.flush()
		return render(request,'delivery_app/login.html')

def login(request): # Login function
    username = request.POST.get('username')
    password = request.POST.get('password')
    next_page = request.GET.get('next')
    user = authenticate(username=username, 
    					password=password)
    if user is not None:
    	auth_login(request, user)
    	if user.role=='Administrator':
    		return render(request,'delivery_app/index.html')
    	else:
    		if user.role=='Employee':
    			return HttpResponseRedirect(reverse('request_list') )
    else:
		return render(request,'delivery_app/login.html')

def Send_menu(self, **kwargs): # Sending email function
	model= Menu
	users= User.objects.exclude(role='Administrator')

	
	pk = kwargs['pk'] # Getting a pk of the menu selected
	menu= Menu.objects.get(id=pk)

	"""
	Creating the message of menu

	"""
	description = 'Hola!\nDejo el menú de hoy :)\n\n'
	count = 1
	for menu in menu.options.all():
		description += 'Opcion '+str(count)+': '+str(menu)+'\n'
		count += 1
	description += 'Tengan lindo día!\n\n'
	description += 'Para ordenar algo del menu ingresa a este link: http://'+self.get_host()+''+reverse('menu_detail', kwargs={'pk':menu.id})

	"""
	Sending email to all of users (loop)

	"""
	for user in users:
		enviar_mail.delay("Cornershop menu of the day", 
						  description,
						  user.email) # Function to send email
	return HttpResponse("Email sent successfully...") 

class MenuList(ListView): # List of menu's class
	model= Menu
	template_name= "delivery_app/menu_list.html"
	context_object_name = 'object_list'
	
class MenuCreate(CreateView): # Create a menu class
	model= Menu
	template_name= "delivery_app/menu_create.html"
	form_class= MenuForm
	success_url = '/delivery_app/menu/list/'

class MenuDetailView(DetailView): # Menu detail view class
	model = Menu

	def get_context_data(self, **kwargs):
		context = super(MenuDetailView, self).get_context_data(**kwargs)
		return context

class MenuUpdate(UpdateView): # Editing an menu
    model = Menu
    template_name = 'delivery_app/menu_update.html'
    form_class = MenuForm
    success_url = '/delivery_app/menu/list/'
	
class OptionsCreate(CreateView): # Create an options of one menu class
	model= Options
	template_name= "delivery_app/options_create.html"
	form_class= OptionsForm
	success_url = '/delivery_app/menu/create/'

class RequestCreate(CreateView): # Create a request of menu class
	model= Request_menu
	template_name= "delivery_app/request_create.html"
	form_class= RequestForm
	success_url = '/delivery_app/menu/request/list'
	context_object_name = 'menu_request'

	"""
	Adding another object to context

	"""
	def get_context_data(self, **kwargs):
		context = super(RequestCreate, self).get_context_data(**kwargs)
		context['menu_options'] = Menu_options.objects.filter(menu=self.kwargs['pk'])
		return context

	"""
	Override the POST function

	"""
	def post(self, request, *args, **kwargs):
		menu_id = self.kwargs['pk']
		option_id = request.POST['option_id']
		customizations = request.POST['customizations']
		version = request.POST['version']
		option = Options.objects.get(pk=option_id)
		menu = Menu.objects.get(id=menu_id)
		user= self.request.user
		request_menu_save = Request_menu.objects.create(customizations = customizations,
										  				version = version,
										  				menu = menu,
										  				option = option,
										  				user = user)
		return HttpResponseRedirect(reverse('request_list') )

def index(request): # index function
    return render(request, 'delivery_app/index.html')

class RequestList(ListView): # List of requests
	model= Request_menu
	template_name= "delivery_app/request_list.html"

	"""
	Filtering depending on which user is

	"""
	def get_queryset(self): 
		queryset = super(RequestList, self).get_queryset()
		if self.request.user.role=='Administrator':
			return Request_menu.objects.all()
		else:
			return Request_menu.objects.filter(user=self.request.user)

	def get_context_data(self, **kwargs):
		context = super(RequestList, self).get_context_data(**kwargs)
		return context

class RequestUpdate(UpdateView): # Editing an request
    model = Request_menu
    template_name = 'delivery_app/request_update.html'
    form_class = RequestForm
    success_url = '/delivery_app/menu/list/'