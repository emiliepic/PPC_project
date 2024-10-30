import numpy as np
import matplotlib.pyplot as plt
from model import CSP

class N_QUEENS(CSP):
    def __init__(self, n):
        self.n = n
        variables = list(range(n))
        domains = {var: list(range(n)) for var in variables}
        constraints = self.generate_constraints()
        super().__init__(variables, domains, constraints)
    
    def generate_constraints(self):
        constraints = [[None for _ in range(self.n)] for _ in range(self.n)]

        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    possible_positions = []
                    for k in range(self.n):
                        for l in range(self.n):
                            # Les dames ne doivent pas être sur la même ligne, la même colonne ou la même diagonale
                            if k != l and abs(i - j) != abs(k - l):
                                possible_positions.append((k, l))
                    constraints[i][j] = possible_positions

        return constraints
    
    def solution_printer(self, solution):
        # Créer un tableau vide de n x n pour l'échiquier
        damier = [['.' for _ in range(self.n)] for _ in range(self.n)]
        
        # Placer les dames sur le damier en fonction de la solution
        for ligne, colonne in solution.items():
            damier[ligne][colonne] = '♕'  # Utilisation du caractère Unicode pour la dame (♕)
        
        # Afficher le damier
        for ligne in damier:
            print(' '.join(ligne))
        print()  # Nouvelle ligne à la fin pour la lisibilité
    
    def solution_display(self, solution):
        # Créer une figure et des axes avec matplotlib
        fig, ax = plt.subplots()
        
        # Créer un tableau vide de n x n pour l'échiquier
        damier = np.zeros((self.n, self.n))
        
        # Placer les dames sur le damier en fonction de la solution
        for ligne, colonne in solution.items():
            damier[ligne][colonne] = 1  # 1 représente une dame
        
        # Afficher le damier en utilisant imshow
        ax.imshow(damier, cmap="Blues")
        
        # Ajouter les dames avec le caractère Unicode pour la dame (♕)
        for ligne, colonne in solution.items():
            ax.text(colonne, ligne, '♕', ha='center', va='center', fontsize=20, color='black')
        
        # Configurer les axes
        ax.set_xticks(np.arange(self.n))
        ax.set_yticks(np.arange(self.n))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xticks(np.arange(-.5, self.n, 1), minor=True)
        ax.set_yticks(np.arange(-.5, self.n, 1), minor=True)
        ax.grid(which="minor", color='black', linestyle='-', linewidth=2)
        ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
        
        # Afficher la figure
        plt.show()
        

        


