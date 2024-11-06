from coloring import *

project_path = os.getcwd()
data_path = os.path.join(project_path,"instances/coloring")
file_name = "david.col.txt"
file_name = "fpsol2.i.1.col"
file_name = "myciel4.col.txt"
file_path = os.path.join(data_path,file_name)

# print(dichotomic_search(file_path, use_ac3=True, fc=True, time_limit=40))

graph = COLORING(file_path, 5)
print(graph.variables)
print(graph.domains)
print(graph.constraints[1][2])
sol = graph.solve(use_ac3=True, fc=False, use_ac3_meanwhile=True)
print(sol)
print(graph.is_feasible(sol))

graph.display_sol(sol)



edges = [(1, 2), (1, 3), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5)]
graph = SMALL_COLORING(edges, 3)
print(graph.variables)
print(graph.domains)
print(graph.constraints)
sol = graph.solve(use_ac3=True)
print(sol)
