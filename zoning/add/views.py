# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import re
import string
from itertools import chain
import json, ast

from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from add.models import zonegroup,Arraygroup,Hostgroup


from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.db import connection

import time
import pdb

import paramiko
# Create your views here.
global Fabric





#@login_required(login_url="/accounts/login")
def storage_group(request):
    logger.info("user logged in")

    return render(request,'add/addzone1.html')

#
#@login_required(login_url="/accounts/login")
def storage_add(request):

    if request.method == 'POST':

        print("Inside post operation")
        #formvalue = addstoragegroup(LunCapacity=request.POST.get("LunCapacity"),NoofLuns=request.POST.get("NoofLuns"),ClusterName=request.POST.get("Cluster"),DirectorId=request.POST.get("DirectorId"),PortId=request.POST.get("PortId"),Initiator=request.POST.get("Initiators"))

        #formvalue = zonegroup(Location=request.POST.get('textaux'),Class=request.POST.get('textaux1'),Switch=request.POST.get('textaux2'))

        Fabric = []

        FabricName = []

        ArrayName =[]


        Location = request.POST.get('textaux')

        Class = request.POST.get('textaux1')

        Switch = request.POST.get('textaux2')

        input_names = [name for name in request.POST.keys() if name.startswith('name')]



        soft_name = []

        host_name_details = []

        clustername = []



        for input_name in input_names:
            soft_name = request.POST.get(input_name)

            HostName = Hostgroup.objects.values_list('HostName','FabricName','Class','Wwn','Vsan').filter(Q(HostName__contains=soft_name))

            host_name_details.append(HostName)



        print(host_name_details)
        #######pdb.set_trace()
        if len(host_name_details) == 1:

            host_details = host_name_details[0]

        else:
            host_details = host_name_details

        hostlength = len(host_name_details)

        #######pdb.set_trace()

        for host in host_details:

            print(host[0])

        FabricName = zonegroup.objects.values_list('FabricName').filter(Q(Location=Location) & Q(Class=Class))
        FabricNamedict = zonegroup.objects.filter(Q(Location=Location) & Q(Class=Class)).values('FabricName')
        finalfabriclist = list(FabricNamedict)
        finalfabric = [{k.encode("utf-8"): v.encode("utf-8") for k, v in elem.items()} for elem in finalfabriclist]

        ArrayName = Arraygroup.objects.values_list('Array').filter(Q(Location=Location) & Q(Class=Class))
        #######pdb.set_trace()
        Arraynamedict = Arraygroup.objects.filter(Q(Location=Location) & Q(Class=Class)).values('Array')
        Arraynamedictlist = list(Arraynamedict)
        finalArray = [{k.encode("utf-8"): v.encode("utf-8") for k, v in elem.items()} for elem in Arraynamedictlist]


        print(Location)


        Fabric = zonegroup.objects.values_list('FabricName','FabricA','FabricB').filter(Q(Location=Location) & Q(Class=Class))

        print("About to go to next page")


        print(Fabric)


    #return render(request,'add/tables.html')
    return render(request,'add/Fabric.html',{'Fabric':FabricName,'finalfabric':finalfabric,'finalArray':finalArray,'Array':ArrayName,'Hostnames':host_details,'hostlength':hostlength})


#@login_required(login_url="/accounts/login")
def Array_ports(request):

    if request.method == 'POST':

        global switchdetails

        switch = request.POST['Fabricrec']

        bc = switch.encode('utf-8')

        #mb = re.search(r"('.*')",bc)
        ##pdb.set_trace()

        #word = mb.group(0)

        #word1 = re.search(r"([a-z]|[A-z].*')",word)

        #fswitch = word1.group(0)

        finalswitch =  bc

        cursor1 = connection.cursor()
        cursor1.execute("SELECT FabricA, FabricB FROM add_zonegroup WHERE FabricName = %s",(finalswitch,))

        global switchrow

        switchrow = cursor1.fetchall()

        Arraydetail = request.POST['Arrayrec']

        Array_Name = re.findall('\d+', Arraydetail)

        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT Array,FaPort,identifier,FaPortg FROM zoningReport WHERE Array = %s", (Array_Name,))
        row = cursor.fetchall()
        ######pdb.set_trace()
        print(row)
        ##pdb.set_trace()

    return render(request,'add/ports.html',{'FaPorts':row,'Switch':switchrow})

