import random

class CSP:
    def __init__(self, variables, domains, constraints, var_heuristic="static", val_heuristic="static"):
        self.variables = variables
        self.var_to_index = {var: i for i, var in enumerate(variables)}
        self.domains = domains
        self.constraints = constraints # array of list of tuples , position [i][j] is a list of tuples that are compatible for variable i and j
        self.var_heuristic = var_heuristic
        self.val_heuristic = val_heuristic
    
    def is_consistent(self, var, value, assignment):
        # Vérifier si l'assignation est consistante avec les contraintes existantes
        for other_var in assignment:
            if other_var != var:
                other_value = assignment[other_var]
                # Vérifier si la valeur assignée est compatible avec les autres
                ind_var = self.var_to_index[var]
                ind_other_var = self.var_to_index[other_var]
                if self.constraints[ind_var][ind_other_var] is not None:
                    if (value, other_value) not in self.constraints[ind_var][ind_other_var]:
                        return False
        return True

    def select_unassigned_variable(self, assignment):
        #Sélectionne la prochaine variable non assignée en fonction de l'heuristique choisie
        unassigned_vars = [v for v in self.variables if v not in assignment]

        if self.var_heuristic == "static":
            return unassigned_vars[0]  # Sélection de la première variable dans l'ordre statique
        elif self.var_heuristic == "MRV":
            # Minimum Remaining Values (MRV): Choisir la variable avec le moins de valeurs possibles dans son domaine
            return min(unassigned_vars,
                       key=lambda var: len([value for value in self.domains[var] if self.is_consistent(var, value, assignment)]))
        elif self.var_heuristic == "degree":
            # Degree Heuristic: Choisir la variable avec le plus de contraintes sur les autres variables non assignées
            return max(unassigned_vars, key=lambda var: sum(
                1 for other_var in self.variables if other_var != var and other_var not in assignment))
        else:
            raise ValueError("Heuristique non reconnue. Choisissez entre 'static', 'MRV', ou 'degree'.")

    def order_domain_values(self, var):
        """Ordre les valeurs possibles de la variable selon l'heuristique de choix des valeurs."""
        if self.val_heuristic == "static":
            return self.domains[var]
        elif self.val_heuristic == "inverse":
            return sorted(self.domains[var], reverse=True)
        elif self.val_heuristic == "random":
            values = list(self.domains[var])
            random.shuffle(values)
            return values
        else:
            raise ValueError("Heuristique non reconnue. Choisissez entre 'static', 'inverse', ou 'random'.")


    def backtrack(self, assignment={}):
        # Si toutes les variables sont assignées, retourner l'assignation
        # print("assignment", assignment)
        if len(assignment) == len(self.variables):
            return assignment
        # Sélectionner une variable non assignée
        unassigned_vars = self.select_unassigned_variable(assignment)
        #  print("unassigned_vars", unassigned_vars)
        var = unassigned_vars
        # Essayer chaque valeur du domaine de la variable
        search_domain = self.order_domain_values(var)
        for value in search_domain:
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
    
    def ac3(self):
        # Implémenter l'algorithme AC3
        queue = [(x, y) for x in self.variables for y in self.variables if self.constraints[self.var_to_index[x]][self.var_to_index[y]] is not None]
        print(len(queue))
        # print("les arcs a traiter sont", queue)
        # print("les contraintes sont", self.constraints)

        while queue:
            x, y = queue.pop(0)
            ind_x = self.var_to_index[x]
            ind_y = self.var_to_index[y]
            # print("on enleve de queue l'arc", x, y)
            for i in self.domains[x]:
                if self.not_supported(x, y, i):
                    self.domains[x].remove(i)
                    # print(f"on enleve {i} du domaine de {x}")
                    for z in self.variables:
                        if z != x:
                            ind_z = self.var_to_index[z]
                            if self.constraints[ind_x][ind_z] is not None:
                                self.constraints[ind_x][ind_z] = [(a, b) for a, b in self.constraints[ind_x][ind_z] if a != i]
                                self.constraints[ind_z][ind_x] = [(a, b) for a, b in self.constraints[ind_z][ind_x] if b != i]
                    # print("i", i, self.constraints[ind_x][ind_y])
                    # on ajoute les arcs si ils n'y sont pas deja
                    arc_to_add = [(z, x) for z in self.variables if z != x]
                    queue.extend([arc for arc in arc_to_add if arc not in queue])
                    # print(f"les contraintes pour l'arc {x, y} sont", self.constraints[ind_x][ind_y])
                    # print("on ajoute les arcs", [arc for arc in arc_to_add if arc not in queue], "de", [(z, x) for z in self.variables if z != x])
                    # print("les arcs a traiter sont", queue)
                    # print("les nouvelles contraintes sont", self.constraints)
                if len(self.domains[x]) == 0:
                    return False
                
        return True
    
    def not_supported(self, x, y, i):
        ind_x = self.var_to_index[x]
        ind_y = self.var_to_index[y]
        if self.constraints[ind_x][ind_y] is not None:
            if not any([(i, j) in self.constraints[ind_x][ind_y] for j in self.domains[y]]):
                return True
        return False
    
     
    def solve(self, use_ac3=True):
        # Appliquer AC3 pour réduire les domaines
        if use_ac3:
            if not self.ac3():
                return "No solution found"
        assignment = {}
        result = self.backtrack(assignment=assignment)
        if result is None:
            return "No solution found"
        else:
            return result

