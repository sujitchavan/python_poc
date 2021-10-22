import glob
import os

def search_text_in_file(path, text, eventname):
    # get latest file from LHAgent folder/instead we can use the filewatcher(for this need to invoke in different thread)
    list_of_files = glob.glob(path)
    latest_file = max(list_of_files, key=os.path.getctime)
    print('Reading data from file ' + latest_file)

    # Using readlines()
    file1 = open(latest_file, 'r')
    Lines = file1.readlines()
    
    count = 0
    flag = False
    # Strips the newline character
    for line in Lines:
        count += 1
        s = line.strip()
        if s.find(text) != -1:
            flag = True
            break
    
    if(flag):
        print(eventname + " event sent")
        return True
    else:
        print(eventname + " event not sent")
        return False