#@login_required(login_url="/accounts/login")

def Ajax_call(request):
    if request.method == 'POST':

        print("Hello from Ajax")
        global amount,data1
        amount = request.POST.get('cart')

        data1 = json.loads(amount)

        print(amount)

    return HttpResponse("hello")

@login_required(login_url="/accounts/login")
def Ajax_class(request):

    if request.method == 'POST':
        global amount1
        global data

        print("Hello from Ajax1")
        amount1 = request.POST.get('cart1')

        data = json.loads(amount1)
    return HttpResponse("hello from Ajax_class")



#@login_required(login_url="/accounts/login")
def Array_seg(request):
    if request.method == 'POST':
        k = [] #switches of a class
        j = [] ##switches of b class

        for d in data:
            for d1 in data1:

                dclass = d["Js_class"]
                d1class= d1["Js_Class"]

                if(dclass == d1class):


                    if(dclass == 'A'):
                        newdict = dict(chain.from_iterable(k.items() for k in (d,d1)))
                        k.append(newdict)

                    elif(dclass == 'B'):
                        newdict1 = dict(chain.from_iterable(j.items() for j in (d,d1)))
                        j.append(newdict1)
                    request.session['sesa'] = k
                    request.session['sesb']= j

        print(j)


        ##pdb.set_trace()
    return render(request, 'add/final.html', {'sahs':k,'sbhs':j,'sesa':k,'sesb':j})

