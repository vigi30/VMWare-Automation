import ssl
import time
from pyVim.connect import SmartConnect, Disconnect  
import re
import atexit
import requests
#from tools import cli
#from tools import tasks
from pyVim import connect
from pyVmomi import vim, vmodl


def getvm(content, vimtype, name):

    
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                vm = c
                break
        else:
            vm = c
            break

    
    return vm
    
    
    
    
requests.packages.urllib3.disable_warnings()
# Disabling SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE

try:

                                            

    si=SmartConnect(host='1.1.1.1', user='abcded', pwd='abcdef', port=443, sslContext=context)
    atexit.register(connect.Disconnect, si)
    content = si.RetrieveContent()
    searcher = si.content.searchIndex
    ls=[]
    while True:
        ls_name=raw_input("Enter the VM name or ip ")
        
        if ls_name=='done':
            break
        else:
            
            if len(ls_name)>0: 
                ls.append(ls_name)
           
                
            
    for i in ls:
            

        vm = None
        if  re.search('^[0-9].*',i):
            search_index = si.content.searchIndex
            vm = search_index.FindByIp(ip=i,vmSearch= True)
            print "vm found using ip hahahahaha"
            
        elif re.search('^[A-za-z]*',i):
            content = si.RetrieveContent()
            vm = getvm(content, [vim.VirtualMachine],i)
            print "vm found using name hahahahaha"
            
        else:
            print "VM not found hehehehe"

        print vm
        #'C:\Python27\ser.ps1'
        if re.search('Linux',vm.summary.config.guestFullName):
            vm_path=raw_input("ENter the  path inside a linuxVM if you want to upload ")
            vm_upload_file=raw_input("Enter the path of the file you want to upload in linuxVM ")
            creds = vim.vm.guest.NamePasswordAuthentication(username='r', password='abcd')
               
            f=open(vm_upload_file)
            args = f.read()
            

            try:
                file_attribute = vim.vm.guest.FileManager.FileAttributes()
                
           
                url = content.guestOperationsManager.fileManager.InitiateFileTransferToGuest(vm, creds, vm_path,file_attribute,len(args), True)#/tmp/mbox-short.txt
                
                resp = requests.put(url, data=args, verify=False)
                
                if not resp.status_code == 200:
                    print "Error while uploading file"
                else:
                    print "Successfully uploaded file"
                    arg=raw_input("Enter the command  or the script path to be run inside a shell if not leave blank")
                    if arg:
                    
                        pm = content.guestOperationsManager.processManager
                        ps = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash",arguments=arg)#arguments= "-command ls
                        res = pm.StartProgramInGuest(vm, creds, ps)
                        if res > 0:
                            print "Program submitted, PID is %d" % res
                            pid_exitcode = pm.ListProcessesInGuest(vm, creds,
                                                               [res]).pop().exitCode
                            while (re.match('[^0-9]+', str(pid_exitcode))):
                                print "Program running, PID is %d" % res
                                time.sleep(5)
                                pid_exitcode = pm.ListProcessesInGuest(vm, creds,
                                                                   [res]).pop().\
                                                                   exitCode
                                if (pid_exitcode == 0):
                                    print "Program %d completed with success" % res
                                    continue
                                elif (re.match('[1-9]+', str(pid_exitcode))):
                                    print "ERROR: Program %d completed with Failute" % res
                                    
                                    print "ERROR: More info on process"
                                    print pm.ListProcessesInGuest(vm, creds, [res])
                                    continue
                    else:
                        continue
            except IOError, e:
                print e
        
        elif re.search('Windows',vm.summary.config.guestFullName):
                vm_path=raw_input("ENter the  path inside a windowsVM if you want to upload ")
                vm_upload_file=raw_input("Enter the path of the file you want to upload in windowsVM ")
                creds = vim.vm.guest.NamePasswordAuthentication(username='abcd', password='sbcd@123')
                  
                f=open(vm_upload_file)
                args = f.read()
               

                try:
                    file_attribute = vim.vm.guest.FileManager.FileAttributes()
                    
               
                    url = content.guestOperationsManager.fileManager.InitiateFileTransferToGuest(vm, creds, vm_path,file_attribute,len(args),True)#c:\upload\ser.ps1
                   
                    resp = requests.put(url, data=args, verify=False)
                   
                    if not resp.status_code == 200:
                        print "Error while uploading file"
                    else:
                        print "Successfully uploaded file"
                        arg=raw_input("Enter the command  or the script path to be run inside a shell if not leave blank")
                        if arg:
                            pm = content.guestOperationsManager.processManager
                            ps = vim.vm.guest.ProcessManager.WindowsProgramSpec(programPath="C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe",arguments='-command '+args)#arguments= "-command ls
                            res = pm.StartProgramInGuest(vm, creds, ps)
                            if res > 0:
                                print "Program submitted, PID is %d" % res
                        else:
                            continue
                except IOError, e:
                    print e            
                
except vmodl.MethodFault as error:
    print "Caught vmodl fault : " + error.msg
    
