import os
import time
import json
import csv
import itertools
import matplotlib.pyplot as plt
from n_queens import N_QUEENS
from coloring import dichotomic_search, COLORING


minima_coloring = {"myciel3.col.txt": 4, "myciel4.col.txt": 5, "myciel5.col.txt": 6, "myciel6.col.txt": 7, "myciel7.col.txt": 8}
# 12 colors for plots
colors_plot = [
    "#1f77b4",  # Bleu (Blue)
    "#ff7f0e",  # Orange (Orange)
    "#2ca02c",  # Vert (Green)
    "#d62728",  # Rouge (Red)
    "#9467bd",  # Violet (Purple)
    "#8c564b",  # Marron (Brown)
    "#e377c2",  # Rose (Pink)
    "#7f7f7f",  # Gris (Gray)
    "#bcbd22",  # Jaune-Vert (Yellow-Green)
    "#17becf",  # Cyan (Cyan)
    "#f5a503",  # Jaune vif (Bright Yellow)
    "#ff4451",  # Rouge vif (Bright Red)
]

def plot_time_vs_instances_different_methods(instances, methods, type_problem="n_queens", fixed_parameters=["fc", "use_ac3"], time_limit=20, save=False, plot=True):
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
    
    
    for ind, method in enumerate(methods):
        for instance in instances:
            if type_problem == "n_queens":
                prob = N_QUEENS(instance, method["var_heuristic"], method["val_heuristic"])
                start = time.time()
                sol = prob.solve(use_ac3=method["use_ac3"], fc=method["fc"], time_limit=time_limit)
                end = time.time()
            elif type_problem == "coloring":
                start = time.time()
                prob = COLORING(instance, minima_coloring[os.path.basename(instance)], method["var_heuristic"], method["val_heuristic"])
                prob.solve(use_ac3=method["use_ac3"], fc=method["fc"], time_limit=time_limit)
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
            if execution_time > time_limit:
                break
    
    if save:
        csvfile.close()
    if plot:
        # big figure
        plt.figure(figsize=(12, 8))
        for ind, method in enumerate(methods):
            label_method = [f"{key}={value}" for key, value in method.items() if key not in fixed_parameters]
            valid_instances = instances[:len(times[ind])]
            if type_problem == "coloring":
                # get only the name of the instance (without the path and extension)
                valid_instances = [os.path.splitext(os.path.basename(instance))[0] for instance in valid_instances]
            plt.plot(valid_instances, times[ind], label=" , ".join(label_method), color=colors_plot[ind])
    
        if max(max(times[ind]) for ind in range(len(methods))) > time_limit:
            plt.axhline(y=time_limit, color='r', linestyle='--', label="Time limit")
        plt.xlabel("Instance")
        plt.ylabel("Time (s)")
        str_fixed_parameters = " ".join([f"{param}={method[param]}" for param in fixed_parameters])
        plt.title(f"Resolution Time for {type_problem} Problem with {str_fixed_parameters}")
        plt.legend()
        # save the plot in high quality
        str_fixed_parameters = "_".join([f"{param}_{method[param]}" for param in fixed_parameters])

        plt.savefig(f"results/{type_problem}_{str_fixed_parameters}_plot.png", dpi=300)
        plt.show()
        plt.close()


coloring_instances = ["myciel3.col.txt", "myciel4.col.txt", "myciel5.col.txt", "myciel6.col.txt", "myciel7.col.txt"]
coloring_instances = [os.path.join("instances", "coloring", instance) for instance in coloring_instances]
type_problem = "coloring"


for use_ac3 in [True, False]:
    for fc in [True, False]:
        methods = []
        for var_heuristic in ["static", "MRV", "degree"]:
        # for var_heuristic in ["static", "MRV"]:
            for val_heuristic in ["static", "inverse", "random", "LCV"]:
            # for val_heuristic in ["static"]:
                print(use_ac3, fc, var_heuristic, val_heuristic)
                methods += [{"use_ac3": use_ac3, "fc": fc, "var_heuristic": var_heuristic, "val_heuristic": val_heuristic}]
        plot_time_vs_instances_different_methods(coloring_instances, methods, type_problem, fixed_parameters=["fc", "use_ac3"], time_limit=3, save=True, plot=True)



