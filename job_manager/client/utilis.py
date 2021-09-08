import os.path

import cv2
import requests

from common.database import Database
from common.process_data import Operation

urls = {'sending': 'http://localhost:5000/images',
        'process': 'http://localhost:5000/apply'}
header = {'X-Api-Key': '6g3vu9lop&*vty43q$'}


def prepare_image(name):
    image = cv2.imread(name)
    im_byn = Operation(image).toBytes()
    name = os.path.basename(name)
    ext = name.split('.')[-1]
    content_type = f'img/{ext}'
    return {"file": (name, im_byn, content_type)}, ext


def send_image(data):
    global urls
    img_file, ext = prepare_image(data['image'])
    img_id = Database().get_lid() + 1
    info = {'id': img_id, 'format': ext, 'name': data['name'], 'comment': data['comment']}
    print('Sending...')
    guid = requests.post(url=urls['sending'], files=img_file, data=info, headers=header)
    guid = guid.text
    return guid


def send_for_processing(data, img_id):
    par = {'id': img_id, 'operations': data['operations']}
    print('Processing image...')
    guid = requests.post(urls['process'], json=par, headers=header)
    return guid.text


def get_image(img_id):
    print('Saving image...')
    guid = requests.get(url='http://localhost:5000/images/{}/image'.format(img_id),
                        headers=header)

    return guid.text
