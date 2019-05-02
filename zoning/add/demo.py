def storage_validation(request,**kwargs):

    switchlist= []
    switchusername = request.POST.get('username')
    switchpassword = request.POST.get('password')
    ##pdb.set_trace()

    ###get data from previous session

    sesadata = request.session.get('sesa')
    sesbdata = request.session.get('sesb')
    #pdb.set_trace()

    switchlist=[sesadata[0],sesbdata[0]]


    #pdb.set_trace()
    print(switchlist)
    ValidationResult =[]

    for switch in switchlist:
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
            ###pdb.set_trace()

            print "Looping"
            time.sleep(5)

            if channel.recv_ready():

                time.sleep(2)
                channel_data += channel.recv(9999)
                print '####Device Output#####'
                print channel_data
                ###pdb.set_trace()

                if (Switchname+"#" in channel_data):

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

                    ###pdb.set_trace()

                    ###Proceed only if VSAN is present

                    if("zoneset name" in channel_data):

                        mg = re.findall('zoneset name.*', channel_data)



                        result['vsan'] = mg[0] + " " ' is Configured'




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
                            ###pdb.set_trace()


                        if("port-channel" in channel_data):

                            print("Host wwn is logged in")



                            hostzonesetdetails = re.findall("port-channel.*",channel_data)
                            hostvsan=hostzonesetdetails[0].split()[1]

                            portchanneldetails = re.findall("(port-channel)\w+",channel_data)

                            if(VsanNo == hostvsan):
                                portchanneldetails = re.findall("(port-channel\w+)",channel_data)
                                ##pdb.set_trace()

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
                        ###pdb.set_trace()

                        if("fc" in arrayfacmd[0]):

                            print("Fa wwn is logged in")

                            arrayzonesetdetails = re.findall("fc.*",arrayfacmd[0])
                            ###pdb.set_trace()
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
                        ###pdb.set_trace()

                        ###Cchecking if the list is empty as the regex return array

                        if not hostzonesetdetails:
                            result['hostzoneset'] = Hostwwn + " is not a part of active zoneset"
                        else:

                            for hostzonesetdetail in hostzonesetdetails:
                                if("zone" not in hostzonesetdetail):

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


                        ##pdb.set_trace()

                        #arrayzonesetdetail = arrayzonesetdetails[1]

                        if not arrayzonesetdetails:
                            result['arrayzoneset'] = "FA PORT WWN" + " " +Arraywwn+ " is not part of an active zone"
                        else:

                            for arrayzonesetdetail in arrayzonesetdetails:
                                if("zone" in arrayzonesetdetail):
                                    print("FA PORT is a part of Active Zoneset")

                                    result['arrayzoneset'] = Arraywwn + "Zoneset is present"

                                else:
                                    result['arrayzoneset'] = "FA PORT WWN" + " " +Arraywwn+ " is not part of an active zone"


                        ###now finally checking for host alias
                        HostZoneset = "show device-alias database | grep -i" + " "+  Hostwwn
                        channel.send(HostZoneset )
                        channel.send('\n')
                        time.sleep(4)
                        channel_data += channel.recv(1024)
                        ##pdb.set_trace()

                        hostaliasregex = "show device-alias database \| grep -i "
                        hostaliasvalue = re.findall(hostaliasregex + '[\s\S]*?pwwn',channel_data)

                        ##pdb.set_trace()
                        if(hostaliasvalue):
                            if("name" in hostaliasvalue[0]):

                                print("Host Alias is present")
                                m = re.findall('device-alias name[\s\S]*?pwwn',channel_data)
                                ##pdb.set_trace()
                                m1 = m[0].replace("pwwn", "")
                                result['hostalias'] =  m1

                        else:
                            print("Host Alias is absent")
                            result['hostalias'] = Hostwwn + " Alias is absent"

                        ### now finally check for array Alias
                        ArrayZoneset = "show device-alias database | grep -i" + " "+  Arraywwn

                        channel.send(ArrayZoneset)
                        channel.send('\n')
                        time.sleep(2)
                        channel_data += channel.recv(9999)
                        #arrayaliasregex = "show device-alias database \| grep -i " + Arraywwn
                        arrayaliasvalues = re.findall('show device-alias database \| grep -i[\s\S]*pwwn',channel_data)
                        ###pdb.set_trace()
                        if not arrayaliasvalues:
                            result['arrayalias'] = Arraywwn + "Alias is absent"
                        else:
                            for arrayaliasvalue in arrayaliasvalues:


                                if("VMAX" in arrayaliasvalue):
                                    print("array Alias is present")
                                    m1 = re.findall('device-alias name[\s\S]*?pwwn', arrayaliasvalue)

                                    if(len(m1) > 1):
                                        result['arrayalias'] =  m1[1]
                                    else:
                                        result['arrayalias'] =  m1[0]

                                else:
                                    print("array Alias is absent")
                                    result['arrayalias'] = Arraywwn + "Alias is absent"



                    else:
                        print("VSAN IS ABSENT")

                        result['vsan'] = "VSAN IS ABSENT"
                        result['hostwwn'] = "VSAN IS ABSENT"
                        result['arraywwn'] = "VSAN IS ABSENT"
                        result['hostzoneset'] = "VSAN IS ABSENT"
                        result['arrayzoneset'] = "VSAN IS ABSENT"
                        result['hostalias'] = "VSAN IS ABSENT"
                        result['arrayalias'] = "VSAN IS ABSENT"
            else:
                print("channel not ready")




        else:
            print("ssh connection failed")
            result['vsan'] = "Authentication error"
            result['hostwwn'] = "Authentication error"
            result['arraywwn'] = "Authentication error"
            result['hostzoneset'] = "Authentication error"
            result['arrayzoneset'] = "Authentication error"
            result['hostalias'] = "Authentication error"
            result['arrayalias'] = "Authentication error"

        ValidationResult.append(result)
        ###pdb.set_trace()
        print(ValidationResult)


        ###pdb.set_trace()


    return render(request,'add/validation.html',{'result':ValidationResult,'switchusername':switchusername,'switchpassword':switchpassword})'''
