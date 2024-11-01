import os
import time
import json
import csv
import itertools
import matplotlib.pyplot as plt
from n_queens import N_QUEENS
from coloring import dichotomic_search

def plot_time_vs_instances_different_methods(instances, methods, type_problem="n_queens", time_limit=20, save=False, plot=True):
    """
    Plot the resolution time for each instance in instances for each method in methods
    :param instances: list of instances
    :param methods: list of methods (methods list of method={"use_ac3": True or False, "fc": True or False, "var_heuristic": "static" or "MRV" or "degree", "val_heuristic": "static" or "inverse" or "random"})
    :param time_limit: time limit for the resolution
    :param type_problem: type of problem to solve
    :param save: if True, save the results to a CSV file
    """
    if save:
        project_path = os.getcwd()
        # Create a CSV file to save the results
        file_path = os.path.join(project_path, "results", f"{type_problem}_results.csv")
        csvfile = open(file_path, 'w', newline='')
        fieldnames = ['instance', 'use_ac3', 'fc', 'var_heuristic', 'val_heuristic', 'execution_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
    times = {ind: [] for ind in range(len(methods))}
    
    for instance in instances:
        for ind, method in enumerate(methods):
            if type_problem == "n_queens":
                prob = N_QUEENS(instance, method["var_heuristic"], method["val_heuristic"])
                start = time.time()
                sol = prob.solve(use_ac3=method["use_ac3"], fc=method["fc"], time_limit=time_limit)
                end = time.time()
            elif type_problem == "coloring":
                start = time.time()
                sol = dichotomic_search(instance, method["use_ac3"], method["fc"], method["var_heuristic"], method["val_heuristic"], time_limit)
                end = time.time()
                
            execution_time = end - start
            times[ind].append(execution_time)
            
            print(f"Instance: {instance}, Method: {method}, Time: {execution_time:.4f} seconds")
            
            if save:
                writer.writerow({
                    'instance': instance,
                    'use_ac3': method["use_ac3"],
                    'fc': method["fc"],
                    'var_heuristic': method["var_heuristic"],
                    'val_heuristic': method["val_heuristic"],
                    'execution_time': round(execution_time, 6)
                })
    
    if save:
        csvfile.close()
    if plot:
        for ind, method in enumerate(methods):
            plt.plot(instances, times[ind], label=f'{method}')
    
        if max([max(times[ind]) for ind in range(len(methods))]) > time_limit:
            plt.axhline(y=time_limit, color='r', linestyle='-', label="Time limit")
        
        plt.xlabel("Instance")
        plt.ylabel("Time (s)")
        plt.title(f"Resolution Time for {type_problem} Problem")
        plt.legend()
        plt.show()

def plot_from_csv(type_problem):
    """
    Plot resolution time for instances and methods from a saved CSV file.
    :param file_path: path to the CSV file with saved results
    """
    # Initialiser un dictionnaire pour stocker les temps d'exécution par méthode
    data = {}
    instances = set()

    file_path = os.path.join(os.getcwd(), "results", f"{type_problem}_results.csv")

    # Lire le fichier CSV
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if type_problem == "n_queens":
                instance = int(row['instance'])
            elif type_problem == "coloring":
                instance = row['instance']
            
            method_key = (row['use_ac3'], row['fc'], row['var_heuristic'], row['val_heuristic'])
            execution_time = float(row['execution_time'])
            
            # Ajouter l'instance et son temps d'exécution
            instances.add(instance)
            if method_key not in data:
                data[method_key] = {}
            data[method_key][instance] = execution_time

    # Convertir les instances en une liste triée
    instances = sorted(list(instances))

    # Tracer les temps d'exécution pour chaque méthode
    for method_key, times in data.items():
        use_ac3, fc, var_heuristic, val_heuristic = method_key
        label = f'AC3: {use_ac3}, FC: {fc}, Var Heuristic: {var_heuristic}, Val Heuristic: {val_heuristic}'
        # Obtenir les temps d'exécution dans l'ordre des instances
        execution_times = [times[instance] for instance in instances]
        plt.plot(instances, execution_times, label=label)

    # Ajouter des détails au graphique
    plt.xlabel("Instance")
    plt.ylabel("Time (s)")
    plt.title("Resolution Time from CSV Data")
    plt.legend()
    plt.show()

file_path = os.path.join(os.getcwd(), "results", "n_queens_results.csv")
file_path = os.path.join(os.getcwd(), "results", "coloring_results.csv")
plot_from_csv("n_queens")
plot_from_csv("coloring")

# coloring_instances = ["myciel3.col.txt", "myciel4.col.txt", "myciel5.col.txt", "myciel6.col.txt", "myciel7.col.txt"]
coloring_instances = ["myciel3.col.txt", "mycie4.col.txt"]
coloring_instances = [os.path.join("instances", "coloring", instance) for instance in coloring_instances]
queen_instances = range(4, 15)

for instances, type_problem in zip([coloring_instances, queen_instances], ["coloring", "n_queens"]):
    for use_ac3 in [True, False]:
        for fc in [True, False]:
            methods = []
            for var_heuristic in ["static", "MRV", "degree"]:
                for val_heuristic in ["static", "inverse", "random", "LCV"]:
                    print(use_ac3, fc, var_heuristic, val_heuristic)
                    methods += [{"use_ac3": use_ac3, "fc": fc, "var_heuristic": var_heuristic, "val_heuristic": val_heuristic}]
            plot_time_vs_instances_different_methods(instances, methods, type_problem, 30, save=True, plot=False)