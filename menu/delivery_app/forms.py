from .models import Menu, Options, Request_menu
from django.forms import ModelForm
from django import forms

import datetime


class MenuForm (ModelForm):

	class Meta:
		model= Menu
	
		fields= [
			'description',
			'fecha',
			'options',
			
			]
		labels= {'description': 'description',
				 'fecha': 'fecha',
				 'options': 'Options',
				 }
		widgets={'description': forms.TextInput(attrs={'class':'form-control'}),
				 'fecha': forms.DateInput(attrs={'class':'form-control'}),
				 'options': forms.CheckboxSelectMultiple(),
				 }

class RequestForm(ModelForm):

	class Meta:
		model= Request_menu
	
		fields= [
			'customizations',
			'version',
			'menu',
			'user',
			]
		labels= {'customizations': 'Customizations',
				 'version': 'Version',
				 'menu': 'Menu',
				 'user': 'User'
				 }
		widgets={'customizations': forms.TextInput(attrs={'class':'form-control'}),
				 'version': forms.Select(attrs={'class':'form-control'}),
				 'menu': forms.Select(attrs={'class':'form-control'}),
				 'user':forms.Select(attrs={'class':'form-control'})
	
				 }


class OptionsForm (ModelForm):

	class Meta:
		model= Options
	
		fields= [
			'description',
			
			]
		labels= {'description': 'description',
				 
				 }
		widgets={'description': forms.TextInput(attrs={'class':'form-control'}),
	
				 }

	