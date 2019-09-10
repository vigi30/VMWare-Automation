from pyVmomi import vmodl
from pyVim.connect import SmartConnect, Disconnect

import atexit

from pyVim import connect
from pyVmomi import vim
#from tools import tasks
import ssl
import requests
import re

def get_obj(content, vimtype, name):

    
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    #container.Destroy()
    return obj



def getInfo(si,vm):
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
def main():
    ls=[]
    while True:
        vm_name=raw_input("enter the vm name if u know")
        
        if vm_name=='done' :
            break
        else:
            if len(vm_name)>0: 
                ls.append(vm_name)
            else:
                continue
    requests.packages.urllib3.disable_warnings()
 


# Disabling SSL certificate verification
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE

    # connect this thing
    si=SmartConnect(host='192.168.150.15', user='administrator@vsphere.local', pwd='Hitachi@123', port=443, sslContext=context)
    # disconnect this thing
    atexit.register(Disconnect, si)
    for i in ls:
        vm = None
        print '-----------------------------------------------------------------------------Information of vm',i
        if  re.search('^[0-9].*',i):
            search_index = si.content.searchIndex
            vm = search_index.FindByIp(ip=i,vmSearch= True)
            print "vm found using ip hahahahaha"
            getInfo(si,vm)
        elif re.search('^[A-za-z]*',i):
            content = si.RetrieveContent()
            vm = get_obj(content, [vim.VirtualMachine],i)
            print "vm found using name hahahahaha"
            getInfo(si,vm)
        else:
            print "VM not found hehehehe"

# start this thing
if __name__ == "__main__":
    main()