import jsonpickle
from common.database import Database
from common.process_data import Operation
import os
import cv2

plugins = {}
data_b = Database()


def register_process(func):
    plugins[func.__name__] = func
    return func


def get_tuple(data):
    if not isinstance(data, tuple):
        data = (data.get('id'), data.get('image'), data.get('format'), data.get('name'), data.get('comment')) \
            if isinstance(data, dict) \
            else (None, None, None, None, None)
    return data


@register_process
def put(data_dict):
    try:
        data = get_tuple(data_dict)
        data_b.insert_into_table(data)
    except Exception as ex:
        print(ex)
    finally:
        return data_dict['id']


@register_process
def delete(data):
    data = data['arg']
    img_id = data['img_id']
    data_b.update_data(data, None, img_id)
    return img_id


@register_process
def update(data, value = None, img_id = None):
    if isinstance(data, dict):
        arg = data['arg']
        value = data['value']
        img_id = data['img_id']
    data_b.update_data(data, value, img_id)
    return img_id


@register_process
def processing(img_id, operations):
    image = data_b.get_data('image', img_id)
    image = Operation.fromBytes(image[0])
    image = Operation(image=image, ops=operations).process_image()
    image = Operation(image).toBytes()
    return image


@register_process
def save(image, name):
    path = os.path.join(os.getcwd(), name)
    cv2.imwrite(path, image)


@register_process
def put_process(data):
    image = plugins['processing'](data['id'], data['operations'])
    plugins['update']('image', image, data['id'])
    return 200


@register_process
def saving(data):
    img_id = data['id']
    image = data_b.get_data('image', img_id)
    image = Operation.fromBytes(image)
    name = data_b.get_data('name', img_id)
    save(image, name[0][0])
    image = Operation(image).toBytes()
    return jsonpickle.encode(image)


@register_process
def get_all_data(img_id):
    data = data_b.get_data('img_id, format, name, comment', img_id)
    data = {'id': data[0][0], 'format': data[0][1], 'name': data[0][2], 'comment': data[0][3]}
    return data


def auth(token):
    if token == '6g3vu9lop&*vty43q$':
        return True, {"message": "OK: Authorized"}, 200
    else:

        return False, {"message": "ERROR: Unauthorized"}, 401
