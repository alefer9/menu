
from .models import Menu, Options, Request_menu, User

# Django
from django.forms import ModelForm
from django import forms

# standard library
import datetime

class UserForm (ModelForm):
	class Meta:
		model= User	
		fields= ['username',
				 'password',			
				]
		labels= {'username': 'Username',
				 'password': 'Password',
				 }
		widgets={'username': forms.TextInput(attrs={'class':'form-control'}),
				 'password': forms.TextInput(attrs={'class':'form-control'}),
				 }



class MenuForm (ModelForm): # Menu form with all options and widgets
	class Meta: 
		model= Menu
		fields= ['description',
				 'date',
				 'options',
				]
		labels= {'description': 'description',
				 'date': 'Date',
				 'options': 'Options',
				 }
		widgets={'description': forms.TextInput(attrs={'class':'form-control'}),
				 'date': forms.DateInput(attrs={'class':'form-control'}),
				 'options': forms.CheckboxSelectMultiple(),
				 }


class RequestForm(ModelForm): # Request form with all options and widgets
	class Meta:
		model= Request_menu
		exclude =["user",
				  "menu",
				  "option",
				]
		labels= {'customizations': 'Customizations',
				 'version': 'Version'
				}
		widgets={'customizations': forms.TextInput(attrs={'class':'form-control'}),
				 'version': forms.Select(attrs={'class':'form-control'}),
				 'menu': forms.Select(attrs={'class':'form-control'}),
				}


class OptionsForm (ModelForm): # Options form with all widgets
	class Meta:
		model= Options
	
		fields= ['description',
				]
		labels= {'description': 'description',
				}
		widgets={'description': forms.TextInput(attrs={'class':'form-control'}),
				}

	