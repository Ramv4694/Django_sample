# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.backends import ModelBackend
from django_auth_ldap.config import LDAPSearch
from django_auth_ldap.backend import LDAPBackend

from django.contrib.auth.models import User, Group, Permission


import pdb

# Create your views here.

def signin_view(request,backend='django.contrib.auth.backends.ModelBackend'):
     if request.method == 'POST':

         username = request.POST.get("UserName")
         password =  request.POST.get("password")
         auth = LDAPBackend()

         pdb.set_trace()

         user = auth.authenticate(username = username, password = password)


         if user is not None:
             last_login = user.last_login

             login(request, user,backend='django.contrib.auth.backends.ModelBackend')
             return redirect('/',{'name' : request.user.username,'last': request.user.last_login })
         else:
             return HttpResponse('login failed')

     return render(request,'accounts/login.html')

def logout_view(request):

    print("Logging users out")
    logout(request)

    return redirect('accounts:login')
