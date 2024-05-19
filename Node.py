class Node:
    """
    Represents a node in a search algorithm.

    Attributes:
        state: The state associated with the node.
        parent: The parent node of the current node.
        action: The action taken to reach the current node.
        cost: The cost to reach the current node.
        priority: The priority of the node.
        depth: The depth of the node in the search tree.
    """

    def __init__(self, state, parent=None, action=None, cost=0, priority=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.priority = priority
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

    def __gt__(self, other):
        return self.priority > other.priority
