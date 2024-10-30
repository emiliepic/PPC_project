import numpy as np
import matplotlib.pyplot as plt

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints # array of list of tuples , position [i][j] is a list of tuples that are compatible for variable i and j
    
    def is_consistent(self, var, value, assignment):
        # Vérifier si l'assignation est consistante avec les contraintes existantes
        for other_var in assignment:
            if other_var != var:
                other_value = assignment[other_var]
                # Vérifier si la valeur assignée est compatible avec les autres
                if (value, other_value) not in self.constraints[var][other_var]:
                    return False
        return True

    def backtrack(self, assignment={}):
        # Si toutes les variables sont assignées, retourner l'assignation
        # print("assignment", assignment)
        if len(assignment) == len(self.variables):
            return assignment
        
        # Sélectionner une variable non assignée
        unassigned_vars = [v for v in self.variables if v not in assignment]
        var = unassigned_vars[0]
        
        # Essayer chaque valeur du domaine de la variable
        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                # Assigner la valeur à la variable
                assignment[var] = value
                # Continuer la recherche récursive
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                # Si cela ne mène pas à une solution, annuler l'assignation
                del assignment[var]
        
        return None

    def solve(self):
        result = self.backtrack()
        if result is None:
            return "No solution found"
        else:
            return result

class N_QUEENS(CSP):
    def __init__(self, n):
        self.n = n
        variables = list(range(n))
        domains = {var: list(range(n)) for var in variables}
        constraints = N_QUEENS.generate_constraints(n)
        super().__init__(variables, domains, constraints)
    
    def generate_constraints(n):
        constraints = [[[] for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                possible_positions = []
                for k in range(n):
                    for l in range(n):
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
        

        
n = 4
n_queens = N_QUEENS(n)
print(n_queens.variables)
print(n_queens.domains)
print(n_queens.constraints[1][2])
sol = n_queens.solve()
print(sol)
n_queens.solution_printer(sol)
n_queens.solution_display(sol)

