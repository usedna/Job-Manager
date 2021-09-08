import threading

from flask import Flask, request, Response

from app import resources
from server.job_manager import JobManager
from server.utilis import *

app = Flask(__name__)
job_manager = JobManager()
do_scheduler(60, job_manager.q_serialization)


@app.route('/apply', methods=['POST'])
def apply():
    headers = request.headers
    token = headers.get('X-Api-Key')
    auth, msg, status = resources.auth(token)
    if not auth:
        return Response(response=msg, status=status, mimetype="application/json")
    data = request.json
    guid = job_manager.register_job(data, 'put_process')

    return guid


@app.route('/images/<img_id>/image')
def send_back(img_id):
    threading.Lock()
    guid = ''
    try:
        # lock.acquire()
        headers = request.headers
        token = headers.get('X-Api-Key')
        auth, msg, status = resources.auth(token)
        if not auth:
            return Response(response=msg, status=status, mimetype="application/json")
        guid = job_manager.register_job({'id': img_id}, 'saving')
    finally:
        # lock.release()
        return guid


@app.route('/images/<img_id>', methods=['GET', 'PUT', 'DELETE'])
def put(img_id):
    headers = request.headers
    token = headers.get('X-Api-Key')
    auth, msg, status = resources.auth(token)
    if not auth:
        return Response(response=msg, status=status, mimetype="application/json")
    data = {'id': img_id}
    if request.method == 'GET':
        guid = job_manager.register_job(data, 'get_all_data')
    elif request.method == 'PUT':
        guid = job_manager.register_job(data, 'put')
    elif request.method == 'DELETE':
        arg = request.form.get('arg')
        data = {'arg': arg, 'img_id': img_id}
        guid = job_manager.register_job(data, 'delete')
    else:
        data = dict(request.form.items())
        data.update({'img_id': img_id})
        guid = job_manager.register_job(data, 'update')
    return guid


@app.route('/images', methods=['POST'])
def images():
    headers = request.headers
    token = headers.get('X-Api-Key')
    auth, msg, status = resources.auth(token)
    if not auth:
        return Response(response=msg, status=status, mimetype="application/json")

    data = dict(request.form.items())
    image = request.files['file'].stream.read()
    data['name'] = create_file_name(data['name'], data['format'])
    data.update({'image': image})
    guid = job_manager.register_job(data, 'put')

    return guid


@app.route('/queue')
def view_jobs():
    jobs = job_manager.get_all_jobs()
    return {'result': jobs}


@app.route('/queue/<guid>', methods=['POST', 'GET'])
def job_status(guid):
    status = job_manager.get_job_status(guid)
    return status


@app.route('/queue/<guid>/result', methods=['POST'])
def view_result(guid):
    result = job_manager.get_result(guid)
    return result


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
