import pandas as pd
import numpy as np
from scipy.optimize import differential_evolution
from scipy.optimize import minimize

from apps.home import blueprint
from flask import jsonify, request
from flask_login import login_required
import sqlite3
import datetime
from sqlalchemy import func

from apps.home.models import *
from apps.utils import rack_serializer, history_serializer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

MONITOR_PATH = './apps'
TARGET_FILE = 'experiment_result.csv'
task_status = {'status': 'Not Started'}


# File watcher to monitor the file changes in the database
class MyHandler(FileSystemEventHandler):
    def __init__(self, target_file):
        self.target_file = target_file

    def on_created(self, event):
        # Monitor the file creation
        if event.src_path.endswith(self.target_file):
            print(f'{self.target_file} created!')
            start_optimize()

    def on_deleted(self, event):
        # Monitor the file deletion
        if event.src_path.endswith(self.target_file):
            print(f'{self.target_file} deleted!')

    def on_modified(self, event):
        # Monitor the file modification
        if event.src_path.endswith(self.target_file):
            print(f'{self.target_file} modified!')
            start_optimize()


def monitor_directory(path=MONITOR_PATH, target_file=TARGET_FILE):
    event_handler = MyHandler(target_file)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    task_status['status'] = 'Monitoring directory'

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def start_optimize():
    global task_status
    task_status['status'] = 'Started'

    file_path = os.path.join(MONITOR_PATH, TARGET_FILE)
    data = pd.read_csv(file_path)
    good_solvents = data[data['Solub'] == 1][['delta_d', 'delta_p', 'delta_h']].values
    bad_solvents = data[data['Solub'] == 0][['delta_d', 'delta_p', 'delta_h']].values

    def fitness(params):
        center = params[:3]
        R0 = params[3]
        desirability = []

        # Process good solvents
        for solvent in good_solvents:
            Ra = np.linalg.norm(solvent - center)
            RED = Ra / R0
            if RED <= 1:
                desirability.append(1)  # Ideal for good solvents inside sphere
            else:
                desirability.append(np.exp(1 - RED))  # Penalize if outside

        # Process bad solvents
        for solvent in bad_solvents:
            Ra = np.linalg.norm(solvent - center)
            RED = Ra / R0
            if RED > 1:
                desirability.append(1)  # Ideal for bad solvents outside sphere
            else:
                desirability.append(np.exp(RED - 1))  # Penalize if inside

        # Calculate DATAFIT and Size Factor
        datafit = np.prod(desirability) ** (1 / len(desirability))
        Size_Factor = R0 ** (-1 / len(desirability))
        return -(datafit * Size_Factor)  # Negative for minimization

    param_bounds = [(10, 20), (0, 25.5), (0, 42.3), (0, 30)]
    initial_guess = np.append(np.mean(good_solvents, axis=0), [10])
    seed_value = 56

    def iterative_optimization(bounds, num_iterations=1000, seed_value=seed_value):
        result = differential_evolution(
            fitness,
            bounds,
            strategy='best1bin',
            maxiter=num_iterations,
            popsize=150,
            tol=0.0001,
            mutation=(0.5, 1),
            recombination=0.7,
            seed=seed_value,  # Random number generator seed for consistent results
            polish=True
        )
        return result

    task_status['status'] = 'Optimizing step 1'
    best_result = iterative_optimization(param_bounds, num_iterations=1000, seed_value=seed_value)

    # Check and print the best result
    if best_result.success:
        optimized_center = best_result.x[:3]
        optimized_radius = best_result.x[3]
        print('Optimized sphere center:', optimized_center)
        print('Optimized sphere radius:', optimized_radius)
        task_status['status'] = 'Step 1 completed'
        task_status['optimized_center'] = optimized_center.tolist()
        task_status['optimized_radius'] = optimized_radius
    else:
        print("Optimization failed.")
        task_status['status'] = 'Step 1 failed'

    methods = [
        'Nelder-Mead',
        'Powell',
        'COBYLA',
        'SLSQP',
        'trust-constr'
    ]

    # Increase the maximum number of iterations
    max_iter = 1000  # Example: 10000 iterations

    task_status['status'] = 'Optimizing step 2'

    for method in methods:
        try:
            options = {
                'maxiter': max_iter,
                'disp': True
            }

            task_status['method'] = method
            parameters = None

            if method == 'Nelder-Mead':
                parameters = {'xatol': 1e-9, 'fatol': 1e-9}
                options.update(parameters)
            elif method == 'Powell':
                parameters = {'xtol': 1e-9, 'ftol': 1e-9}
                options.update(parameters)
            elif method == 'COBYLA':
                parameters = {'rhobeg': 1.0}  # 'rhoend' is not a valid parameter for COBYLA
                options.update(parameters)
            elif method == 'SLSQP':
                parameters = {'ftol': 1e-9, 'disp': True}
                options.update(parameters)
            elif method == 'trust-constr':
                parameters = {'gtol': 1e-9}
                options.update(parameters)  # Use 'gtol' instead of 'x_tol'

            task_status['parameters'] = parameters

            result = minimize(
                fitness,
                initial_guess,
                method=method,
                bounds=param_bounds,
                options=options
            )

            if result.success:
                print(f"{method} - Successful: True, Result: {result.x}")
                task_status['status'] = 'Step 2 completed'
                task_status['result'] = result.x.tolist()
            else:
                print(f"{method} - Successful: False, Message: {result.message}")
                task_status['status'] = 'Step 2 failed'
                task_status['result'] = result.message
        except Exception as e:
            print(f"{method} - Error: This method may not be suitable for this problem. Error message: {str(e)}")
            task_status['status'] = 'Step 2 failed'
            task_status['result'] = str(e)
