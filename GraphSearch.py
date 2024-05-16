import copy
import PriorityQueue
import Node

class GraphSearch:
    def __init__(self, problem, strategy):
        self.problem = problem
        self.strategy = strategy

    def general_search(self):
        initial_node = Node.Node(self.problem.initial_state)
        explored = set()
        frontier = PriorityQueue.PriorityQueue()
        frontier.put(initial_node, 0)  

        if self.strategy == "IDA_star":
            threshold = float('inf')  
        elif self.strategy == "IDS":
            depth = 0 

        while not frontier.empty():
            node = copy.deepcopy(frontier.get())

            if self.strategy == "steepest":
                current_node = node
                best_neighbor = self.problem.get_best_neighbor(current_node)
                if best_neighbor:
                    frontier.put(best_neighbor, best_neighbor.priority)
                else:
                    return "failure"     
            else:
                if self.problem.goal_test(node.state):
                    return self.get_path(node)

            explored.add(node.state)
            #print(len(explored))
            #print(frontier.lenght())
            for action in self.problem.actions(node.state):
                child_node = copy.deepcopy(self.problem.result(node, action))
                if child_node.state not in explored:
                    frontier.put(child_node, child_node.priority)

                if self.strategy == "IDA_star":
                    if child_node.priority > threshold:
                        return "failure"
                    threshold = min(threshold, child_node.priority)
                elif self.strategy == "IDS":
                    if node.depth > depth:
                        return "failure"
                    depth += 1
                elif self.strategy == "UCS":
                    if node.cost > frontier.elements[0][0]:  
                        return "failure"

        return "failure"


    def get_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))
