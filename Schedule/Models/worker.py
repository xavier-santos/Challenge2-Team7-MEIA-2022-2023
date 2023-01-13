# Definition of the worker class
# Properties:
#   - id: unique identifier of the worker
#   - start_time: time when the worker starts working
#   - end_time: time when the worker stops working
#   - excluded_weekdays: list of weekdays when the worker is not available

class Worker:
    def __init__(self, worker_id, start_time, end_time, excluded_weekdays):
        self.worker_id = worker_id
        self.start_time = start_time
        self.end_time = end_time
        self.excluded_weekdays = excluded_weekdays
