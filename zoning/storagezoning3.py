import requests 
import ssl
import warnings
import contextlib
import requests
import json
import pdb
import datetime
import re
import mysql.connector


today_date = datetime.datetime.today().strftime('%Y-%m-%d')

try:
    from functools import partialmethod
except ImportError:
    # Python 2 fallback: https://gist.github.com/carymrobbins/8940382
    from functools import partial

    class partialmethod(partial):
        def __get__(self, instance, owner):
            if instance is None:
                return self

            return partial(self.func, instance, *(self.args or ()), **(self.keywords or {}))

@contextlib.contextmanager
def no_ssl_verification():
    
    old_request = requests.Session.request
    requests.Session.request = partialmethod(old_request, verify=False)

    warnings.filterwarnings('ignore', 'Unverified HTTPS request')
    yield
    warnings.resetwarnings()

    requests.Session.request = old_request
    

username = ''
passcode = ''

conn=mysql.connector.connect(user='',password='',host='',database='',auth_plugin='mysql_native_password')




array=[]


for ip in array:
    
    try:
        
        
        Report = []
        str1 = ''.join(ip)
        onlyip = re.findall(r'[0-9]+(?:\.[0-9]+){3}',str1)
        onlyipstr = onlyip[0]
        print(ip)
        resource='/sloprovisioning/symmetrix'
        url = ip+resource
        #pdb.set_trace()
        with no_ssl_verification():
            
            json_data= requests.get(url, auth=(username,passcode),verify = False).json()
            Symmetrixname = json_data['symmetrixId']
            print(Symmetrixname)

            ##Loop Inside SymmetrixNames of each array and get all directors

            for Symmetrix in Symmetrixname:

                #pdb.set_trace()

                directoru = '/sloprovisioning/symmetrix/'+Symmetrix+'/director/'

                directorurl = ip+directoru

                print(directorurl)

                ###Get all the directors for each Symmetrix

                Dir_data = requests.get(directorurl, auth=(username,passcode),verify = False).json()

                print(Dir_data)

                Dir_count = Dir_data['num_of_directors']

                if(Dir_count > 0 ):

                    Dir_names = Dir_data['directorId']

                    ##Get all Directors starting with FA
                    first_letters = "FA"

                    FA_Dirs = [Dir_name for Dir_name in Dir_names if (first_letters in Dir_name)]

                    ####Get all Ports Under FA Directors hence looping through FA Directors

                    if(len(FA_Dirs) > 0):
                        
                        for FA_Dir in FA_Dirs:

                            #pdb.set_trace()
                            
                            portu = '/sloprovisioning/symmetrix/'+Symmetrix+'/director/'+FA_Dir
                            
                            FA_url = ip + portu

                            FA_Data = requests.get(FA_url, auth=(username,passcode),verify = False).json()


                            print(FA_Data)

                            FA_ports =  FA_Data['director'][0]['num_of_ports']

                            ### Check if each ports has greater than a port

                            ##https://10.254.64.174:8443/univmax/restapi/sloprovisioning/symmetrix/000192601394/director/FA-6F/port###

                            if(FA_ports > 0):

                                #pdb.set_trace()

                                eachport = '/sloprovisioning/symmetrix/'+Symmetrix+'/director/'+FA_Dir+'/port'

                                ep_url = ip + eachport

                                Port_data = requests.get(ep_url, auth=(username,passcode),verify = False).json()

                                Port_id =[]
                                for port in Port_data['symmetrixPortKey']:

                                    Port_id.append(port[u'portId'])

                                    
                                ##### Port_id has alll the ports hence coming out of the for loop

                                    final_data = []

                                for finalport in Port_id:

                                    finalur = '/sloprovisioning/symmetrix/'+Symmetrix+'/director/'+FA_Dir+'/port/'+finalport

                                    finalurl = ip + finalur

                                    print(finalurl)

                                    #pdb.set_trace()

                                    Port_final = requests.get(finalurl, auth=(username,passcode),verify = False).json()

                                    Identifier_id = Port_final['symmetrixPort'][0]['identifier']

                                    finalport = FA_Dir+"_"+finalport

                                    db_Symmetrix = Symmetrix.encode("ascii")

                                    db_FA_dir = FA_Dir.encode("ascii")

                                    db_Identifier_id = Identifier_id.encode("ascii")

                                    db_finalport = finalport.encode("ascii")

                                    

                                    final_data = [[onlyipstr,'Vmax3',db_Symmetrix,db_FA_dir,db_Identifier_id,db_finalport,today_date]]

                                    #pdb.set_trace()


                                    #####Insert final_data into MySql
                                    #mycursor.executemany("""INSERT INTO Vmax (Ip,ArrayName,PoolId,TotalSpace,UsedSpace,FreeSpace,PercentAllocated,PercentSubscribed,StoreDate)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",Report)

                                    mycursor=conn.cursor()
                                    mycursor.executemany("""INSERT INTO zoningReport(Hostname,Version,Array,FaPort,Identifier,FaPortg,todaydate) VALUES(%s,%s,%s,%s,%s,%s,%s)""",final_data)
                                    conn.commit()
                                    mycursor.close()
                                

                                    

                                    
                                   
                

                    

                    

                
                
                

    except Exception as e:
        print(e)




















