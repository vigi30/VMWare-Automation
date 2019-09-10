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
    
    
def get_hdd_prefix_label(language):
    language_prefix_label_mapper = {
        'English': 'Hard disk '
        
    }
    return language_prefix_label_mapper.get(language)
    
def delete_virtual_disk(si, vm_obj, disk_number, language):
    
    hdd_prefix_label = get_hdd_prefix_label(language)
    if not hdd_prefix_label:
        raise RuntimeError('Hdd prefix label could not be found')

    hdd_label = hdd_prefix_label + str(disk_number)
    virtual_hdd_device = None
    for dev in vm_obj.config.hardware.device:
        #print dev
        if isinstance(dev, vim.vm.device.VirtualDisk) \
                and dev.deviceInfo.label == hdd_label:
            virtual_hdd_device = dev
    #print virtual_hdd_device        
    if not virtual_hdd_device:
        raise RuntimeError('Virtual {} could not '
                           'be found.'.format(virtual_hdd_device))

    virtual_hdd_spec = vim.vm.device.VirtualDeviceSpec()
    virtual_hdd_spec.operation = \
        vim.vm.device.VirtualDeviceSpec.Operation.remove
    virtual_hdd_spec.device = virtual_hdd_device

    spec = vim.vm.ConfigSpec()
    spec.deviceChange = [virtual_hdd_spec]
    task = vm_obj.ReconfigVM_Task(spec=spec)
    #tasks.wait_for_tasks(si, [task])
    return True    

def add_disk(vm, si, disk_size, disk_type):
        spec = vim.vm.ConfigSpec()
        # get all disks on a VM, set unit_number to the next available
        unit_number = 0
        for dev in vm.config.hardware.device:
            if hasattr(dev.backing, 'fileName'):
                unit_number = int(dev.unitNumber) + 1
                # unit_number 7 reserved for scsi controller
                if unit_number == 7:
                    unit_number += 1
                if unit_number >= 16:
                    print "we don't support this many disks"
                    return
            if isinstance(dev, vim.vm.device.VirtualSCSIController):
                controller = dev
        # add disk here
        dev_changes = []
        new_disk_kb = int(disk_size) * 1024 * 1024
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        disk_spec.fileOperation = "create"
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing = \
            vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        if disk_type == 'thin':
            disk_spec.device.backing.thinProvisioned = True
        disk_spec.device.backing.diskMode = 'persistent'
        disk_spec.device.unitNumber = unit_number
        disk_spec.device.capacityInKB = new_disk_kb
        disk_spec.device.controllerKey = controller.key
        dev_changes.append(disk_spec)
        spec.deviceChange = dev_changes
        vm.ReconfigVM_Task(spec=spec)
        print "%sGB disk added to %s" % (disk_size, vm.config.name)
        # confirm=raw_input("DO you want to delete this disk  yes/no")
        # if confirm =='yes':
            # number=raw_input("Enter the number of the disk:")
            # lang=raw_input("Enter the language used in the Vcenter")
            # delete_virtual_disk(si, vm, number, lang)
            # print('VM HDD "{}" successfully deleted.'.format(number))
        # else:
            # print ("please do some other job")
      
       


def main():
    # args = get_args()


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
            
    requests.packages.urllib3.disable_warnings()
 
# Disabling SSL certificate verification
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE

    # connect this thing
    si=SmartConnect(host='1.1.1.1', user='abcd', pwd='abcd', port=443, sslContext=context)
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
            choice=raw_input('Wanna Add or delete the disk say add or del')
            if choice=='ADD':
                disk_size=raw_input("enter the disk size in GB")
                disk_type=raw_input("enter the disk type either thin or thick")
                add_disk(vm, si, disk_size, disk_type)
            elif  choice=='del':
                confirm=raw_input("DO you want to delete this disk  yes/no")
                if confirm =='yes':
                    number=raw_input("Enter the number of the disk:")
                    lang=raw_input("Enter the language used in the Vcenter")
                    delete_virtual_disk(si, vm, number, lang)
                    print('VM HDD "{}" successfully deleted.'.format(number))
            else:
                print 'please do some other job'
                
        else:
            print "VM not found hehehehe"
# start this thing
if __name__ == "__main__":
    main()
