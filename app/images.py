import json
import os
import random
import shutil
import time
import threading

import PIL
from PIL import Image
import requests

from utils.config import getConfig

__CONFIG_LOC__ = 'config/config.json'
config = getConfig(__CONFIG_LOC__)

extensions = set()

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
    img = Image.open(filename)

    file_type = os.path.splitext(filename)[-1]
    out_file = 'static/img/resized_image{}'.format(file_type)

    # Check to see which is bigger (width or height)

    scale = [
        float(img.size[0]) / float(config['screen_size']['width']),
        float(img.size[1]) / float(config['screen_size']['height'])
    ]

    if scale[0] >= scale[1]:
        percent = 1.0 / scale[0]
    else:
        percent = 1.0 / scale[1]

    new_size = (
        int(float(img.size[0]) * percent),
        int(float(img.size[1]) * percent)
    )

    img = img.resize(new_size, PIL.Image.ANTIALIAS)
    img.save(out_file)
    
    return out_file

def download_image(url):
    response = requests.get(url, stream=True)
    
    # Get file extension of image
    img_type = response.headers['Content-Type']
    img_type = img_type.replace('image/', '')

    filename = 'static/img/background.{}'.format(img_type) 

    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    return resize_image(filename)

def generate_return_data(path, data):
    # Generate 'path' without the root folder, and filename
    basename = os.path.basename(path)
    root_dir = config['dropbox_folder'].lower()

    path = path.replace(basename, '')
    path = path.replace(root_dir, '')

    filepath = download_image(data['link'])

    return_data = {
        'path' : path,
        'link' : filepath
    }

    return json.dumps(return_data)

def check_valid_file(file_json):
    if file_json['.tag'] == 'folder':
        return False
                
    # I have a 'hidden' folder in my dropbox image location which
    # contains pictures I don't want to show in my photo frame.
    if 'hidden' in file_json['path_lower']:
        return False

    __IGNORE_EXTENSIONS__ = {'.txt', '.docx', '.wmv', '.mp4', '.avi', '.mov', '.pptx', '.mpg', '.vscode'}

    _, file_extension = os.path.splitext(file_json['path_lower'])

    return not file_extension in __IGNORE_EXTENSIONS__


def get_list_files():
    cursor = ''
    files = {}

    while True:

        if cursor is None:
            with open(config['image_dict_path'], 'w') as files_file:
                files_file.write(json.dumps(files))

            cursor = ''
            return files
            
        elif cursor == '':
            url = 'https://api.dropboxapi.com/2/files/list_folder'

            data = {'path': config['dropbox_folder'],
                    'recursive': True,
                    'include_media_info': False,
                    'include_deleted': False,
                    'include_mounted_folders': True
                    }
        else:
            url = 'https://api.dropboxapi.com/2/files/list_folder/continue'

            data = {'cursor': cursor}

        res = requests.post(url, headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(config['access_token'])}, data=json.dumps(data))
        
        data = json.loads(res.content.decode('utf-8'))

        if data['has_more']:
            cursor = data['cursor']
        else:
            cursor = None

        if data['entries']:
            for d in data['entries']:
                if check_valid_file(d):
                    if 'id' in d:
                        files[d['id']] = d['path_lower']


def get_random_file():
    with open(config['image_dict_path'], 'r') as f:
        files = json.load(f)

    num = len(files.keys())
    i = random.randint(0,num)

    id = list(files.keys())[i]

    print('{} / {}'.format(i, num))

    path = files[id]

    url = 'https://api.dropboxapi.com/2/files/get_temporary_link'

    data = {'path': path }

    print(path)

    res = requests.post(url, headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(config['access_token'])}, data=json.dumps(data))
        
    data = json.loads(res.content.decode('utf-8'))

    return generate_return_data(path, data)
