from infra_libarrys.infra_classes.Reduction.ReducedEdge import ReducedEdge
from infra_libarrys.infra_classes.Reduction.ReducedNode import ReducedNode


class ReducedEnv:
    def __init__(self, original_env):
        self.nodes = set()
        self.edges = set()
        self.original_to_reduced_mapping = {}
        self.reduced_to_original_mapping = {}

        # Connect ReducedNodes based on original Edges
        for curr_node in original_env.nodes:
            new_node = ReducedNode(curr_node, package=False, old_edge=False)
            self.original_to_reduced_mapping[curr_node] = new_node
            self.reduced_to_original_mapping[new_node] = curr_node
            self.nodes.add(new_node)
            for curr_edge in curr_node.edges:
                if curr_edge.is_fragile:
                    self.reduce_fragile_edge(curr_edge, new_node)

        for old_edge in original_env.edges_dict.values():
            if not old_edge.is_fragile:
                self.reduce_regular_edge(old_edge)

    def reduce_fragile_edge(self, fragile_edge, connected_new_node):
        if fragile_edge in self.original_to_reduced_mapping:
            new_reduced_node = self.original_to_reduced_mapping[fragile_edge]
        else:
            new_reduced_node = ReducedNode(fragile_edge, package=True, old_edge=True)
            self.nodes.add(new_reduced_node)
        new_reduced_edge = ReducedEdge(left_node=connected_new_node, right_node=new_reduced_node, weight=0)
        self.edges.add(new_reduced_edge)
        new_reduced_node.add_reduced_edge(new_reduced_edge)
        connected_new_node.add_reduced_edge(new_reduced_edge)

    def reduce_regular_edge(self, old_edge):
        node_1, node_2 = old_edge.nodes
        reduced_node_1 = self.original_to_reduced_mapping[node_1]
        reduced_node_2 = self.original_to_reduced_mapping[node_2]
        new_reduced_edge = ReducedEdge(original_object=old_edge, left_node=reduced_node_1, right_node=reduced_node_2, weight=old_edge.weight)
        reduced_node_1.add_reduced_edge(new_reduced_edge)
        reduced_node_2.add_reduced_edge(new_reduced_edge)
        self.original_to_reduced_mapping[old_edge] = new_reduced_edge
        self.reduced_to_original_mapping[new_reduced_edge] = old_edge
        self.edges.add(new_reduced_edge)
