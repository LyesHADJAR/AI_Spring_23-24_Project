import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

    def lenght(self):
        return len(self.elements)


class stack:
    def __init__(self):
        self.elements = []
    def clear(self):
        self.elements.clear()
    def get(self):
        item = self.elements[len(self.elements) - 1]
        self.elements.pop(len(self.elements) - 1)
        return item

    def put(self, item,val):
        self.elements.append(item)

    def empty(self):
        return len(self.elements) == 0

    def print(self):
        for i in range(0, len(self.elements)):
            print(self.elements[i])


class queue:
    def __init__(self):
        self.elements = []
    def clear(self):
        self.elements.clear()
    def get(self):
        if not self.empty():
            item = self.elements[0]
            self.elements.pop(0)
            return item

    def put(self, item,val):
        self.elements.append(item)

    def empty(self):
        return len(self.elements) == 0

    def print(self):
        for i in range(0, len(self.elements)):
            print(self.elements[i])
