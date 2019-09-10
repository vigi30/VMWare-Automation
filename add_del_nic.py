from pyVmomi import vim
from pyVmomi import vmodl
from pyVim.connect import SmartConnect, Disconnect
import atexit
import argparse
import getpass
import ssl
import requests
import re
def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def add_nic(si, vm, network):
    
    spec = vim.vm.ConfigSpec()
    nic_changes = []

    nic_spec = vim.vm.device.VirtualDeviceSpec()
    nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

    nic_spec.device = vim.vm.device.VirtualE1000()

    nic_spec.device.deviceInfo = vim.Description()
    nic_spec.device.deviceInfo.summary = 'vCenter API test'

    nic_spec.device.backing = \
        vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
    nic_spec.device.backing.useAutoDetect = False
    content = si.RetrieveContent()
    nic_spec.device.backing.network = get_obj(content, [vim.Network], network)
    nic_spec.device.backing.deviceName = network

    nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.allowGuestControl = True
    nic_spec.device.connectable.connected = False
    nic_spec.device.connectable.status = 'untried'
    nic_spec.device.wakeOnLanEnabled = True
    nic_spec.device.addressType = 'assigned'

    nic_changes.append(nic_spec)
    spec.deviceChange = nic_changes
    e = vm.ReconfigVM_Task(spec=spec)
    print "NIC CARD ADDED"

    
    
def del_nic(si, vm, nic_number):
    
    nic_prefix_label = 'Network adapter '
    nic_label = nic_prefix_label + str(nic_number)
    virtual_nic_device = None
    for dev in vm.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualEthernetCard)   \
                and dev.deviceInfo.label == nic_label:
            virtual_nic_device = dev

    if not virtual_nic_device:
        raise RuntimeError('Virtual {} could not be found.'.format(nic_label))

    virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
    virtual_nic_spec.operation = \
        vim.vm.device.VirtualDeviceSpec.Operation.remove
    virtual_nic_spec.device = virtual_nic_device

    spec = vim.vm.ConfigSpec()
    spec.deviceChange = [virtual_nic_spec]
    task = vm.ReconfigVM_Task(spec=spec)
    #tasks.wait_for_tasks(si, [task])
    return True




def main():

    ls=[]
    while True:
        vm_name=raw_input("enter the vm name or ip if u know")
        
        if vm_name=='done':
            break
        else:
            if len(vm_name)>0: 
                ls.append(vm_name)
            else:
                continue
    # args = get_args()
    

    requests.packages.urllib3.disable_warnings()
 


# Disabling SSL certificate verification
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE

    # connect this thing
    si=SmartConnect(host='2.2.2.2', user='abcdl', pwd='abcd', port=443, sslContext=context)
    # disconnect this thing
    atexit.register(Disconnect, si)
    for i in ls:
        
        print 'give information for  vm',i
        
        vm = None
        if  re.search('^[0-9].*',i):
            search_index = si.content.searchIndex
            vm = search_index.FindByIp(ip=i,vmSearch= True)
            print "vm found using ip hahahahaha"
            
        elif re.search('^[A-za-z]*',i):
            content = si.RetrieveContent()
            vm = get_obj(content, [vim.VirtualMachine],i)
            print "vm found using name hahahahaha"
            
        if vm:
            choice=raw_input('Wanna Add or delete the nic say add or del')
            if choice=='add':
                port_group=raw_input("enter the port group name")
                add_nic(si,vm,port_group)
            elif  choice=='del':
                confirm=raw_input("DO you want to delete this nic yes/no")
                if confirm =='yes':
                    number=raw_input("Enter the number of the nic card:")
                    del_nic(si,vm,number)
                    print('VM nic "{}" successfully deleted.'.format(number))
            else:
                print 'please do some other job'
                
        else:
            print "VM not found hehehehe"

   # start this thing
if __name__ == "__main__":
    main()