#@login_required(login_url="/accounts/login")
def storage_validation(request,**kwargs):


    switchusername = request.POST.get('username')
    switchpassword = request.POST.get('password')
    request.session['switchusername'] = switchusername
    request.session['switchpassword'] = switchpassword
    ###pdb.set_trace()

    ###get data from previous session

    sesadata = request.session.get('sesa')
    sesbdata = request.session.get('sesb')
    ##pdb.set_trace()

    switchlist=[sesadata,sesbdata]
    request.session['switchlist'] = switchlist
    currenttime = datetime.now().strftime("%Y_%m_%d")



    ##pdb.set_trace()
    print(switchlist)
    ValidationResult =[]

    for switchl in switchlist:
        for switch in switchl:
            result = {}

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            channel_data = str()
            fa_data = str()
            sshconnection = ""

            UVSwitch = switch['Js_Switch']
            Switchname = ast.literal_eval(json.dumps(UVSwitch))
            result['switchname'] = Switchname
            print("The current switch is ",Switchname)

            ###connect to ssh

            try:
                ssh.connect(Switchname, port=22, username=switchusername ,password=switchpassword)
                print("Successfully connected to ")
                sshconnection = "Success"
            except:
                ###if not logged in "
                print("Authentication error")
            if sshconnection == "Success":



                channel = ssh.invoke_shell()
                ####pdb.set_trace()

                print "Looping"
                time.sleep(5)

                if channel.recv_ready():

                    time.sleep(2)
                    channel_data += channel.recv(9999)
                    print '####Device Output#####'
                    print channel_data
                    ####pdb.set_trace()
                    if("#" in channel_data):

                    #if (Switchname+"#" in channel_data):

                        UVsanNo = switch['Js_VSan']
                        RVsanNo = ast.literal_eval(json.dumps(UVsanNo))

                        ###Get only VSAN NO
                        all=string.maketrans('','')
                        nodigs=all.translate(all, string.digits)
                        VsanNo = RVsanNo.translate(all, nodigs)

                        ##Pass VsanNo variable to command
                        print("Ready to execute commands")

                        Vsancommand = "show zoneset active vsan" + " " + VsanNo



                        ####Check for VSAN NO

                        channel.send('terminal length 0')

                        channel.send('\n')

                        time.sleep(2)

                        channel_data += channel.recv(9999)

                        channel.send(Vsancommand)

                        channel.send('\n')

                        time.sleep(2)

                        print("Checkng channel status")


                        while channel.recv_ready() == True:

                            print("reading please wait")
                            channel_data += channel.recv(9999)

                            if(channel_data.endswith('')):

                                print("CLOSING THE OPERATION")

                        ####pdb.set_trace()

                        ###Proceed only if VSAN is present

                        if("zoneset name" in channel_data):

                            mg = re.findall('zoneset name.*', channel_data)



                            result['vsan'] = mg[0] + " " ' is Configured'
                            zonesetregex = "name[\s\S]*?vsan"
                            zoneset = re.findall(zonesetregex,mg[0])
                            zonesetrvsan = zoneset[0].replace("vsan","")
                            zonesetrname = zonesetrvsan.replace("name","")
                            finalzoneset_name = zonesetrname.lstrip()
                            finalzonesetname = finalzoneset_name.rstrip()
                            result['zoneset'] = finalzonesetname





                            print("VSAN IS PRESENT HENCE CONTINUING WITH THE OPERATION")

                            ###Checking Host WWN 20:00:00:25:B5:28:00:DE

                            Hostwwnraw = switch['Js_Wwn']

                            Hostwwn = ast.literal_eval(json.dumps(Hostwwnraw))

                            hostwwncommand = "show flogi database | grep -i" + " " + Hostwwn

                            if channel.send_ready():

                                channel.send(hostwwncommand)

                                channel.send('\n')
                                time.sleep(2)
                                print("checking hostwwn")

                                while channel.recv_ready() == True:
                                    print("reading hostwwn please wait")
                                    channel_data += channel.recv(9999)
                                    if(channel_data.endswith('')):
                                        print("CLOSING THE OPERATION")

                            else:
                                print("chhannel not ready")
                                time.sleep(4)
                                channel_data = channel.recv(9999)
                                ####pdb.set_trace()


                            if("port-channel" in channel_data):

                                print("Host wwn is logged in")



                                hostzonesetdetails = re.findall("port-channel.*",channel_data)
                                hostvsan=hostzonesetdetails[0].split()[1]

                                portchanneldetails = re.findall("(port-channel)\w+",channel_data)

                                if(VsanNo == hostvsan):
                                    portchanneldetails = re.findall("(port-channel\w+)",channel_data)
                                    ###pdb.set_trace()

                                    ###add portchanneldetails
                                    result['hostwwn'] = Hostwwn + " is logged in and connected to " + "" + portchanneldetails[0]
                                else:
                                    result['hostwwn'] = Hostwwn + "is logged in but does not match VSAN"




                            else:
                                print("Host wwn is not logged in, do you still want to proceed")

                                result['hostwwn'] = Hostwwn + " is not logged in"


                            ##Check Array WN

                            Array_wwn = switch['Js_WWN'] ##without :

                            Arraywwn = ':'.join(a+b for a,b in zip(Array_wwn[::2], Array_wwn[1::2]))

                            Arraywwncmd = "show flogi database | grep -i" + " " + Arraywwn

                            ##since regex cannot accept | i m adding

                            Arraywwncmdregex ="show flogi database \| grep -i" + " " + Arraywwn

                            channel.send(Arraywwncmd)
                            channel.send('\n')
                            time.sleep(2)
                            channel_data += channel.recv(9999)

                            ##Regex to pull array Details
                            arrayregex = Arraywwncmdregex+"[\s\S]*?#"

                            arrayfacmd = re.findall(arrayregex,channel_data)
                            ####pdb.set_trace()

                            if("fc" in arrayfacmd[0]):

                                print("Fa wwn is logged in")

                                arrayzonesetdetails = re.findall("fc.*",arrayfacmd[0])
                                ####pdb.set_trace()
                                arrayvsan=arrayzonesetdetails[0].split()[1]
                                if(VsanNo == arrayvsan):
                                    ##add fc port details
                                    result['arraywwn'] = Arraywwn + " is logged in and matches with VSAN"

                                else:
                                    result['arraywwn'] = Arraywwn + "is logged in but does not match VSAN"###give what vsan is connected




                            else:

                                print("Fa wwn not logged in ")

                                result['arraywwn'] = Arraywwn + " is not logged in"

                            ####Now Check for Host Alias
                            #20:00:00:25:B5:28:00:DE

                            HostZoneset = "show zone member pwwn "  + ""+  Hostwwn
                            channel.send(HostZoneset)
                            channel.send('\n')
                            time.sleep(2)
                            channel_data += channel.recv(1024)

                            ##get zone set details
                            hostzonesetregex =  "# show zone member pwwn "  + ""+  Hostwwn

                            hostzonesetdetails = re.findall(hostzonesetregex + "[\s\S]*?#",channel_data)
                            ##pdb.set_trace()

                            ###Cchecking if the list is empty as the regex return array

                            if not hostzonesetdetails:
                                result['hostzoneset'] = Hostwwn + " is not a part of active zoneset"
                            else:

                                for hostzonesetdetail in hostzonesetdetails:
                                    if("vsan" not in hostzonesetdetail):

                                        print("Host Zoneset is not present")


                                        result['hostzoneset'] = Hostwwn + " is not part of an active zone"

                                    else:

                                        print("Host zoneset is present")

                                        ###  show zoneset active vsan 800 | grep -i DUGRC1esx1

                                        ## check pwwn matches and print the zone name

                                        result['hostzoneset'] = Hostwwn + " is a part of active zoneset"

                                ####Now check Array Zoneset

                            ArrayZoneset = "show zone member pwwn  "+ ""+  Arraywwn
                            Arrayzonecmdregex ="show zone member pwwn  "+ ""+  Arraywwn

                            channel.send(ArrayZoneset)

                            channel.send("\n")
                            time.sleep(2)


                            while channel.recv_ready() == True:
                                print("reading hostwwn please wait")
                                channel_data += channel.recv(9999)
                                if(channel_data.endswith('')):
                                    print("CLOSING THE OPERATION")

                            arrayzonesetdetails = re.findall(Arrayzonecmdregex + "[\s\S]*?#",channel_data)


                            ###pdb.set_trace()

                            #arrayzonesetdetail = arrayzonesetdetails[1]

                            if not arrayzonesetdetails:
                                result['arrayzoneset'] = "FA PORT WWN" + " " +Arraywwn+ " is not part of an active zone"
                            else:

                                for arrayzonesetdetail in arrayzonesetdetails:
                                    if("zone" in arrayzonesetdetail):
                                        print("FA PORT is a part of Active Zoneset")

                                        result['arrayzoneset'] = Arraywwn + "is a part of active zoneset"

                                    else:
                                        result['arrayzoneset'] = "FA PORT WWN" + " " +Arraywwn+ " is not part of an active zone"


                            ###now finally checking for host alias
                            HostZoneset = "show device-alias database | grep -i" + " "+  Hostwwn
                            channel.send(HostZoneset )
                            channel.send('\n')
                            time.sleep(4)
                            channel_data += channel.recv(1024)
                            ###pdb.set_trace()

                            hostaliasregex = "show device-alias database \| grep -i "
                            hostaliasvalue = re.findall(hostaliasregex + '[\s\S]*?pwwn',channel_data)

                            ###pdb.set_trace()
                            if(hostaliasvalue):
                                if("name" in hostaliasvalue[0]):

                                    print("Host Alias is present")
                                    m = re.findall('device-alias name[\s\S]*?pwwn',channel_data)
                                    ###pdb.set_trace()
                                    m1 = m[0].replace("pwwn", "")
                                    result['hostalias'] =  m1

                            else:
                                print("Host Alias is absent")
                                result['hostalias'] = Hostwwn + " Alias is not present"

                            ### now finally check for array Alias
                            ArrayZoneset = "show device-alias database | grep -i" + " "+  Arraywwn

                            channel.send(ArrayZoneset)
                            channel.send('\n')
                            time.sleep(2)
                            channel_data += channel.recv(9999)
                            #arrayaliasregex = "show device-alias database \| grep -i " + Arraywwn
                            arrayaliasvalues = re.findall('show device-alias database \| grep -i[\s\S]*pwwn',channel_data)
                            ####pdb.set_trace()
                            if not arrayaliasvalues:
                                result['arrayalias'] = Arraywwn + "Alias is not present"
                            else:
                                for arrayaliasvalue in arrayaliasvalues:


                                    if("VMAX" in arrayaliasvalue or "vmax" in arrayaliasvalue):
                                        print("array Alias is present")
                                        m1 = re.findall('device-alias name[\s\S]*?pwwn', arrayaliasvalue)

                                        if(len(m1) > 1):
                                            result['arrayalias'] =  m1[1]
                                        else:
                                            result['arrayalias'] =  m1[0]

                                    else:
                                        print("array Alias is not present")
                                        result['arrayalias'] = Arraywwn + "Alias is not present"
                            ##Taking Backup
                            backupcmd = 'copy running-config ftp://10.146.84.98/'+"app"+""+ Switchname+currenttime
                            channel.send(backupcmd)
                            channel.send('\n')
                            time.sleep(2)
                            while channel.recv_ready() == True:

                                print("reading please wait")
                                channel_data += channel.recv(9999)

                                if(channel_data.endswith('')):

                                    print("CLOSING THE OPERATION")
                            if 'username' in channel_data:
                            #pdb.set_trace()
                                channel.send('venkar2')
                                channel.send('\n')
                                time.sleep(2)
                                while channel.recv_ready() == True:

                                    print("reading please wait")
                                    channel_data += channel.recv(9999)

                                    if(channel_data.endswith('')):
                                        print("CLOSING THE OPERATION")
                                        #pdb.set_trace()
                            if 'password' or 'Password' in channel_data:

                                #pdb.set_trace()
                                channel.send('Chel$eaChel$ea@33')
                                channel.send('\n')
                                time.sleep(2)
                                while channel.recv_ready() == True:

                                    print("reading please wait")
                                    channel_data += channel.recv(9999)
                                if("complete" in channel_data):


                                    print("file copied")
                                    result['backupfile'] ="Backup Taken"

                                else:

                                    print("Failed to copy")
                                    result['backupfile'] ="Backup not Taken"


                        else:
                            print("VSAN IS ABSENT")

                            result['vsan'] = "VSAN IS ABSENT"
                            result['zoneset'] = "VSAN IS ABSENT"
                            result['hostwwn'] = "VSAN IS ABSENT"
                            result['arraywwn'] = "VSAN IS ABSENT"
                            result['hostzoneset'] = "VSAN IS ABSENT"
                            result['arrayzoneset'] = "VSAN IS ABSENT"
                            result['hostalias'] = "VSAN IS ABSENT"
                            result['arrayalias'] = "VSAN IS ABSENT"
                            result['backupfile'] ="VSAN IS ABSENT"
                else:
                    print("channel not ready")




            else:
                print("ssh connection failed")
                result['vsan'] = "Authentication error"
                result['zoneset'] = "VSAN IS ABSENT"
                result['hostwwn'] = "Authentication error"
                result['arraywwn'] = "Authentication error"
                result['hostzoneset'] = "Authentication error"
                result['arrayzoneset'] = "Authentication error"
                result['hostalias'] = "Authentication error"
                result['arrayalias'] = "Authentication error"
                result['backupfile'] ="Authentication error"

            ValidationResult.append(result)
            ####pdb.set_trace()
            print(ValidationResult)


        ####pdb.set_trace()


    return render(request,'add/validation.html',{'result':ValidationResult,'switchusername':switchusername,'switchpassword':switchpassword})

