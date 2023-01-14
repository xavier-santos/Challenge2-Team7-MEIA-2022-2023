import json
import time
import json_exporter
from Models.worker import Worker
from Models.engine import Engine
from Algorithms import GeneticAlgorithm, BruteForce

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

start_time = time.time()
pop_bf, best_bf = BruteForce.bruteforce(workers, engines)
time_bf = time.time() - start_time

print(f"Best Brute Force: {best_bf} \nTime Brute Force: {time_bf} \nBest Genetic Algorithm: {best_ga}"
      f"\nTime Genetic Algorithm: {time_ga}")
