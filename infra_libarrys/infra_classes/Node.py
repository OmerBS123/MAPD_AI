class Node:
    def __init__(self, x, y, package=None, agent=None):
        self.x = x
        self.y = y
        self.package = package
        self.edges = set()
        self.agent = agent

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x},{self.y})"

    def add_edge(self, edge):
        self.edges.add(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def get_edge_from_node(self, other_node):
        for edge in self.edges:
            if other_node in edge.nodes:
                return edge
        return None

    def get_x_y_coordinate(self):
        return self.x, self.y

    def is_node_destination(self, packages):
        x_y_coordinate = self.get_x_y_coordinate()
        filtered_packages = {package for package in packages if package.get_delivery_x_y() == x_y_coordinate}
        if not filtered_packages:
            return None
        return filtered_packages.pop()
