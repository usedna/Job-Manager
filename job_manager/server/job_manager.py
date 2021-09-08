import json
import os.path
import queue
import threading
import dill
from server.job import *
import logging

mutex = threading.Lock()


def function(job_manager, guid):
    job_manager.set_status('Running', guid)
    try:
        result = job_manager.running_jobs[guid].run()
        job_manager.set_status('Done', guid)
        job_manager.set_result(result, guid)
    except Exception as ex:
        job_manager.set_status('Error', guid)
        logging.exception(f"Exception occurred in the job function")
        return ex
    finally:
        job_manager.job2json()
        job_manager.done_jobs.update({guid: job_manager.running_jobs[guid]})


class JobManager:
    q = queue.Queue()
    running_jobs = {}
    done_jobs = {}

    def __init__(self, available_jobs=5):
        self.available_jobs = available_jobs


    def register_job(self, data, job_type):
        a_job = Job(data, job_type)
        self.running_jobs.update({a_job.guid: a_job})
        self.job2json()
        th = threading.Thread(target=self.monitor, args=(a_job.guid,))
        th.start()
        return a_job.guid

    def start_job(self, guid):
        self.acquire()
        th = threading.Thread(target=function, args=(self, guid))
        th.start()

    @staticmethod
    def get_all_jobs():
        with open('jobs.json') as job_file:
            data = json.load(job_file)
        return json.dumps(data)

    @staticmethod
    def get_job_status(guid):
        with open('jobs.json') as job_file:
            data = json.load(job_file)
            status = data[guid].status
            return status

    @staticmethod
    def get_result(guid):
        with open('jobs.json') as job_file:
            data = json.load(job_file)
            result = data[guid].result
            return result

    def job2json(self):
        last_jobs = {}
        try:
            if os.stat('jobs.json').st_size != 0:
                with open('jobs.json', 'r') as jobs_file:
                    last_jobs = json.load(jobs_file)
        except FileNotFoundError:
            pass
        finally:
            last_jobs.update(self.running_jobs)
            with open('jobs.json', 'w') as jobs_file:
                json.dump(last_jobs, jobs_file, indent=4)

    def q_serialization(self):
        if not self.q.empty():
            with open('queue.bin', 'wb') as q_file:
                dill.dump(self.q, q_file)

    def set_status(self, new_status, guid):
        self.running_jobs[guid].status = new_status

    def set_result(self, result, guid):
        self.running_jobs[guid].result = result

    def job_is_available(self):
        if self.available_jobs == 0:
            return False
        return True

    def acquire(self):
        self.available_jobs -= 1

    def release(self):
        self.available_jobs += 1

    def finish(self):
        for job in self.running_jobs.values():
            if job.status in ['Done', 'Error']:
                self.release()
                del self.running_jobs[job.guid]

    def monitor(self, guid):
        self.finish()
        if not self.job_is_available():
            self.q.put(guid)

        if self.job_is_available():
            if self.q.empty():
                self.start_job(guid)
            else:
                self.start_qjobs()

    def start_qjobs(self):
        while not self.q.empty():
            self.start_job(self.q.get())
            if not self.job_is_available():
                break
