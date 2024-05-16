import copy
from DataStructures import PriorityQueue, stack, queue
import Node


class GraphSearch:
    def __init__(self, problem, strategy):
        self.problem = problem
        self.strategy = strategy

    def general_search(self):
        initial_node = Node.Node(self.problem.initial_state)
        explored = set()

        frontier = PriorityQueue()

        if self.strategy == "IDA_star":
            threshold = float("inf")
        elif self.strategy == "IDS":
            depth = 0
            frontier = stack()
        elif self.strategy == "BFS":
            depth = 0
            frontier = queue()
        frontier.put(initial_node, 0)
        i = 0

        while not frontier.empty():

            # print((frontier).lenght())
            # print(len(frontier.elements))
           # print(len(frontier.elements))
            node = copy.deepcopy(frontier.get())
            # print(node)
            # print("==================")
            # print("unused needed=")

            # print(node.state.getTotalLandUsed())
            # print(node.state.getUnusedLand())
            # print("==================")

            # print("unused land is:")
            # print(node.state.getUnusedLand())
            # print("heuristic is ")
            # print(node.priority)
            # if i<2:
            #             print("-----------------")
            #             print(node.state.total_production)
            #             i+=1
            # print((frontier).lenght())
            # print("parent")
            # print(node.state.total_production["wheat"])
            if self.strategy == "steepest":
                current_node = node
                best_neighbor = self.problem.get_best_neighbor(current_node)
                if best_neighbor != None:

                    frontier.put(best_neighbor, best_neighbor.priority)
                else:
                    return node
            else:
                if self.problem.goal_test(node.state):
                    return (node)

                explored.add(node.state)
                # print(len(frontier.elements))
                for action in self.problem.actions(node.state):

                    child_node = copy.deepcopy(
                        self.problem.result(node, action))
                    # if i<2 and child_node!=None:
                    #     print("-----------------")
                    #     print("child")
                    #     print(child_node.state.total_production)
                    #     print(child_node.state.getUnusedLand())
                    #     i+=1
                    if child_node == None:
                        continue
                    if child_node.state not in explored:
                        frontier.put(copy.deepcopy(child_node),
                                     child_node.priority)

                    if self.strategy == "IDA_star":
                        if child_node.priority > threshold:
                            print("STOP==========================================")
                            frontier.clear()
                            frontier.put(initial_node, 0)
                            threshold = min(threshold, child_node.priority)
                    elif self.strategy == "IDS":
                        if node.depth > depth:
                            frontier.clear()
                            frontier.put(initial_node, 0)
                            depth += 1
                            continue

        return "failure"

    def get_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))
