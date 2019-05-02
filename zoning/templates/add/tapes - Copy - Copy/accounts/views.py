# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
import pdb

# Create your views here.

def signin_view(request):
     if request.method == 'POST':

         username = request.POST.get("UserName")
         password =  request.POST.get("password")

         #pdb.set_trace()

         user = authenticate(username = username, password = password)

         if user is not None:

             login(request, user)
             return redirect('/',{'name' : request.user.username })
         else:
             return HttpResponse('login failed')

     return render(request,'accounts/login.html')

def logout_view(request):

    print("Logging users out")
    logout(request)

    return redirect('accounts:login')
