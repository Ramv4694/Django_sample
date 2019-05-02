from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Masterlist,Network1,Network,Manual,Discarded
from django.http import JsonResponse
import datetime,json,os,platform,sys,json
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.views.generic import TemplateView
from django.core.serializers.json import DjangoJSONEncoder
from .forms import DiscardedForm

from django_datatables_server_side.views import DatatablesServerSideView
from djqscsv import render_to_csv_response
import datetime
import pdb
from django import forms

global Materlist
Materlist = Network1.objects.filter(barcode__in=Masterlist.objects.values('barcode'))

#Executes when the url for home is matched,comes from urls.py

@login_required(login_url="/accounts/login")
def home(request):
    #execute the following only if the request is of POST type
    if request.method == 'POST':
        #get all data into a variable 'data'
        data = request.POST['servers']
        #here data is in a single string,we need to seperate the server names and add to a list
        #declare an empty string to store name of each server
        s=""

        #declare an empty list to add name of each server
        l=[]

        #here i is each character in data
        for i in data:
            #if \n is found, then it is end of a string,so we add that name to list and make the string empty for reading the next charaters as a neew string
            if(i=="\n"):
                l.append(s)
                s=""

            #if i is not \n then append that charcter to a string
            s+=i

        #the last string is not appended as the last server name has no \n ,so we add it manually.
        l.append(s)

        #empty list to store pingable servers
        pingable=[]
        for i in l:
            #if the server is pingable,append it to list
            if check_ping(i):
                pingable.append(i)

            #otherwise check the next server in the list.
            else:
                continue



        return HttpResponse(pingable)
    return render(request,'index.html')



@login_required(login_url="/accounts/login")
def report(request):

    #Materlist is the list of all tapes which are both in networker dump and in master list provided.
    #Here, we are filtering all the networker objectcs whose barcode is in masterlist provided.
    global Materlist
    Materlist = Network1.objects.filter(barcode__in=Masterlist.objects.values('barcode'))
    #counting the no of tapes found in networker dump and masterlist.i.e.,Materlist
    Materlistcount = Materlist.count()



    #counting no of tapes in materlist whose volume retention is marked as expired
    expiredcount = Materlist.filter(volret='expired').count()

    #counting no of tapes in materlist whose volume retention is marked as a particular date.
    # ^\d{1|2}\/\d{1|2}\/\d{1|2|3|4}$ is the regular expression for the format in which date is present in the networker dump
    Datecount = Materlist.filter(volret__iregex='^\d{1|2}\/\d{1|2}\/\d{1|2|3|4}$').count()

    #counting no of tapes in materlist whose volume retention is marked as manual
    manualcount = Materlist.filter(volret='manual').count()

    #counting no of tapes in materlist whose volume retention is marked as undef
    undefcount = Materlist.filter(volret='undef').count()

    #The unidentified tapes are the tapes which are not present networker dump but in the provided masterlist
    #Here,we are excluding the tapes from masterlist which are not in the materlist(matched list)
    Unidentifiedcount = Masterlist.objects.exclude(barcode__in=Materlist.values('barcode')).count()

    #Note:In the materlist(includes expiredcount,Datecount,manualcount as well as undefcount), barcodes of all the tapes may not be unique as there are tapes with some additional data represented again using the same barcode
    #So, there might be some inconsistency regarding the count.



    # Servers = Materlist.values_list('ip').distinct()
    # s = []
    # for i in Servers:
    #     for j in i:
    #         s.append(str(j))
    #
    # sc=[]
    # for i in s:
    #     sc.append(Materlist.filter(ip=i).count())
    hop2 = Materlist.filter(ip="Lgtohop2").count()
    hop3 = Materlist.filter(ip="Lgtohop3").count()
    webo2 = Materlist.filter(ip="Lgtowebo2").count()
    webo3 = Materlist.filter(ip="Lgtowebo3").count()
    webo4 = Materlist.filter(ip="Lgtowebo4").count()



    return render(request,'temp.html',{'Materlist':Materlist,'Expired':expiredcount, 'Manual':manualcount, 'Netdate':Datecount, 'Undef':undefcount,'Unidentified':Unidentifiedcount,'hop2':hop2,'hop3':hop3,'webo2':webo2,'webo3':webo3,'webo4':webo4})

