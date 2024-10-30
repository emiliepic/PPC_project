import networkx as nx
import os
from model import CSP
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class COLORING(CSP):
    def __init__(self, file_path, nb_colors):
        self.graph = self.read_file_col(file_path)
        print(self.graph)
        self.nb_colors = nb_colors
        variables = list(self.graph.nodes())
        domains = {var: list(range(nb_colors)) for var in variables}
        self.var_to_index = {var: i for i, var in enumerate(variables)}
        constraints = self.generate_constraints()
        super().__init__(variables, domains, constraints)
    
    def read_file_col(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        vertices = []
        graph = nx.Graph()
        for line in lines:
            #print(line)
            if line.startswith('e'):
                _, vertex_1, vertex_2 = line.split()
                if vertex_1 not in vertices:
                    vertices.append(vertex_1)
                if vertex_2 not in vertices:
                    vertices.append(vertex_2)
                graph.add_edge(int(vertex_1), int(vertex_2))
        # print(vertices)
        print("nb vertices:", len(vertices))
        return graph
    
    def generate_constraints(self):
        constraints = [[None for _ in range(len(self.graph.nodes()))] for _ in range(len(self.graph.nodes()))]
        for edge in self.graph.edges():
            vertex_1, vertex_2 = edge
            ind_vertex_1 = self.var_to_index[vertex_1]
            ind_vertex_2 = self.var_to_index[vertex_2]
            possible_color_v_1 = []
            possible_color_v_2 = []
            for color_1 in range(self.nb_colors):
                for color_2 in range(self.nb_colors):
                    if color_1 != color_2:
                        possible_color_v_1.append((color_1, color_2))
                        possible_color_v_2.append((color_2, color_1))
            constraints[ind_vertex_1][ind_vertex_2] = possible_color_v_1
            constraints[ind_vertex_2][ind_vertex_1] = possible_color_v_2
        return constraints
    
    def display_sol(self, solution):
        G = self.graph
        node_colors = solution

        # Nombre unique de couleurs nécessaires
        unique_color_indices = set(node_colors.values())
        num_colors = len(unique_color_indices)

        # Générer une palette de couleurs automatique avec `num_colors` couleurs
        color_palette = cm.get_cmap('hsv', num_colors)

        # Associer chaque indice entier à une couleur de la palette
        color_map = {index: color_palette(index) for index in unique_color_indices}

        # Créer la liste de couleurs pour chaque sommet du graphe
        colors = [color_map[node_colors[node]] for node in G.nodes()]

        # Dessiner le graphe
        plt.figure(figsize=(8, 6))
        nx.draw(G, with_labels=True, node_color=colors, node_size=400, font_color='white', font_weight='bold')
        plt.show()
    

class SMALL_COLORING(CSP):
    def __init__(self, edges, nb_colors):
        self.nb_colors = nb_colors
        self.variables = []
        for x, y in edges:
            if x not in self.variables:
                self.variables.append(x)
            if y not in self.variables:
                self.variables.append(y)
        domains = {var: list(range(nb_colors)) for var in self.variables}
        self.var_to_index = {var: i for i, var in enumerate(self.variables)}
        constraints = self.generate_constraints(edges)
        super().__init__(self.variables, domains, constraints)

    def generate_constraints(self, edges):
        constraints = [[None for _ in range(len(self.variables))] for _ in range(len(self.variables))]
        print(constraints)
        for edge in edges:
            vertex_1, vertex_2 = edge
            ind_vertex_1 = self.var_to_index[vertex_1]
            ind_vertex_2 = self.var_to_index[vertex_2]
            possible_color_v_1 = []
            possible_color_v_2 = []
            for color_1 in range(self.nb_colors):
                for color_2 in range(self.nb_colors):
                    if color_1 != color_2:
                        possible_color_v_1.append((color_1, color_2))
                        possible_color_v_2.append((color_2, color_1))
            constraints[ind_vertex_1][ind_vertex_2] = possible_color_v_1
            constraints[ind_vertex_2][ind_vertex_1] = possible_color_v_2

        return constraints
    

project_path = os.getcwd()
data_path = os.path.join(project_path,"instances/coloring")
file_name = "david.col.txt"
file_path = os.path.join(data_path,file_name)

graph = COLORING(file_path, 10)
print(graph.variables)
print(graph.domains)
print(graph.constraints[1][2])
sol = graph.solve(use_ac3=True)
print(sol)
graph.display_sol(sol)




edges = [(1, 2), (1, 3), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5)]
graph = SMALL_COLORING(edges, 3)
print(graph.variables)
print(graph.domains)
print(graph.constraints)
sol = graph.solve(use_ac3=True)
print(sol)