import win32evtlog
from datetime import datetime

def check_crash_in_event_viewer(server, logtype, time, message):
    hand = win32evtlog.OpenEventLog(server,logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    flag = False
    while True:
        if flag:
            break
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if events:
            for event in events:
                if event.EventID == 1000:
                    # print ('Event Category:', event.EventCategory)
                    # print ('Time Generated:', event.TimeGenerated)
                    # print ('Source Name:', event.SourceName)
                    # print ('Event ID:', event.EventID)
                    # print ('Event Type:', event.EventType)
                    dt_string = event.TimeGenerated.strftime("%Y-%m-%d %H:%M:%S")
                    if dt_string > time:
                        data = event.StringInserts
                        if data:
                            for msg in data:
                                if msg == message:
                                    print(message + ' is crashed')
                                    flag = True
        else:
            print(message + ' is not crashed')
            break
    
    return flag