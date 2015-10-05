from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import *
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from myproject.views import *
from django.forms.fields import CheckboxInput

handler404 = 'myproject.views.error404'

urlpatterns = patterns('',
	url(r'^$', inici),
	url(r'^afegir$', afegir),
	url(r'^afegirInputs$', afegirInputs),
	url(r'^afegirFormula$', afegirFormula),
	url(r'^reinicia$', reinicia),
	url(r'^funcionament$', funcionament),
	url(r'^inici$', inici),
	url(r'^graf$', graf),
	url(r'^quisom$', quisom),
    url(r'^error404/$', error404),
)

