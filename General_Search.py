import Node
class Search:
    def __init__(self):
        pass

    def general_search(self, problem, frontier):
        explored = set()
        initial_node = Node(problem.initial_state)
        frontier.put(initial_node, 0)

        while not frontier.empty():
            current_node = frontier.get()

            if problem.goal_test(current_node.state):
                return current_node

            explored.add(current_node.state)
            for action in problem.actions(current_node.state):
                child_state = problem.result(current_node.state, action)
                if child_state not in explored:
                    child_node = Node(state=child_state, parent=current_node)
                    child_cost = problem.cost(child_state)
                    frontier.put(child_node, child_cost)#we can chnage the child_cost to the child_node.priority in order to sort the nodes in the frontier according to their priorities)
                    explored.add(child_state)

        return None
