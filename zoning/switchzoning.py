import csv
import paramiko
from datetime import datetime
import pdb
import subprocess, sys
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
channel_data = str()
fa_data = str()

Validationresult = []

hostname = "DURBC-FABRIC-A-MD01"
###pdb.set_trace()

try:
    ssh.connect("DURBC-FABRIC-A-MD01", port=22, username="svc_sanauthcamp" ,password="94YfImdyt")
    print("Successfully connected to ")

    channel = ssh.invoke_shell()
    pdb.set_trace()

    

    print "Looping"
    if channel.recv_ready():
        time.sleep(2)
        
                        
        channel_data += channel.recv(9999)
        print '####Device Output#####'
        print channel_data
        pdb.set_trace()

        if (hostname+"#" in channel_data):

            Vsan = '900'

            print("Ready to execute commands")

            pdb.set_trace()

            ####Check for VSAN NO

            channel.send('terminal length 0')

            channel.send('\n')

            time.sleep(2)

            channel_data += channel.recv(9999)


            
        
            channel.send("show zoneset active vsan"+ " "+ Vsan)

            channel.send('\n')

            print("Checkng channel status")
            pdb.set_trace()

            while channel.recv_ready() == True:

                print("reading please wait")
                channel_data += channel.recv(9999)

                if(channel_data.endswith('')):
                    
                    print("CLOSING THE OPERATION")

                


            pdb.set_trace()

            ###Proceed only if VSAN is present

            if("zoneset name" in channel_data):

                m = re.findall('zoneset name.*', channel_data)
                

                print("VSAN IS PRESENT HENCE CONTINUING WITH THE OPERATION")

                ###Checking Host WWN 20:00:00:25:B5:28:00:DE

                if channel.send_ready():
                
                    channel.send('show flogi database | grep -i "20:00:00:25:B5:28:00:DE"')

                    channel.send('\n')

                    
                else:
                    print("chhannel not ready")

                

                time.sleep(4)
                channel_data = channel.recv(9999)
                pdb.set_trace()

                if("port-channel" in channel_data):

                    print("Host wwn is logged in")
                else:
                    print("Host wwn is not logged in, do you still want to proceed")

                    ###Do not stop if the output is empty

                ##Check Array WWN

                channel.send('show flogi database | grep -i "50:00:09:72:08:2e:f9:68"')
                channel.send('\n')
                time.sleep(2)
                channel_data += channel.recv(9999)
                pdb.set_trace()

                if("fc" in channel_data):

                    print("Fa wwn is logged in")


                else:

                    print("Fa wwn not logged in ")

                ####Now Check for Host Zoneset
                    #20:00:00:25:B5:28:00:DE

                channel.send('show zoneset active | grep -i "20:00:00:25:B5:28:00:DE"')

                channel.send('\n')

                time.sleep(2)

                channel_data += channel.recv(1024)

                pdb.set_trace()

                if("fcid" not in channel_data):

                    print("Host zoneset is not present")

                else:

                    print("Host zoneset is present")

                ####Now check Array Zoneset
                Arrayzoneset ="show zoneset active | grep -i 50:00:09:72:08:2e:f9:68\n"

                channel.send(Arrayzoneset)
                while channel.recv_ready() == True:
                    print("reading hostwwn please wait")
                    channel_data += channel.recv(9999)
                    if(channel_data.endswith('')):
                        print("CLOSING THE OPERATION")

                hostzonesetdetails = re.findall('show zoneset active[\s\S]*#',channel_data)

                hostzonesetdetail = hostzonesetdetails[1]

                
                pdb.set_trace()
                

                
                print(channel_data)

                if("fcid" in hostzonesetdetail):
                    print("Array zoneset is present")

                else:

                    print("Array zoneset is absent")
                #st = channel.recv_exit_status()

                ##Now check host alais

                HostZoneset = "show device-alias database | grep -i 20:00:00:25:B5:28:00:DE"
                channel.send(HostZoneset )
                channel.send('\n')
                time.sleep(2)
                channel_data += channel.recv(1024)
                pdb.set_trace()

                if("name" in channel_data):
                    print("Host alias is present")
                    m = re.findall('device-alias name[\s\S]*?pwwn', channel_data)

                else:
                    print("Array alias is absent")

                ##nnow check array alias

                ArrayZoneset = "show device-alias database | grep -i 50:00:09:72:08:2e:f9:68"
                channel.send(ArrayZoneset)
                channel.send('\n')
                time.sleep(2)
                
                pdb.set_trace()

                if("device-alias name VMAX" in channel_data):
                    print("array Alias is present")
                    m = re.findall('device-alias name[\s\S]*?pwwn', channel_data)
                    
                else:
                    print("array Alias is absent")
                    


                

                    

                


                    

                    

                    

            else:

                print ("VSAN is absent")

                
              

                       
                        
                                   

                     
                     

                 
            


    

except:
    ###if there is an authentication Error
    print("Authentication Error")
    
