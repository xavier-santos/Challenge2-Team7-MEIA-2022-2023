import json

from Model.engine import Engine
from Model.worker import Worker


def import_engines():
    engines = []
    file = open('../../Data/SchedulingData.json')
    data = json.load(file)
    for engine in data["engines"]:
        engines.append(Engine(engine["id"], engine["ttf"], engine["maintenancetime"]))
    file.close()
    return engines


def import_workers():
    workers = []
    file = open('../../Data/Workers.json')
    data = json.load(file)
    for worker in data["workers"]:
        print(worker)
        workers.append(Worker(worker["id"], worker["starttime"], worker["endtime"]))
    file.close()
    return workers


if __name__ == '__main__':
    import_workers()
