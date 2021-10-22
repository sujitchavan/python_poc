import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class Filename:
    def __init__(self, name = 0):
         self._name = name
      
    # getter method
    def get_name(self):
        return self._name
      
    # setter method
    def set_name(self, x):
        self._name = x

name = Filename()

def on_created(event):
    print(f"{event.src_path} has been created")
    name.set_name(event.src_path)

def on_modified(event):
    print(f"{event.src_path} has been modified")
    name.set_name(event.src_path)
    # print(get_latest_filename())

def file_watcher():
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_modified = on_modified

    path = "C:\\ProgramData\\HP\\StreamLog\\LHAgent.exe"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()

def get_latest_filename():
    return name.get_name()

# file_watcher()