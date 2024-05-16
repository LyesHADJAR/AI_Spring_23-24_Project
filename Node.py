class Node:
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
        return self.priority>other.priority
