import json
import os
import random
import requests
import time
import threading

from utils.config import getConfig

__CONFIG_LOC__ = 'config/config.json'
config = getConfig(__CONFIG_LOC__)

class ThreadClass(object):
    def __init__(self, interval=300):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            get_list_files()

            time.sleep(self.interval)

            print('Image Pull Complete!')
  
def get_list_files():
    cursor = ''
    files = {}

    while True:

        if cursor is None:
            with open(config['image_dict_path'], 'w') as files_file:
                files_file.write(json.dumps(files))

            cursor = ''
            print('Image Pull Complete!')
            return files
            
        elif cursor == '':
            url = 'https://api.dropboxapi.com/2/files/list_folder'

            data = {"path": "/Photos",
                    "recursive": True,
                    "include_media_info": False,
                    "include_deleted": False,
                    "include_mounted_folders": True
                    }
        else:
            url = 'https://api.dropboxapi.com/2/files/list_folder/continue'

            data = {"cursor": cursor}

        res = requests.post(url, headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(config['access_token'])}, data=json.dumps(data))
        
        data = json.loads(res.content.decode('utf-8'))

        if data['has_more']:
            cursor = data['cursor']
        else:
            cursor = None

        # TODO : Change to cycle through array rather than one long if

        if data['entries']:
            for d in data['entries']:
                if d['.tag'] == 'folder':
                    continue

                if 'hidden' in d['path_lower']:
                    continue

                if '.mov' in d['path_lower']:
                    continue
                
                if '.modd' in d['path_lower']:
                    continue
                
                if '.wmv' in d['path_lower']:
                    continue
                
                if '.mp4' in d['path_lower'] or '.avi' in d['path_lower']:
                    continue
                
                if '.avi' in d['path_lower']:
                    continue
                
                if 'id' in d:
                    files[d['id']] = d['path_lower']
                
                if '.vscode' in d['path_lower'] or '.avi' in d['path_lower']:
                    continue

def get_random_file():
    with open(config['image_dict_path'], 'r') as f:
        files = json.load(f)

    num = len(files.keys())
    i = random.randint(0,num)

    id = list(files.keys())[i]

    print('{} / {}'.format(i, num))

    path = files[id]

    url = 'https://api.dropboxapi.com/2/files/get_temporary_link'

    data = {"path": path }

    print(path)

    res = requests.post(url, headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(config['access_token'])}, data=json.dumps(data))
        
    data = json.loads(res.content.decode('utf-8'))

    # TODO : Put this in another method
    
    test = path.split('/')
    del test[0]
    del test[0]
    del test[-1]

    path = ''
    for s in test:
        path += s
        path += '/'

    return_data = {
        "path" : path[:-1],
        "link" : data['link']
    }

    return json.dumps(return_data)

