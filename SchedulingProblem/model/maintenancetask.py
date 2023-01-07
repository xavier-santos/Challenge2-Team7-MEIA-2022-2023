from datetime import datetime, timedelta
from model.engine import Engine
from model.worker import Worker


class MaintenanceTask:
    def __init__(self, engine: Engine, worker: Worker, start: datetime):
        self.engine = engine.id
        self.worker = worker.id
        self.start = start
        self.duration = engine.maintenance_time
        self.end = start + timedelta(hours=engine.maintenance_time)