#@login_required(login_url="/accounts/login")
def storage_Ajaxprocess(request):

    if request.method == 'POST':


        print("Hello from Validation Ajax call")
        validation_report = request.POST.get('validcart')

        datavalidation_report = json.loads(validation_report)
        print(datavalidation_report)
        request.session['datavalidation_report'] = datavalidation_report


    return HttpResponse(datavalidation_report)

#@login_required(login_url="/accounts/login")
def storage_process(request):



    print "All Zoning details"


    ###get data from previous session

    #request.session.get('sesa')
    datavalidation_report = request.session.get('datavalidation_report')
    switchlist = request.session.get('switchlist')
    switchusername = request.session.get('switchusername')
    switchpassword = request.session.get('switchpassword')
    print(switchlist)
    print(datavalidation_report)
    pdb.set_trace()


    print(switchlist)
    ValidationResult =[]
    counter = 0

    for switch1 in switchlist:

        for switch in switch1:
            result = {}



            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            channel_data = str()
            fa_data = str()
            sshconnection = ""
            pdb.set_trace()
            currentdata = datavalidation_report[counter]

            UVsanNo = switch['Js_VSan']
            RVsanNo = ast.literal_eval(json.dumps(UVsanNo))

            ###Get only VSAN NO
            all=string.maketrans('','')
            nodigs=all.translate(all, string.digits)
            VsanNo = RVsanNo.translate(all, nodigs)


            UVSwitch = switch['Js_Switch']
            Switchname = ast.literal_eval(json.dumps(UVSwitch))
            Switchusername = ast.literal_eval(json.dumps(switchusername))
            Switchpassword = ast.literal_eval(json.dumps(switchpassword))
            Faport = switch['Js_FAPort']
            Faportname =  ast.literal_eval(json.dumps(Faport))

            Hostname = switch['Js_Hostname']
            Hostname =ast.literal_eval(json.dumps(Hostname))
            Arrayname = switch['Js_Arrayname']
            Arrayname =ast.literal_eval(json.dumps(Arrayname))
            lastArray = Arrayname[-4:]
            pdb.set_trace()

            Vhbano = switch['Js_Fabricname']
            Vhbano =ast.literal_eval(json.dumps(Vhbano))
            Arraywwn1 = switch['Js_WWN']
            Arrayww = ast.literal_eval(json.dumps(Arraywwn1))
            Arraywwn = ':'.join(a+b for a,b in zip(Arrayww[::2], Arrayww[1::2]))

            HostZonewwn = switch['Js_Wwn']
            Hostwwn =ast.literal_eval(json.dumps(HostZonewwn))
            HostZonestatus =datavalidation_report[counter]['zoneset_status']
            Checklist = datavalidation_report[counter]['checked']

            Zoneset =ast.literal_eval(json.dumps(HostZonestatus))

            counter = counter+1
            print(counter)
            Zoneresult = {}



            print("The current switch is ",Switchname)

            ###connect to ssh


            if(Checklist == True):
                print("Inside True statement")


                try:
                    ssh.connect(Switchname, port=22, username=switchusername ,password=switchpassword)
                    print("Successfully connected to ")
                    sshconnection = "Success"
                except:
                    ###if not logged in "
                    print("Authentication error")
                if sshconnection == "Success":
                    print("success")

                    channel = ssh.invoke_shell()
                    pdb.set_trace()

                    print "Looping"
                    time.sleep(5)
                    if channel.recv_ready():

                        time.sleep(2)
                        channel_data += channel.recv(9999)
                        print '####Device Output#####'
                        print channel_data
                        pdb.set_trace()

                        if ("#" in channel_data):




                            ##Pass VsanNo variable to command
                            print("Ready to execute commands")
                            pdb.set_trace()





                            ####Check for VSAN NO

                            channel.send('config')

                            channel.send('\n')

                            time.sleep(2)

                            channel.send('device-alias database')

                            channel.send('\n')

                            if("not" in  currentdata['HostAlias_status']):
                                hostaliascmd = 'device-alias name ' + "" + Hostname+ "_"+ Vhbano +" pwwn" +" "+ Hostwwn

                                channel.send(hostaliascmd)

                                channel.send('\n')

                                channel.send('device-alias commit')

                                channel.send('\n')

                                channel.send('show device-alias name '+ Hostname+ "_"+ Vhbano +" pwwn" +" "+ Hostwwn)

                                channel.send('\n')

                                time.sleep(2)

                                print("Checkng HOst Device alias")


                                while channel.recv_ready() == True:

                                    print("reading please wait")
                                    channel_data += channel.recv(9999)

                                    if(channel_data.endswith('')):

                                        print("CLOSING THE OPERATION")

                                        ###Regex part

                            else:

                                print("Host Alias already exists hence checking Array Alias")

                            ###Now check for array alias
                            if("not" in currentdata['ArrayAlias_status']):
                                arrayaliascd = 'device-alias name '+ "VMAX"+ ""+lastArray+ "_"+ Faportname +" "+"pwwn"+" "+ Arraywwn
                                arrayaliascmd =ast.literal_eval(json.dumps(arrayaliascd))

                                channel.send('device-alias database')

                                channel.send('\n')
                                pdb.set_trace()

                                print('stopping before array alias creation')

                                channel.send(arrayaliascmd)


                                channel.send('\n')





                                channel.send('device-alias commit')

                                channel.send('\n')

                                channel.send('show device-alias name '+ Arrayname+ "_"+ Faportname +" "+"pwwn"+" "+ Arraywwn)

                                channel.send('\n')

                                time.sleep(2)

                                print("Checkng Array Device alias")


                                while channel.recv_ready() == True:

                                    print("reading please wait")
                                    channel_data += channel.recv(9999)

                                    if(channel_data.endswith('')):

                                        print("CLOSING THE OPERATION")

                            else:

                                print("Array Alias already exists hence going for zone creation part")


                                     ##Regexpart

                            pdb.set_trace()

                            ####Now create zones

                            channel.send('config')

                            channel.send('\n')
                            while channel.recv_ready() == True:

                                print("reading please wait")
                                channel_data += channel.recv(9999)

                                if(channel_data.endswith('')):

                                    print("CLOSING THE OPERATION")


                            if("(config)" in channel_data):


                                if("is" in currentdata['HostZone_status']):
                                    finalArray = "VMAX" + Arrayname[-4:]
                                    print("Checking Array name")
                                    pdb.set_trace()
                                    print("Checking for Host Name")
                                    zonename_sw_a1 = Hostname+"_"+Vhbano+"_"+finalArray+"_"+""+Faportname

                                    zonename_sw_a1_cmd = "zone name "+ zonename_sw_a1 + " vsan " + VsanNo

                                    channel.send(zonename_sw_a1_cmd)

                                    channel.send('\n')

                                    channel.send("member pwwn "+ Hostwwn)
                                    channel.send('\n')

                                    channel.send("member pwwn "+ Arraywwn)


                                    channel.send('\n')
                                    channel.send('zone commit vsan '+  VsanNo)

                                    channel.send('\n')


                                    time.sleep(1)

                                    channel.send('show zone pending-diff')

                                    channel.send('\n')
                                    pdb.set_trace()
                                else:
                                    print("Host Zone is present")



                            #channel.send('zone commit vsan <vsan no>')

                            #channel.send('\n')

                            ###Check for entries pr else roolback

                            #channel.send('show zone pending-diff')

                            #channel.send('\n')

                            while channel.recv_ready() == True:

                                print("reading zone set entries")
                                channel_data += channel.recv(9999)

                                if(channel_data.endswith('')):

                                    print("CLOSING THE OPERATION")

                            ####Check if there is any pending entry else initiate rollback
                            print("Zone created")
                            zonecheckcmd = "show " + ""+ zonename_sw_a1_cmd
                            zonecheck_cmd = ast.literal_eval(json.dumps(zonecheckcmd))
                            channel.send(zonecheck_cmd)

                            channel.send('\n')

                            time.sleep(2)

                            while channel.recv_ready() == True:

                                print("reading zone set entries")
                                channel_data += channel.recv(9999)

                                if(channel_data.endswith('')):

                                    print("CLOSING THE OPERATION")


                            ###check if zone is created with host and arraywwn

                            zonevalidationregex = "show zone name[\s\S]*?#"

                            arrayfacmd = re.findall(zonevalidationregex ,channel_data)
                            Arraywwn in arrayfacmd[0]
                            Hostwwn in arrayfacmd[0]

                            if(Arraywwn in arrayfacmd[0] and Hostwwn in arrayfacmd[0]):

                                print("Host and Array wwn are present in zone")


                            print("Checking for Zone creation Validation Part")

                            pdb.set_trace()





                            ####Check if there is any pending entry and match with vsan else initiate rollback

                            ##code has to come here

                            ###Create zone set
                            channel.send('config')

                            channel.send('\n')


                            zoneset_cmd = "zoneset name "+ "" + Zoneset + " vsan " + VsanNo
                            zonesetcmd =ast.literal_eval(json.dumps(zoneset_cmd))
                            channel.send(zonesetcmd)

                            channel.send('\n')

                            zonename_sw_a1 =ast.literal_eval(json.dumps(zonename_sw_a1))

                            channel.send('member '+ zonename_sw_a1 )

                            channel.send('\n')

                            print("Added members")

                            #needed in prod
                            channel.send('zone commit vsan '+ VsanNo)

                            channel.send('\n')

                            channel.send('show zoneset pending-diff')

                            channel.send('\n')
                            time.sleep(4)

                            while channel.recv_ready() == True:

                                print("reading zone set entries")
                                channel_data += channel.recv(9999)

                                if(channel_data.endswith('')):

                                    print("CLOSING THE OPERATION")


                            ##output check, if no entries, continue, else initiate rollback//

                            ##roll back code has to come WHERE
                            channel.send('config')

                            channel.send('\n')

                            Activatezoneset_cd = "zoneset activate name " + Zoneset +  " vsan " + VsanNo

                            ##remove the u'
                            Activatezoneset_cmd =ast.literal_eval(json.dumps(Activatezoneset_cd))

                            channel.send(Activatezoneset_cmd)

                            channel.send('\n')

                            time.sleep(3)

                            pdb.set_trace()

                            channel.send('zone commit vsan ' + VsanNo)

                            channel.send('\n')

                            print("Zone Activated")

                            channel.send('show zoneset active vsan ' + VsanNo + " | grep -i " + zonename_sw_a1)

                            channel.send('\n')

                            while channel.recv_ready() == True:

                                print("searching for zone names from previous step, if found, proceed, else initiate rollback//")
                                channel_data += channel.recv(9999)

                                if(channel_data.endswith('')):

                                    print("CLOSING THE OPERATION")

                            ###Grep for zone names from previous step, if found, proceed, else initiate rollback//##


                            ##rollback cde has to come here

                            time.sleep(2)

                            channel.send('copy run start')

                            channel.send('\n')

                            channel.send('fin')

                            channel.send('\n')


                            ###Now checking whether the operation has completed or not

                            time.sleep(2)

                            channel.send("show zoneset active | grep - i" + zonename_sw_a1)


                            channel.send('\n')
                            while channel.recv_ready() == True:

                                print("Checking whether final zone is activated")
                                channel_data += channel.recv(9999)

                                if(channel_data.endswith('')):

                                    print("CLOSING THE OPERATION")
                                    break
                            Zonecreationregex = ("show zoneset active \| grep - i" + "" + zonename_sw_a1)

                            Zonesetvalues = re.findall(Zonecreationregex + "[\s\S]*?#",channel_data)
                            print("Check for Zoneset final activation")
                            pdb.set_trace()


                            if(zonename_sw_a1 in Zonesetvalues):
                                print("Zone Succesfully activated and operation completed")
                                Zoneresult['result']= zonenaeme_sw_a1 + "Succesfully configured"
                                Zoneresult['switch'] = Switchname

                            else:
                                Zoneresult['result'] = "Zoning not completed"
                                Zoneresult['switch'] = Switchname










                            ###Now create zones
                    else:
                        print("channel not ready")


                else:
                    ###Ssh connection failed
                    print("ssh connection failed")
                    Zoneresult['result'] = "Ssh Connecteion Failed"
                    Zoneresult['switch'] = Switchname
            else:
                print("Checkbox unselected")
                Zoneresult = "Checkbox left Uncheked"
                Zoneresult['switch'] = Switchname



    return render(request,'add/process.html',{'Zoneresult':Zoneresult,'Swich':Switchname})
