import time
import random
import copy


class CSP:
    def __init__(self, variables, domains, constraints, var_heuristic="static", val_heuristic="static"):
        # Initialisation des variables, domaines, contraintes et heuristiques pour le problème CSP
        self.variables = variables
        self.var_to_index = {var: i for i, var in enumerate(variables)}  # Associer chaque variable à un index
        self.domains = domains  # Domaines de chaque variable
        self.constraints = constraints  # Contraintes entre les variables
        self.var_heuristic = var_heuristic  # Heuristique de sélection des variables
        self.val_heuristic = val_heuristic  # Heuristique de sélection des valeurs

    def is_consistent(self, var, value, assignment):
        # Vérifier si l'assignation de la valeur à la variable est consistante avec les contraintes existantes
        for other_var in assignment:
            if other_var != var:
                other_value = assignment[other_var]
                ind_var = self.var_to_index[var]
                ind_other_var = self.var_to_index[other_var]
                if self.constraints[ind_var][ind_other_var] is not None:
                    if (value, other_value) not in self.constraints[ind_var][ind_other_var]:
                        return False  # Incohérence détectée
        return True

    def select_unassigned_variable(self, assignment):
        # Sélectionner la prochaine variable non assignée en fonction de l'heuristique choisie
        unassigned_vars = [v for v in self.variables if v not in assignment]

        if self.var_heuristic == "static":
            return unassigned_vars[0]  # Retourne la première variable non assignée
        elif self.var_heuristic == "MRV":
            # Minimum Remaining Values (MRV): Choisir la variable avec le moins de valeurs possibles dans son domaine
            return min(unassigned_vars, key=lambda var: len([value for value in self.domains[var] if self.is_consistent(var, value, assignment)]))
        elif self.var_heuristic == "degree":
            # Degree Heuristic: Choisir la variable avec le plus de contraintes sur les autres variables non assignées
            return max(unassigned_vars, key=lambda var: sum(1 for other_var in self.variables if other_var != var and other_var not in assignment and self.constraints[self.var_to_index[var]][self.var_to_index[other_var]] is not None))
        else:
            raise ValueError("Heuristique non reconnue. Choisissez entre 'static', 'MRV', ou 'degree'.")

    def order_domain_values(self, var, assignment, domains=None):
        # Ordonner les valeurs du domaine de la variable selon l'heuristique de choix des valeurs
        if self.val_heuristic == "static":
            return domains[var] if domains is not None else self.domains[var]
        elif self.val_heuristic == "inverse":
            return sorted(domains[var], reverse=True) if domains is not None else sorted(self.domains[var], reverse=True)
        elif self.val_heuristic == "random":
            values = list(domains[var]) if domains is not None else list(self.domains[var])
            random.shuffle(values)
            return values
        elif self.val_heuristic == "LCV":
            # Least Constraining Value (LCV): Trie en fonction du nombre de valeurs compatibles restantes pour les voisins
            return sorted(domains[var], key=lambda val: self.count_conflicts(var, val, assignment)) if domains is not None else sorted(self.domains[var], key=lambda val: self.count_conflicts(var, val, assignment))
        else:
            raise ValueError("Heuristique de valeur non reconnue.")

    def count_conflicts(self, var, value, assignment):
        # Compte les conflits introduits par l'attribution de 'value' à 'var'
        count = 0
        ind_var = self.var_to_index[var]
        for other_var in self.variables:
            if other_var != var and other_var not in assignment:
                ind_other_var = self.var_to_index[other_var]
                if self.constraints[ind_var][ind_other_var] is not None:
                    count += sum(1 for val in self.domains[other_var] if (value, val) not in self.constraints[ind_var][ind_other_var])
        return count

    def backtrack(self, assignment={}, domains=None, use_ac3_meanwhile=True, fc=False, time_limit=None, time_start=None):
        # Algorithme de recherche par backtracking pour trouver une solution
        if len(assignment) == len(self.variables):
            return assignment  # Retourne l'assignation si toutes les variables sont assignées

        var = self.select_unassigned_variable(assignment)
        search_domain = self.order_domain_values(var, assignment, domains)
        new_domains = self.domains.copy()

        for value in search_domain:
            if time_limit is not None and time.time() - time_start > time_limit:
                print("time limit reached")
                return None
            if self.is_consistent(var, value, assignment):
                if fc:
                    res_fc = self.forward_checking(var, value, assignment, domains)
                    if res_fc is None:
                        continue
                    new_domains = res_fc
                if use_ac3_meanwhile:
                    res_ac = self.ac3_meanwhile(var, value, assignment, domains)
                    if not res_ac:
                        continue
                    new_domains = res_ac
                assignment[var] = value  # Assigner la valeur à la variable
                if fc or use_ac3_meanwhile:
                    result = self.backtrack(assignment, new_domains, fc=fc, use_ac3_meanwhile=use_ac3_meanwhile, time_limit=time_limit, time_start=time_start)
                else:
                    result = self.backtrack(assignment, domains, fc=fc, time_limit=time_limit, time_start=time_start)
                if result is not None:
                    return result
                del assignment[var]  # Annuler l'assignation si cela ne mène pas à une solution

        return None

    def forward_checking(self, var, value, assignment, domains):
        # Appliquer le forward checking pour réduire les domaines des variables non assignées
        new_domains = domains.copy()
        for other_var in self.variables:
            if other_var not in assignment and other_var != var:
                ind_var = self.var_to_index[var]
                ind_other_var = self.var_to_index[other_var]
                if self.constraints[ind_var][ind_other_var] is not None:
                    new_domains[other_var] = [val for val in new_domains[other_var] if (value, val) in self.constraints[ind_var][ind_other_var]]
                    if len(new_domains[other_var]) == 0:
                        return None  # Retourne None si aucun domaine possible n'est trouvé
        return new_domains

    def ac3(self, time_limit=None, time_start=None):
        # Implémenter l'algorithme AC3 pour réduire les domaines des variables
        queue = [(x, y) for x in self.variables for y in self.variables if self.constraints[self.var_to_index[x]][self.var_to_index[y]] is not None]
        while queue:
            if time_limit is not None and time.time() - time_start > time_limit:
                print("time limit reached")
                return None
            x, y = queue.pop(0)
            ind_x = self.var_to_index[x]
            ind_y = self.var_to_index[y]
            for i in self.domains[x]:
                if self.not_supported(x, y, i):
                    self.domains[x].remove(i)  # Supprimer la valeur du domaine si elle n'est pas supportée
                    for z in self.variables:
                        if z != x:
                            ind_z = self.var_to_index[z]
                            if self.constraints[ind_x][ind_z] is not None:
                                self.constraints[ind_x][ind_z] = [(a, b) for a, b in self.constraints[ind_x][ind_z] if a != i]
                                self.constraints[ind_z][ind_x] = [(a, b) for a, b in self.constraints[ind_z][ind_x] if b != i]
                    arc_to_add = [(z, x) for z in self.variables if z != x]
                    queue.extend([arc for arc in arc_to_add if arc not in queue])
                if len(self.domains[x]) == 0:
                    return False
        return True
    
    def ac3_meanwhile(self, var, value, assignment, domains):
        # Appliquer AC3 pendant l'assignation pour ajuster les domaines
        new_domains = copy.deepcopy(domains)
        new_domains[var] = [value]
        new_constraints = copy.deepcopy(self.constraints)
        ind_var = self.var_to_index[var]
        for other_var in self.variables:
            if var != other_var:
                ind_other_var = self.var_to_index[other_var]
                if self.constraints[ind_var][ind_other_var] is not None:
                    new_constraints[ind_var][ind_other_var] = [(a, b) for a, b in self.constraints[ind_var][ind_other_var] if a in new_domains[var]]
                    if len(new_constraints[ind_var][ind_other_var]) == 0:
                        return False
                    new_constraints[ind_other_var][ind_var] = [(a, b) for a, b in self.constraints[ind_other_var][ind_var] if b in new_domains[var]]
                    if len(new_constraints[ind_other_var][ind_var]) == 0:
                        return False
        queue = [(x, y) for x in self.variables for y in self.variables if new_constraints[self.var_to_index[x]][self.var_to_index[y]] is not None]
        while queue:
            x, y = queue.pop(0)
            ind_x = self.var_to_index[x]
            ind_y = self.var_to_index[y]
            for i in new_domains[x]:
                if self.not_supported(x, y, i):
                    new_domains[x].remove(i)
                    for z in self.variables:
                        if z != x:
                            ind_z = self.var_to_index[z]
                            if new_constraints[ind_x][ind_z] is not None:
                                new_constraints[ind_x][ind_z] = [(a, b) for a, b in new_constraints[ind_x][ind_z] if a != i]
                                new_constraints[ind_z][ind_x] = [(a, b) for a, b in new_constraints[ind_z][ind_x] if b != i]
                                if len(new_constraints[ind_x][ind_z]) == 0 or len(new_constraints[ind_z][ind_x]) == 0:
                                    return False
                    arc_to_add = [(z, x) for z in self.variables if z != x]
                    queue.extend([arc for arc in arc_to_add if arc not in queue])
                if len(new_domains[x]) == 0:
                    return False
        return new_domains

    def not_supported(self, x, y, i):
        # Vérifier si une valeur n'est pas supportée par les contraintes
        ind_x = self.var_to_index[x]
        ind_y = self.var_to_index[y]
        if self.constraints[ind_x][ind_y] is not None:
            if not any([(i, j) in self.constraints[ind_x][ind_y] for j in self.domains[y]]):
                return True
        return False

    def solve(self, use_ac3=True, use_ac3_meanwhile=False, fc=False, time_limit=None):
        # Résoudre le problème CSP avec les options spécifiées
        time_start = time.time()

        if use_ac3:
            result_ac3 = self.ac3(time_limit=time_limit, time_start=time_start)
            if result_ac3 is None or not result_ac3:
                return "No solution found"
        print("AC3 done after", time.time() - time_start)
        assignment = {}
        result = self.backtrack(assignment=assignment, domains=self.domains.copy(), use_ac3_meanwhile=use_ac3_meanwhile, fc=fc, time_limit=time_limit, time_start=time_start)
        if result is None:
            return "No solution found"
        else:
            return result
