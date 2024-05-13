from infra_libarrys.infra_classes.Edge import Edge


class Clique:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, node1, node2, weight, old_to_new_nodes_dict):
        new_node1 = old_to_new_nodes_dict[node1]
        new_node2 = old_to_new_nodes_dict[node2]
        edge = Edge(nodes={new_node1, new_node2}, weight=weight)
        self.edges.add(edge)
        new_node1.edges.add(edge)
        new_node2.edges.add(edge)
