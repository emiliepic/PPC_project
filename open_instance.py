import networkx as nx
import os
 
print(os.getcwd())
def read_file_col(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    graph = nx.Graph()
    for line in lines:
        if line.startswith('e'):
            _, vertex_1, vertex_2 = line.split()
            graph.add_edge(int(vertex_1), int(vertex_2))
    
    return graph

# Example of usage

project_path = os.getcwd()
data_path = os.path.join(project_path,"instances/coloring")
file_name = "fpsol2.i.1.col"
file_path = os.path.join(data_path,file_name)

graph = read_file_col(file_path)

print("Vertices:", graph.nodes())
print("Edges:", graph.edges())