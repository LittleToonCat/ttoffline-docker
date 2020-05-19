#!/usr/bin/env python3
import json
import requests
import os
import sys
import hashlib
import bz2
import stat
from pathlib import Path

PATCHER_LINK = 'https://releases.ttoffline.com/'
if sys.platform == 'win32':
    MANIFEST_FILENAME = 'windows.json'
elif 'linux' in sys.platform:
    MANIFEST_FILENAME = 'linux.json'
COMPRESSION_EXTENSION = '.bz2'
EXECUTABLES = ['astrond-linux', 'offline']

def get_hash(filePath):
    hasher = hashlib.md5()
    with open(filePath, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)

    return hasher.hexdigest()

def download_file(fileLocation, fileName, filePath, data):
    Path(data['path']).mkdir(parents=True, exist_ok=True)

    print('Downloading {}'.format(filePath))
    r = requests.get(PATCHER_LINK + fileLocation + COMPRESSION_EXTENSION)

    if r.status_code != 200:
        print('Failed to download file {}, aborting!'.format(filePath))
        sys.exit(1)

    print('Extracting archive...')
    with open(filePath, 'wb') as file:
        file.write(bz2.decompress(r.content))

    if fileName in EXECUTABLES:
        print('Marking {} as executable.'.format(fileName))
        st = os.stat(filePath)
        os.chmod(filePath, st.st_mode | stat.S_IEXEC)

r = requests.get(PATCHER_LINK + MANIFEST_FILENAME)
if r.status_code != 200:
    print('Failed to get mainifest!  Aborting.')
    sys.exit(1)

manifest_dict = r.json()
files = manifest_dict['files']
for file in files:
    data = files[file]
    fileName = file.split('/')[-1]
    filePath = data['path'] + '/' + fileName if data['path'] else fileName
    if os.path.exists(filePath):
        hash = get_hash(filePath)
        if hash == data['hash']:
            print('{} doesn\'t need to be updated. Skipping.'.format(filePath))
            continue
        else:
            download_file(file, fileName, filePath, data)
    else:
        download_file(file, fileName, filePath, data)

# Ensure that astron/databases/astrondb directory is created.
Path('astron/databases/astrondb').mkdir(parents=True, exist_ok=True)

print('Everything should be ready to go!')
sys.exit(0)
