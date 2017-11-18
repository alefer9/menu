#Django
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


from .views import MenuList, Send_menu, RequestList,RequestUpdate, RequestCreate, MenuCreate, MenuUpdate, MenuDetailView, index, OptionsCreate

# All url to use 
urlpatterns = [
   url(r'^send/menu/(?P<pk>[\w-]+)$', Send_menu, name= 'send_menu'),
   url(r'^menu/list', MenuList.as_view(), name= "menu_list"),
   url(r'^menu/create', MenuCreate.as_view(), name= "menu_create"),
   url(r'^menu/view/(?P<pk>[\w-]+)$', MenuDetailView.as_view(), name= "menu_detail"),
   url(r'^options/create', OptionsCreate.as_view(), name= "options_create"),
   url(r'^menu/request/create/(?P<pk>[\w-]+)$', RequestCreate.as_view(), name= "request_create"),
   url(r'^menu/request/list', RequestList.as_view(), name= "request_list"),
   url(r'^menu/request/update/(?P<pk>[\w-]+)$', RequestUpdate.as_view(), name= "request_update"),
   url(r'^menu/update/(?P<pk>[\w-]+)$', MenuUpdate.as_view(), name= "menu_update"),
   url(r'^menu', index, name= 'admin_inicio'),
]