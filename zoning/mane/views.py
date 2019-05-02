# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import *
from django.db.models import Q
from io import StringIO
import pymysql
import json
from datetime import datetime, timedelta

# Create your views here.
@login_required(login_url="/accounts/login")
def landing(request, template_name='mane/landing.html'):
    return render(request, template_name)
