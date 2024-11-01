import matplotlib.pyplot as plt
import time
from n_queens import N_QUEENS
from coloring import dichotomic_search

def plot_time_vs_instances_different_methods(instances, methods, type_problem="n_queens", time_limit=20):
    """
    Plot the resolution time for each instance in instances for each method in methods
    :param instances: list of instances
    :param methods: list of methods (methods list of method={"use_ac3": True or False, "fc": True or False, "var_heuristic": "static" or "MRV" or "degree", "val_heuristic": "static" or "inverse" or "random"})
    :param time_limit: time limit for the resolution
    :param type_problem: type of problem to solve
    """
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
            print(f"n = {instance}, time = {end - start}")
            times[ind].append(end - start)
    for ind, method in enumerate(methods):
        plt.plot(instances, times[ind], label=method)
    # plot a line for the time limit
    if type_problem == "n_queens" and max([max(times[ind]) for ind in range(len(methods))]) > time_limit:
        plt.axhline(y=time_limit, color='r', linestyle='-', label="Time limit")
    # plt.axhline(y=time_limit, color='r', linestyle='-', label="Time limit")
    plt.xlabel("n")
    plt.ylabel("Time (s)")
    plt.title("Resolution time for n-queens problem")
    plt.legend()
    plt.show()

plot_time_vs_instances_different_methods(range(4, 10), [{"use_ac3": True, "fc": False, "var_heuristic": "static", "val_heuristic": "static"}, {"use_ac3": True, "fc": False, "var_heuristic": "MRV", "val_heuristic": "static"}, {"use_ac3": True, "fc": False, "var_heuristic": "degree", "val_heuristic": "static"}], "n_queens", 20)