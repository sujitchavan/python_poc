import requests
import subprocess
import Filewatcher
import time
import os
import Registry
import win32serviceutil
import File


def downloadclient():
    print('Downloading client')
    url = 'https://downloads.hpdaas.com/master/microsoft/tm-client/3.21.1239/HPTechPulse.msi'
    r = requests.get(url, allow_redirects=True)
    open('HPTechPulse.msi', 'wb').write(r.content)
    print('Downloaded')


# Capability Check: Web Req download, MSI Installation, Windows Registry API
def test_installenrollclient():
    Registry.delete_registry(r'SOFTWARE\Policies\Hewlett-Packard\HPTechPulse\AssetLocation')
    downloadclient()
    print('Installing and Enrolling client')
    subprocess.call('msiexec /i %s CPIN=%s SERVER=%s' % ('HPTechPulse.msi', 'S44XiHmq', 'https://usdevms.daas.hppipeline.com/'), shell=True)
    print('Installation is done and enrolling client, waiting for 1 min 30 seconds')
    time.sleep(90)
    
    # Read from registr editor
    val = Registry.read_registry('DeviceEnrolled')
    if(val == "True"):
        print("Successfully enrolled")
        print("First Test Case Passed")
        assert True
    else:
        print('Failed to enrolled')
        print("First Test Case Failed")
        assert False


# Capability Check: File Operartions
def test_devicesbchangeeventonenroll():
    time.sleep(150)

    val = File.search_text_in_file('C:\\ProgramData\\HP\\StreamLog\\LHAgent.exe\\*.log', 
        "AwsIot:Publish event success, Event: DeviceSBChanged", 
        "DeviceSbChanged")

    if(val == True):
        assert True
        print("second Test Case Passed")
    else:
        assert False
        print("second Test Case Failed")


# Capability Check: Windows Service API
def test_bitlockereventsentonservicerestart():
    # Restart LHAgent service
    print('Restarting LHAgent service')
    win32serviceutil.RestartService("hpLHAgent")

    print("Restarted, Waiting for 5 mins")
    time.sleep(300)

    val = File.search_text_in_file('C:\\ProgramData\\HP\\StreamLog\\LHAgent.exe\\*.log', 
        "AwsIot:Publish event success, Event: bitlocker-status-event", 
        "bitlocker-status-event")

    if(val == True):
        assert True
        print("Third Test Case Passed")
    else:
        assert False
        print("Third Test Case Failed")


# device heirachy location event on change validation and data validation
def test_deviceheirarchylocation():
    Registry.write_registry(r'SOFTWARE\Policies\Hewlett-Packard\HPTechPulse\AssetLocation', 
        'DeviceLocation', 
        'Pune\\baner\\AmarApex\\HP1')
    
    time.sleep(5)

    val = File.search_text_in_file('C:\\ProgramData\\HP\\StreamLog\\LHAgent.exe\\*.log', 
        "AwsIot:Publish event success, Event: DeviceHierarchyLocationUpdated", 
        "DeviceHierarchyLocationUpdated")    

    if(val == True):
        print("Fourth Test Case Passed")
        assert True
    else:
        print("Fourth Test Case Failed")
        assert False


# event viewer : client crash validation