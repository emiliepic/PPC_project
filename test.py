from n_queens import N_QUEENS
import time
import matplotlib.pyplot as plt

n = 10
start = time.time()
n_queens_test = N_QUEENS(n, var_heuristic="static", val_heuristic="static")
sol = n_queens_test.solve(use_ac3=True, fc=False, use_ac3_meanwhile=True)
print(n, sol)
end = time.time()
n_queens_test.solution_printer(sol)
print(f"n = {n}, time = {end - start}")
