class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def is_consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint(assignment):
                return False
        return True

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable
        return None

    def backtracking_search(self):
        return self.backtrack({})

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
