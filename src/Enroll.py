import requests
import subprocess
import Filewatcher
import time
import os
import Registry
import win32serviceutil
import File

def download_client():
    print('Downloading client')
    url = 'https://downloads.hpdaas.com/master/microsoft/tm-client/3.21.1239/HPTechPulse.msi'
    r = requests.get(url, allow_redirects=True)
    open('HPTechPulse.msi', 'wb').write(r.content)
    print('Downloaded')

def install_enroll_client():
    print('Installing and Enrolling client')
    subprocess.call('msiexec /i %s CPIN=%s SERVER=%s' % ('HPTechPulse.msi', 'S44XiHmq', 'https://usdevms.daas.hppipeline.com/'), shell=True)
    print('Installation is done and enrolling client, waiting for 1 min 30 seconds')
    time.sleep(90)
    
    # Read from registr editor
    val = Registry.read_registry('DeviceEnrolled')
    if(val == "True"):
        print("Successfully enrolled")
    else:
        print('Failed to enrolled')


# AwsIot:Publish event success, Event: DeviceSBChanged
def verify_devicesbchangeevent_onenroll():
    File.search_text_in_file('C:\\ProgramData\\HP\\StreamLog\\LHAgent.exe\\*.log', 
        "AwsIot:Publish event success, Event: DeviceSBChanged", 
        "DeviceSbChanged")


def verify_devicesbchangeevent_notsent_onservicerestart():
    # Restart LHAgent service
    print('Restarting LHAgent service')
    win32serviceutil.RestartService("hpLHAgent")

    print("Restarted, Waiting for 5 mins")
    time.sleep(300)

    File.search_text_in_file('C:\\ProgramData\\HP\\StreamLog\\LHAgent.exe\\*.log', 
        "AwsIot:Publish event success, Event: DeviceSBChanged", 
        "DeviceSbChanged")


# print('Starting file watcher')
# Filewatcher.file_watcher()
# latest_file = Filewatcher.get_latest_filename()
# download_client()
# install_enroll_client()
# verify_devicesbchangeevent_onenroll()
verify_devicesbchangeevent_notsent_onservicerestart()