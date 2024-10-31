from n_queens import N_QUEENS
import time
import matplotlib.pyplot as plt

n = 4
n_queens_test = N_QUEENS(n)
sol = n_queens_test.solve(use_ac3=True, fc=True)
print(n, sol)

# # get resolution time for each n between 4 and 20
# times = []  
# n_max = 20
# for n in range(4, n_max):
#     n_queens = N_QUEENS(n, "MRV", "random")
#     start = time.time()
#     sol = n_queens.solve(use_ac3=True)
#     end = time.time()
#     if sol != "No solution found":
#         n_queens.solution_printer(sol)
#     print(f"n = {n}, time = {end - start}")
#     times.append(end - start)
# plt.plot(range(4, n_max), times)
# plt.xlabel("n")
# plt.ylabel("Time (s)")
# plt.title("Resolution time for n-queens problem")
# plt.show()


# n = 7
# n_queens_test = N_QUEENS(n)
# sol = n_queens_test.solve(use_ac3=True)
# print(n, sol)

# for i in range(4,n):
#     n_queens_test = N_QUEENS(i)
#     start = time.time()
#     sol = n_queens_test.solve(use_ac3=True)
#     end = time.time()
#     print(sol)

# # n_queens_test.solution_display(sol)