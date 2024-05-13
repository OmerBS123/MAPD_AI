from infra_libarrys.consts_and_enums.EdgeConsts import DEFAULT_WEIGHT


class Edge:
    def __init__(self, nodes=None, is_fragile=False, weight=DEFAULT_WEIGHT):
        self.nodes = nodes
        self.is_fragile = is_fragile
        self.weight = weight

    def __eq__(self, other):
        return self.nodes == other.nodes

    def __hash__(self):
        return hash(frozenset(self.nodes))

    def __str__(self):
        node1, node2 = self.nodes
        return f"({node1},{node2}"

    def add_nodes(self, node1, node2):
        self.nodes = {node1, node2}

    def get_neighbor_node(self, curr_node):
        node_singleton = self.nodes - {curr_node}
        return node_singleton.pop()

    def remove_self_from_env(self, env):
        coordinate_tuple = []
        for node in self.nodes:
            node.remove_edge(edge=self)
            x, y = node.get_x_y_coordinate()
            coordinate_tuple.extend([x, y])

        coordinate_tuple = tuple(coordinate_tuple)
        switched_coordinate_tuple = (coordinate_tuple[2], coordinate_tuple[3], coordinate_tuple[0], coordinate_tuple[1])
        env.fragile_edges = env.fragile_edges - {coordinate_tuple, switched_coordinate_tuple}
        env.blocked_edges.add(coordinate_tuple)

    def get_edge_coordinate(self):
        node1, node2 = self.nodes
        x1, y1 = node1.get_x_y_coordinate()
        x2, y2 = node2.get_x_y_coordinate()
        return x1, y1, x2, y2
