import json
import os
import PIL
from PIL import Image
import random
import requests
import shutil
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

def resize_image(filename):
    # Check to see which is bigger (width or height)
    img = Image.open(filename)

    file_type = os.path.splitext(filename)[-1]

    out_file = 'static/img/resized_image%s' % file_type
    
    if img.size[0] >= img.size[1] : # width > height
        basewidth = 700
        
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        img.save(out_file)
    else:
        baseheight = 500
        
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(hpercent) * img.size[0]))
        img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
        img.save(out_file)
    
    return out_file

def download_image(url):
    response = requests.get(url, stream=True)
    img_type = response.headers['Content-Type']

    img_type = img_type.replace('image/', '')

    print(img_type)

    filename = 'static/img/background.%s' % img_type 

    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    return resize_image(filename)


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

    filepath = download_image(data['link'])
    print(filepath)

    return_data = {
        "path" : path[:-1],
        "link" : filepath
    }

    return json.dumps(return_data)