queen_instances = range(4, 26)
type_problem = "n_queens"

for use_ac3 in [True, False]:
    for fc in [True, False]:
        methods = []
        for var_heuristic in ["static", "MRV", "degree"]:
        # for var_heuristic in ["static"]:
            for val_heuristic in ["static", "inverse", "random", "LCV"]:
            # for val_heuristic in ["static"]:
                print(use_ac3, fc, var_heuristic, val_heuristic)
                methods += [{"use_ac3": use_ac3, "fc": fc, "var_heuristic": var_heuristic, "val_heuristic": val_heuristic}]
        plot_time_vs_instances_different_methods(queen_instances, methods, type_problem, fixed_parameters=["fc", "use_ac3"], time_limit=20, save=True, plot=True)


def plot_from_csv(type_problem):
    """
    Plot resolution time for instances and methods from a saved CSV file.
    :param file_path: path to the CSV file with saved results
    """
    # Initialize a dictionary to store execution times per method
    data = {}
    instances = set()

    file_path = os.path.join(os.getcwd(), "results", f"{type_problem}_results.csv")

    # Read the CSV file
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if type_problem == "n_queens":
                instance = int(row['instance'])
            elif type_problem == "coloring":
                instance = row['instance']

            method_key = (row['use_ac3'], row['fc'], row['var_heuristic'], row['val_heuristic'])
            execution_time = float(row['execution_time'])

            # Add instance and its execution time
            instances.add(instance)
            if method_key not in data:
                data[method_key] = {}
            data[method_key][instance] = execution_time

    # Convert instances to a sorted list
    instances = sorted(list(instances))

    # Plot execution times for each method
    for method_key, times in data.items():
        use_ac3, fc, var_heuristic, val_heuristic = method_key
        label = f'AC3: {use_ac3}, FC: {fc}, Var Heuristic: {var_heuristic}, Val Heuristic: {val_heuristic}'

        # Get execution times in order of instances, handling missing values
        execution_times = [times.get(instance, None) for instance in instances]

        # Filter out None values (instances with no execution time)
        valid_instances = [instance for instance, time in zip(instances, execution_times) if time is not None]
        valid_times = [time for time in execution_times if time is not None]

        if valid_times:  # Only plot if there is data
            plt.plot(valid_instances, valid_times, label=label)

    # Add details to the plot
    plt.xlabel("Instance")
    plt.ylabel("Time (s)")
    plt.title("Resolution Time from CSV Data")
    plt.legend()
    plt.show()


# file_path = os.path.join(os.getcwd(), "results", "n_queens_results.csv")
# file_path = os.path.join(os.getcwd(), "results", "coloring_results.csv")
# plot_from_csv("n_queens")
# plot_from_csv("coloring")

# # coloring_instances = ["myciel3.col.txt", "myciel4.col.txt", "myciel5.col.txt", "myciel6.col.txt", "myciel7.col.txt"]
# coloring_instances = ["myciel3.col.txt", "myciel4.col.txt"]
# coloring_instances = [os.path.join("instances", "coloring", instance) for instance in coloring_instances]
# queen_instances = range(4, 15)

# for instances, type_problem in zip([coloring_instances, queen_instances], ["coloring", "n_queens"]):
#     for use_ac3 in [True, False]:
#         for fc in [True, False]:
#             methods = []
#             for var_heuristic in ["static", "MRV", "degree"]:
#                 for val_heuristic in ["static", "inverse", "random", "LCV"]:
#                     print(use_ac3, fc, var_heuristic, val_heuristic)
#                     methods += [{"use_ac3": use_ac3, "fc": fc, "var_heuristic": var_heuristic, "val_heuristic": val_heuristic}]
#             plot_time_vs_instances_different_methods(instances, methods, type_problem, 30, save=True, plot=False)