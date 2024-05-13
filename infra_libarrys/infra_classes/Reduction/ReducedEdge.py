from infra_libarrys.consts_and_enums.EdgeConsts import DEFAULT_WEIGHT


class ReducedEdge:
    def __init__(self, left_node, right_node, weight=DEFAULT_WEIGHT, original_object=None):
        self.original_object = original_object
        self.weight = weight
        self.nodes = {right_node, left_node}

    def get_neighbor_node(self, curr_node):
        return (self.nodes - {curr_node}).pop()
