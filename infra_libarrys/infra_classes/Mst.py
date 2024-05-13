import heapq

from infra_libarrys.infra_classes.Wrappers.MstWrapper import MstWrapper


class Mst:
    def __init__(self, clique):
        self.clique = clique
        self.mst_edges = set()

    def prim(self, start_node):
        visited = set()
        heap = [MstWrapper(0, start_node, None)]  # (weight, current_node, previous_node)

        while heap:
            weight, current_node, previous_node = heapq.heappop(heap).unpack_wrapper()

            if current_node not in visited:
                visited.add(current_node)

                if previous_node is not None:
                    edge = current_node.get_edge_from_node(previous_node)
                    self.mst_edges.add(edge)

                for neighbor_edge in current_node.edges:
                    neighbor_node = neighbor_edge.get_neighbor_node(current_node)
                    if neighbor_node not in visited:
                        heapq.heappush(heap, MstWrapper(neighbor_edge.weight, neighbor_node, current_node))

    def create_mst(self):
        start_node = next(iter(self.clique.nodes))  # Start from any node in the clique
        self.prim(start_node)

    def get_mst_weight(self):
        return sum([edge.weight for edge in self.mst_edges])
