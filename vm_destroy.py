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



def destroy(si,vm):
    
    
    print("The current powerState is: {0}".format(vm.runtime.powerState))
    if format(vm.runtime.powerState) == "poweredOn":
        print("Attempting to power off {0}".format(vm.name))
        TASK = vm.PowerOffVM_Task()
        #tasks.wait_for_tasks(si, [TASK])
        print("{0}".format(TASK.info.state))
        print("Destroying VM from vSphere.")
        TASK = vm.Destroy_Task()
    #tasks.wait_for_tasks(si, [TASK])
        print("Done.")
    else:
        #TASK = vm.PowerOnVM_Task()
        print("nothing to display get lst")
        

   

def main():
    ls=[]
    while True:
        vm_name=raw_input("enter the vm name if u know")
        iP=raw_input("enter the vm ip if u have any idea what is it")
        if vm_name=='done' or iP=='done':
            break
        else:
            if len(vm_name)>0: 
                ls.append(vm_name)
            elif len(iP)>0:
                ls.append(iP)
    requests.packages.urllib3.disable_warnings()
 


# Disabling SSL certificate verification
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE

    # connect this thing
    si=SmartConnect(host='1.1.1.1', user='abcd', pwd='abcd', port=443, sslContext=context)
    # disconnect this thing
    atexit.register(Disconnect, si)
    for i in ls:
        vm = None
        if  re.search('^[0-9].*',i):
            search_index = si.content.searchIndex
            vm = search_index.FindByIp(ip=i,vmSearch= True)
            print "vm found using ip hahahahaha"
            destroy(si,vm)
        elif re.search('^[A-za-z]*',i):
            content = si.RetrieveContent()
            vm = get_obj(content, [vim.VirtualMachine],i)
            print "vm found using name hahahahaha"
            destroy(si,vm)
        else:
            print "VM not found hehehehe"

# start this thing
if __name__ == "__main__":
    main()
