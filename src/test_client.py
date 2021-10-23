import requests
import subprocess
import Filewatcher
import time
import os
import Registry
import win32serviceutil
import File
import EventViewer
from datetime import datetime

def downloadclient():
    print('Downloading client')
    url = 'https://downloads.hpdaas.com/master/microsoft/tm-client/3.21.1239/HPTechPulse.msi'
    r = requests.get(url, allow_redirects=True)
    open('HPTechPulse.msi', 'wb').write(r.content)
    print('Downloaded')


# Capability Check: Web Req download, MSI Installation, Windows Registry API
def test_installenrollclient():
    print('Test Case 1 Started')
    Registry.write_registry(r'SOFTWARE\Policies\Hewlett-Packard\HPTechPulse\AssetLocation', 
        'DeviceLocation', 
        'Pune\\baner\\AmarApex\\HP1')
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
    print('Test Case 2 Started')
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
    print('Test Case 3 Started')
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

# Check event
def test_deviceheirarchylocation():
    print('Test Case 4 Started')
    Registry.write_registry(r'SOFTWARE\Policies\Hewlett-Packard\HPTechPulse\AssetLocation', 
        'DeviceLocation', 
        'Pune\\baner\\AmarApex\\HP2')
    
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


# Capability Check: event viewer
def test_checkcrash():
    print('Test Case 5 Started')
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("DateTime : ", dt_string)
    val = EventViewer.check_crash_in_event_viewer('localhost', 'Application', dt_string, 'LHAgent.exe')

    if val == False:
        print("Fifth Test Case Passed")
        assert True
    else:
        print("Fifth Test Case Failed")
        assert False