@login_required(login_url="/accounts/login")
def Discard(request):
    if request.method =='POST':

        form = DiscardedForm(request.POST)
        if form.is_valid():
            Bar= request.POST.get('comment','')
            SplitBar = Bar.split()

            for Split in SplitBar:


                Discarded_obj = Discarded(Barcode = Split)
                Discarded_obj.save()
            DiscardedBarcode =  Discarded.objects.all().values_list('Barcode',flat=True)
            cursor = connection.cursor()
            cursor.execute("select * FROM NETWORK1 INNER JOIN Discard WHERE NETWORK1.BARCODE = Discard.Barcode")

            global rowcount
            rowcount = cursor.fetchall()



            print(rowcount)

            #pdb.set_trace()

             # form.save() saves the model to the database
             # form.save does only work on modelforms, not on regular forms
             #form.save()
    else:
        form = DiscardedForm()

    return render(request,'Discarded.html',{'Test':rowcount})

@login_required(login_url="/accounts/login")
def type_details(request,type):
    #getting the list of matched tapes which are in networker dump as well as masterlist
    #Here, we are filtering all the networker objectcs whose barcode is in masterlist provided.

    if type=='Unidentified':
        return render(request,'unidentified.html',{'type':type})

    elif type=='netdate':
        return render(request,'detailed_report.html',{'type':type})

    elif type=='expired':
        #if the type of selected list is either expired,manual or undef, the same query can be used just by using the type variable directly by filtering the materlist
        final_list = Materlist.filter(volret=type).distinct()
        #Now,we are sending the list, type to the template to render them properly.
        return render(request,'detailed_report.html',{'type':type})

    elif type=='manual':
        #if the tapes with dates are selected,we'll find the list of those tapes by filtering the materlist
        final_list = Materlist.filter(volret__iregex='^\d{1|2}\/\d{1|2}\/\d{1|2|3|4}$')
        #Now,we are sending the list, type to the template to render them properly.
        return render(request,'detailed_report.html',{'type':type})

    elif type=='undef':
        #if the tapes with dates are selected,we'll find the list of those tapes by filtering the materlist
        final_list = Materlist.filter(volret__iregex='^\d{1|2}\/\d{1|2}\/\d{1|2|3|4}$')
        #Now,we are sending the list, type to the template to render them properly.
        return render(request,'detailed_report.html',{'type':type})




def check(request):
    return HttpResponse("This page is not yet ready!")


#method to check if server is pingable3
def check_ping(hostname):

    try:
        plat = platform.system()
        server = hostname.strip()
        if plat=="Windows":
            response = os.system("ping -n 1 %s" % server)
        elif plat=="Linux":
            response = os.system("ping -c 1 %s" % server)
        else:
            response = 1
    except:
        response = 1
    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False

    return pingstatus



def download_csv(request,type):
    if type=="expired":
        qs = Materlist.filter(volret='expired').distinct()
    elif type=="undef":
        qs = Materlist.filter(volret='undef').distinct()
    elif type=="manual":
        qs = Materlist.filter(volret='manual').distinct()
    elif type=="netdate":
        qs = Materlist.filter(volret__iregex='^\d{1|2}\/\d{1|2}\/\d{1|2|3|4}$')
    elif type=="matched":
        qs= Materlist.values('barcode', 'volret', 'state', 'flags', 'capacity','typefull','ip')
    elif type=="manual_saveset":
        qs = Manual.objects.all()
    else:
        qs = Masterlist.objects.exclude(barcode__in=Materlist.values('barcode')).values('barcode')
    return render_to_csv_response(qs)





class UnidentifiedDatatableView(DatatablesServerSideView):
	model = Masterlist
	columns =  ['barcode']
	searchable_columns =  ['barcode']

	def get_initial_queryset(self):
		return Masterlist.objects.exclude(barcode__in=Materlist.values('barcode'))

class ManualSavesetDatatableView(DatatablesServerSideView):
	model = Manual
	columns = ['barcode', 'volret', 'state', 'flags', 'capacity','typefull','ip','name','clretent']
	searchable_columns =  ['barcode', 'volret', 'state', 'flags', 'capacity','typefull','ip','name','clretent']

	def get_initial_queryset(self):
		return Manual.objects.all()


class MulDatatableView(DatatablesServerSideView):


    model = Network1
    columns =  ['barcode', 'volret', 'state', 'flags', 'capacity','typefull','ip']
    searchable_columns =  ['barcode', 'volret', 'state', 'flags', 'capacity','typefull','ip']

    def get_initial_queryset(self,*args,**kwargs):
        type = self.kwargs['type']
        if type=="netdate":
            return Materlist.filter(volret__iregex='^\d{1|2}\/\d{1|2}\/\d{1|2|3|4}$')
        elif type=="matched":
            return Materlist
        return Materlist.filter(volret=type).distinct()

@login_required(login_url="/accounts/login")
def manual_saveset(request):
    return render(request,'manual_saveset.html')
