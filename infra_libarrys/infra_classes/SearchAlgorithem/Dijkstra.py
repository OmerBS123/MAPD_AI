import heapq

from infra_libarrys.infra_classes.Wrappers.DistanceNodeWrapper import DistanceNodeWrapper
from infra_libarrys.infra_classes.SearchAlgorithem.SearchAlgorithm import SearchAlgorithm


class Dijkstra(SearchAlgorithm):
    def __init__(self, start_node, env, destination_node=None, agent_packages=None):
        super().__init__(start_node, env, destination_node=destination_node)
        self.distances = {node: float('inf') for node in self.env.nodes}
        self.previous = {node: None for node in self.env.nodes}
        self.heap = []
        self.nodes_with_package = [node for node in self.env.nodes if node.package is not None]
        delivery_point_coordinate = [package.get_delivery_x_y() for package in agent_packages] if agent_packages is not None else []
        self.delivery_point_nodes = [self.env.graph[x][y] for x, y in delivery_point_coordinate]

    def run_search(self):
        if not self.destination_node:
            if not self.nodes_with_package and not self.delivery_point_nodes:
                return None, None

        heapq.heappush(self.heap, DistanceNodeWrapper(0, self.start_node))

        self.distances[self.start_node] = 0

        while self.heap:
            node_wrapper = heapq.heappop(self.heap)
            current_distance, current_node = node_wrapper.distance, node_wrapper.node

            for edge in current_node.edges:
                neighbor_node = edge.get_neighbor_node(current_node)
                new_distance = self.distances[current_node] + edge.weight

                if new_distance < self.distances[neighbor_node]:
                    self.distances[neighbor_node] = new_distance
                    self.previous[neighbor_node] = current_node
                    heapq.heappush(self.heap, DistanceNodeWrapper(new_distance, neighbor_node))

        if self.destination_node is None:
            self.destination_node = self.get_min_distance_package_node()

        shortest_path = self.get_shortest_path()

        return shortest_path, self.distances

    def get_min_distance_package_node(self):
        all_destinations = self.nodes_with_package + self.delivery_point_nodes
        return min(all_destinations, key=lambda node: self.distances[node])

    def get_shortest_path(self):
        path = []
        current_node = self.destination_node

        while current_node:
            path.append(current_node)
            current_node = self.previous[current_node]

        return list(reversed(path))
