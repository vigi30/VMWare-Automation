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
        #vm = searcher.FindByIp(ip=tip.get(), vmSearch=True)
        #print 'vm valule',vm
        container = content.rootFolder 
        viewType = [vim.VirtualMachine]
        recursive = True
        containerView = content.viewManager.CreateContainerView(
            container, viewType, recursive)
            
        children = containerView.view
        for vm in children:
            #501f0771-7bbb-9614-55f3-22660a86a5b3
            if vm.summary.config.name=='WIN_PRACT_V':


    # Print out the information of VM
                
                print '\nRam                   :{} MB' .format(vm.summary.config.memorySizeMB)
                print '\nName                 : ', vm.summary.config.name
                print '\nGuest                : ', vm.summary.config.guestFullName
                print '\nInstance UUID        : ', vm.summary.config.instanceUuid
                print '\nBios UUID            : ', vm.summary.config.uuid
                print '\nState                : ', vm.summary.runtime.powerState
                print '\nCpus usage           :',vm.summary.quickStats.overallCpuUsage
                #print 'device information:',vm.config.hardware.device
                for device in vm.config.hardware.device:
                    #print device            # diving into each device
                    dev_details = {'summary': device.deviceInfo.summary}
                    if device.deviceInfo.label.startswith('Hard disk'):
                        print ' \n label: {0}'.format(device.deviceInfo.label)
                        print ' \n------------------'
                        for name,value in dev_details.items():
                            print '\nTotal size: {} GB  '.format(int(value.rstrip('KB').replace(',',''))/(1024*1024))
                                                           
                        dev_details_backing = {'Filename':device.backing.fileName,'Thinprovisioned':device.backing.thinProvisioned }
                        for name1,value1 in dev_details_backing.items():
                            print '\n{} : {}'.format(name1,value1)
                    if device.deviceInfo.label.startswith('Network adapter'):
                     
                        print ' \n label: {0}'.format(device.deviceInfo.label)
                        print ' \n------------------'
                        print '\nMac address : {} '.format(device.macAddress)
                                                           
                          
            
            #if device.backing is None:
                #continue
        #print vm.guest
        
        #print 'hello5'
        Disconnect(vc)
        #print 'hello6'
        exit()                                                                                  
        #print 'hello7'
     
    except IOError as e:
        #print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print 'vcenter ip is incorrect'
    except vim.fault.InvalidLogin:
        print "ERROR: Invalid login credentials '%s'"         
        exit(1)
    except vim.fault as message:
        print("Error connecting to vSphere: %s" % str(message))
        exit(1)
         
        
            


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
     
