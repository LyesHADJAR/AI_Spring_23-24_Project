class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables  # List of variables
        self.domains = domains   # Dictionary {Variable: List of possible values}
        self.constraints = constraints  #Dictionary {Variable: List of constraint functions}

    def is_consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint(assignment):  # Assignment is  a dictionary { Variable : assigned or not (boolean)}
                return False
        return True

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable
        return None

    def backtracking_search(self):
        return self.backtrack({}) # Dictionary of assignment 

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.domains[var]:
            assignment[var] = value
            if self.is_consistent(var, assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            assignment.pop(var, None)

        return None
