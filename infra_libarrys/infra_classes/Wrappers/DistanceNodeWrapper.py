class DistanceNodeWrapper:
    def __init__(self, distance, node):
        self.node = node
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance
