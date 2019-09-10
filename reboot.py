                    #---------------------------------------------------------------------------LIBRARY---------------------------------------------------------
import ssl  
import requests
 
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
from pyVmomi import vim
import pyVim
import sys

from  Tkinter import  *


#-----------------------------------------------------------------------------------FUNCTION TO GET INFORMATION ABOUT THE VM--------------------------
def info_VM(event):
    #f= sys.stdin.read()
    #sys.stdout.write('Received: %s'%f)
    
    
    # Disabling urllib3 ssl warnings
    requests.packages.urllib3.disable_warnings()
     
    
    
    # Disabling SSL certificate verification
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE
     
    vc = None
     
    
    
    
    
    # Connecting to vCenter
    try:
        #print 'hello110'
        vc = SmartConnect(host=vcenter.get(), user=uname.get(), pwd=password.get(), port=443, sslContext=context)
        #print 'ello2'
        searcher = vc.content.searchIndex
        #print 'hello3'
        #print searcher
        about=vc.content.about
        #print 'ello1'
        ip_details=vc.content.ipPoolManager
        #print  ip_details
            
            
    # Find a VM
        content = vc.RetrieveContent()
        #print content
        lst=['10.57.7.8','10.57.7.9','10.57.7.10','10.57.7.11','10.57.7.12','10.57.7.13']
        for i in lst:
            print 'rebooting .....',i
            vm = searcher.FindByIp(ip=i, vmSearch=True)
        #print 'vm valule',vm
        
            vm.RebootGuest()
        Disconnect(vc)
        exit()                                                                                  
    
    except IOError as e:
        #print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print 'vcenter ip is incorrect'
    except vim.fault.InvalidLogin:
        print "ERROR: Invalid login credentials '%s'"         
        exit(1)
    except vim.fault as message:
        print("Error connecting to vSphere: %s" % str(message))
        exit(1)
    except:
    # forceably shutoff/on
    # need to do if vmware guestadditions isn't running
        vm.ResetVM_Task()
         
        
            


#-----------------------------------------------------------------------------GUI DEVELOPMENT------------------------------
top=Tk()

                #--------------------GETTING THE VALUE FROM ENTRY BOX AND STORING IT  IN THIS VARAIABLE------------
vcenter=StringVar()                                         
port_n=StringVar()
uname=StringVar()
password=StringVar()
tip=StringVar()
                
                #-----------------DEFINING LABEL ,FRAMES ,ENTRY AND BUTTON----------------------
login_button=Button(top,text="InfoVm")
login_button.bind("<Button-1>",info_VM)


entry_vcenter=Entry(top,textvariable = vcenter)
entry_port=Entry(top)
entry_username=Entry(top,textvariable = uname)
entry_password=Entry(top,textvariable = password)
entry_search_vm=Entry(top,textvariable = tip)


label1=Label(top,text='enter the vcenter ip')
label2=Label(top,text='enter the port')
label3=Label(top,text='enter the username')
label4=Label(top,text='enter the password')
label5=Label(top,text='Enter the VM ip want You to Search for')



label1.grid(row=0,column=0,sticky=W)
label2.grid(row=1,column=0,sticky=W)
label3.grid(row=2,column=0,sticky=W)
label4.grid(row=3,column=0,sticky=W)
label5.grid(row=4,column=0,sticky=W)



entry_vcenter.grid(row=0,column=1)
entry_port.grid(row=1,column=1)
entry_username.grid(row=2,column=1)
entry_password.grid(row=3,column=1)
entry_search_vm.grid(row=4,column=1)
login_button.grid(row=5)

top.mainloop()
     
