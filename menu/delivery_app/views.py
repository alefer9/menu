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
# Create your views here.

def Send_menu(self, **kwargs):
	model= Menu
	users= User.objects.exclude(role='Administrator')
	pk = kwargs['pk']
	menu= Menu.objects.get(id=pk)
	description = 'Hola!\nDejo el menú de hoy :)\n\n'
	count = 1
	for menu in menu.options.all():
		description += 'Opcion '+str(count)+': '+str(menu)+'\n'
		count += 1
	description += 'Tengan lindo día!\n\n'
	description += 'Para ordenar algo del menu ingresa a este link: https://'+self.get_host()+''+reverse('request_create')
	for user in users:
		print(user.email)
		enviar_mail.delay("Cornershop menu of the day", description, user.email)
	return HttpResponse("Send Email")

class MenuList(ListView):
	model= Menu
	template_name= "delivery_app/menu_list.html"
	def get_context_data(self, **kwargs):
		context = super(MenuList, self).get_context_data(**kwargs)
		return context

class MenuCreate(CreateView):
	model= Menu
	template_name= "delivery_app/menu_create.html"
	form_class= MenuForm
	success_url = '/delivery_app/menu/list/'
	

class OptionsCreate(CreateView):

	model= Options
	template_name= "delivery_app/options_create.html"
	form_class= OptionsForm
	success_url = '/delivery_app/menu/create/'

class RequestCreate(CreateView):
	model= Request_menu
	template_name= "delivery_app/request_create.html"
	form_class= RequestForm
	success_url = '/delivery_app/menu/request/list'

class MenuUpdate(UpdateView):
    model = Menu
    template_name = 'delivery_app/menu_update.html'
    form_class = MenuForm
    success_url = '/delivery_app/menu/list/'

def index(request):
    return render(request, 'delivery_app/index.html')

class RequestList(ListView):
	model= Request_menu
	template_name= "delivery_app/request_list.html"
	def get_queryset(self): 
		queryset = super(RequestList, self).get_queryset()
		if self.request.user.id==1:
			return Request_menu.objects.all()
		else:
			return Request_menu.objects.filter(user=self.request.user)

	def get_context_data(self, **kwargs):
		context = super(RequestList, self).get_context_data(**kwargs)
		return context

class RequestUpdate(UpdateView):
    model = Request_menu
    template_name = 'delivery_app/request_update.html'
    form_class = RequestForm
    success_url = '/delivery_app/menu/list/'