import threading
from celery import signals
from ether_sql.session import Session
from ether_sql.globals import push_session


class CeleryWorkerThread(threading.Thread):
    """
    Class to open celery in a seperate thread so as to perform tests
    """
    def __init__(self, app, settings=None):
        super().__init__()
        self.app = app
        self.settings = settings
        self.workers = []

    def on_worker_init(self, sender=None, **kwargs):
        self.workers.append(sender)

    def run(self):
        signals.worker_init.connect(self.on_worker_init)

        session = Session(self.settings)
        push_session(session)
        worker = self.app.Worker()
        worker.start()

    def stop(self):
        for w in self.workers:
            w.terminate()

        signals.worker_init.disconnect(self.on_worker_init)
