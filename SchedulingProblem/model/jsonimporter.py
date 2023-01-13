import json

from model.engine import Engine
from model.worker import Worker


def import_engines() -> [Engine]:
    engines = []
    file = open('tests/SchedulingData.json')
    data = json.load(file)
    for engine in data["engines"]:
        engines.append(Engine(engine["id"], engine["ttf"], engine["maintenancetime"]))
    file.close()
    return engines


def import_workers() -> [Worker]:
    workers = []
    file = open('tests/Workers.json')
    data = json.load(file)
    for worker in data["workers"]:
        workers.append(Worker(worker["id"], worker["starttime"], worker["endtime"], worker["workhours"]))
    file.close()
    return workers
