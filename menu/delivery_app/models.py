# -*- coding: utf-8 -*-
# future
from __future__ import unicode_literals

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import signals

class User(AbstractUser): # User model
	EMPLOYEE= 'Employee'
	ADMINISTRATOR = 'Administrator'
	ROLE_CHOICES = (
		(EMPLOYEE, 'Employee'),
		(ADMINISTRATOR, 'Administrator'),
	)

	rut = models.IntegerField(unique=True, null=True)
	address = models.CharField(max_length=45, null=True)
	cellphone = models.CharField(max_length=45, null=True, blank=True)
	role = models.CharField(max_length=30,choices=ROLE_CHOICES)
	
	class Meta:
		db_table = 'auth_user'

class Options (models.Model): # Options of menu model
	description=models.CharField(max_length=255)
	
	def __unicode__(self):
		return '%s' % (self.description)

class Menu (models.Model): # Menu Model
	description=models.CharField(max_length=255)
	date= models.DateField(max_length=45, null=True, blank=True)
	options= models.ManyToManyField(Options, through='Menu_options', related_name='%(class)s_requests_created')
	
	def __unicode__(self):
		return '%s %s' % (self.description, self.options)

class Menu_options (models.Model): # Menu options ManyToMany relationship Model
	menu = models.ForeignKey(Menu, related_name='menu')
	options =models.ForeignKey(Options,related_name='options')
	
	class Meta:
		auto_created = True
	
	def __unicode__(self):
		return '%s %s' % (self.menu, self.options)

class Request_menu (models.Model): # Request of menu Model
	normal= 'Normal'
	extralarge= 'extralarge'
	VERSION_CHOICES = (
		(normal, 'Normal'),
		(extralarge, 'Extralarge'),
	)
	customizations = models.CharField(max_length=255)
	version= models.CharField(max_length=30,choices=VERSION_CHOICES)
	menu = models.ForeignKey(Menu)
	option = models.ForeignKey(Options,related_name='option')
	user= models.ForeignKey(User)

	def __unicode__(self):
		return '%s %s %s %s' % (self.customizations, self.version, self.menu, self.option, self.user)