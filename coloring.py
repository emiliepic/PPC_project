import networkx as nx
import os
from model import CSP
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def read_file_col(file_path):
    # Lire le fichier de description du graphe et construire le graphe avec NetworkX
    with open(file_path, 'r') as file:
        lines = file.readlines()
    vertices = []
    graph = nx.Graph()
    for line in lines:
        if line.startswith('e'):
            # Ajouter les arêtes du graphe à partir des lignes commençant par 'e'
            _, vertex_1, vertex_2 = line.split()
            if vertex_1 not in vertices:
                vertices.append(vertex_1)
            if vertex_2 not in vertices:
                vertices.append(vertex_2)
            graph.add_edge(int(vertex_1), int(vertex_2))
    print("nb vertices:", len(vertices))
    return graph

class COLORING(CSP):
    def __init__(self, file_path, nb_colors, var_heuristic="static", val_heuristic="static"):
        # Initialisation du problème de coloration en lisant le graphe et en définissant les contraintes
        self.graph = read_file_col(file_path)
        print(self.graph)
        self.nb_colors = nb_colors
        variables = list(self.graph.nodes())
        domains = {var: list(range(nb_colors)) for var in variables}  # Chaque variable a un domaine de couleurs
        self.var_to_index = {var: i for i, var in enumerate(variables)}
        constraints = self.generate_constraints()  # Générer les contraintes de coloration
        super().__init__(variables, domains, constraints, var_heuristic, val_heuristic)
    
    def generate_constraints(self):
        # Générer les contraintes de non-adjacence pour la coloration du graphe
        constraints = [[None for _ in range(len(self.graph.nodes()))] for _ in range(len(self.graph.nodes()))]
        for edge in self.graph.edges():
            vertex_1, vertex_2 = edge
            ind_vertex_1 = self.var_to_index[vertex_1]
            ind_vertex_2 = self.var_to_index[vertex_2]
            possible_color_v_1 = []
            possible_color_v_2 = []
            for color_1 in range(self.nb_colors):
                for color_2 in range(self.nb_colors):
                    if color_1 != color_2:  # Les sommets adjacents ne doivent pas avoir la même couleur
                        possible_color_v_1.append((color_1, color_2))
                        possible_color_v_2.append((color_2, color_1))
            constraints[ind_vertex_1][ind_vertex_2] = possible_color_v_1
            constraints[ind_vertex_2][ind_vertex_1] = possible_color_v_2
        return constraints
    
    def display_sol(self, solution):
        # Afficher la solution de la coloration du graphe
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
    
    def is_feasible(self, solution):
        # Vérifier si une solution donnée est faisable (i.e., aucun sommet adjacent n'a la même couleur)
        for edge in self.graph.edges():
            vertex_1, vertex_2 = edge
            if solution[vertex_1] == solution[vertex_2]:
                return False
        return True
    

class SMALL_COLORING(CSP):
    def __init__(self, edges, nb_colors):
        # Initialiser un petit problème de coloration avec une liste d'arêtes spécifiée
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
        # Générer les contraintes de non-adjacence pour la coloration du graphe
        constraints = [[None for _ in range(len(self.variables))] for _ in range(len(self.variables))]
        for edge in edges:
            vertex_1, vertex_2 = edge
            ind_vertex_1 = self.var_to_index[vertex_1]
            ind_vertex_2 = self.var_to_index[vertex_2]
            possible_color_v_1 = []
            possible_color_v_2 = []
            for color_1 in range(self.nb_colors):
                for color_2 in range(self.nb_colors):
                    if color_1 != color_2:  # Les sommets adjacents ne doivent pas avoir la même couleur
                        possible_color_v_1.append((color_1, color_2))
                        possible_color_v_2.append((color_2, color_1))
            constraints[ind_vertex_1][ind_vertex_2] = possible_color_v_1
            constraints[ind_vertex_2][ind_vertex_1] = possible_color_v_2

        return constraints
    

def dichotomic_search(file_path, use_ac3=True, fc=False, var_heuristic="static", val_heuristic="static", time_limit=20):
    # Effectuer une recherche dichotomique pour trouver le nombre minimal de couleurs nécessaires
    graph = read_file_col(file_path)
    nb_max_colors = len(graph.nodes())
    nb_min_colors = 1
    nb_colors = (nb_max_colors + nb_min_colors) // 2
    
    while nb_max_colors - nb_min_colors > 1:
        print("nb_min_colors", nb_min_colors)
        print("nb_max_colors", nb_max_colors)
        print("nb_colors", nb_colors)
        graph = COLORING(file_path, nb_colors, var_heuristic, val_heuristic)
        sol = graph.solve(use_ac3=use_ac3, fc=fc, time_limit=time_limit)  # Résoudre le problème avec le nombre actuel de couleurs
        if sol == "No solution found":
            nb_min_colors = nb_colors  # Pas de solution trouvée, augmenter le nombre minimum de couleurs
        else:
            nb_max_colors = nb_colors  # Solution trouvée, réduire le nombre maximum de couleurs
        nb_colors = (nb_max_colors + nb_min_colors) // 2
        
    return nb_max_colors  # Retourner le nombre minimal de couleurs trouvées
