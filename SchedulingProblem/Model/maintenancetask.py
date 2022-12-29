from datetime import datetime, timedelta
from Model.engine import Engine
from Model.worker import Worker


class MaintenanceTask:
    def __init__(self, engine: Engine, worker: Worker, start: datetime):
        self.engine = engine.id
        self.worker = worker.id
        self.start = start
        self.duration = engine.maintenance_time
        self.end = start + timedelta(hours=3)