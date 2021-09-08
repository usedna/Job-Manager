from random import randint
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from _datetime import datetime


def do_scheduler(time, function):
    schedule = BackgroundScheduler()
    schedule.add_job(func=function, trigger='interval', seconds=time)
    schedule.start()
    atexit.register(lambda: schedule.shutdown)


def create_file_name(img_name, img_format):
    if img_name == '' or img_name is None:
        date = datetime.now().strftime('%d%m%Y_%H%M%S')
        rand_ID = randint(0, 10000) * 23
        img_name = f'image__{date}__{rand_ID}'
    if img_name.find('.') < 0:
        img_name = f'{img_name}.{img_format}'
    return img_name
