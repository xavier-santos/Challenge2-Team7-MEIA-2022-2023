import json
import time
import json_exporter
from Models.worker import Worker
from Models.engine import Engine
from Algorithms import GeneticAlgorithm

# Import workers from json file
workers = []
with open('Data/Workers.json') as json_file:
    data = json.load(json_file)
    for p in data['workers']:
        workers.append(Worker(p['id'], p['start_time'], p['end_time'], p['excluded_workdays']))

# Import engines from json file
engines = []
with open('Data/Engines.json') as json_file:
    data = json.load(json_file)
    for p in data['engines']:
        engines.append(Engine(p['id'], p['ttf'], p['maintenance_time']))

start_time = time.time()
pop_ga, best_ga = GeneticAlgorithm.run_evolution(workers, engines)
time_ga = time.time() - start_time

json_exporter.export_week(pop_ga[0], "test.json")

print(f"Best Genetic Algorithm: {best_ga}"
      f"\nTime Genetic Algorithm: {time_ga}")
