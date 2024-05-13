from itertools import combinations
from copy import copy

from infra_libarrys.infra_classes.Agent.Agent import Agent
from infra_libarrys.infra_classes.Clique import Clique
from infra_libarrys.infra_classes.Node import Node
from infra_libarrys.infra_classes.Edge import Edge
from infra_libarrys.infra_classes.SearchAlgorithem.Dijkstra import Dijkstra


class Env:
    def __init__(self, width, height, agents_list=None, blocked_edges=None, fragile_edges=None, package_appear_dict=None, package_disappear_dict=None, start_time=0):
        self.package_appear_dict = package_appear_dict
        self.package_disappear_dict = package_disappear_dict
        self.width = width
        self.height = height
        self.graph = [[Node(x, y) for y in range(height + 1)] for x in range(width + 1)]
        self.nodes = {node for row in self.graph for node in row}
        self.edges_dict = {}
        self.blocked_edges = blocked_edges if blocked_edges is not None else set()
        self.fragile_edges = fragile_edges if fragile_edges is not None else set()
        self.package_points = {node for node in self.nodes if node.package is not None}
        self.agent_nodes = [node for node in self.nodes if node.agent is not None]
        self.delivery_points = self.get_delivery_nodes()
        self.update_packages_state_if_needed(start_time)
        self.create_all_edges()
        self.agents_list = agents_list

    def __copy__(self):
        copy_env = Env(self.width, self.height, self.blocked_edges, self.fragile_edges)

        old_package_created = set()
        copy_package_created = set()
        self.copy_packages(copy_env, old_package_created, copy_package_created)

        self.copy_package_appear_dict(copy_env, old_package_created, copy_package_created)

        self.copy_package_disappear_dict(copy_env, copy_package_created)

        delivery_coordinates = {node.get_x_y_coordinate() for node in self.delivery_points}
        copy_env.delivery_points = {copy_env.graph[x][y] for x, y in delivery_coordinates}

        self.copy_agents(copy_env, copy_package_created)

        self.copy_agent_list(copy_env)

        return copy_env

    def __eq__(self, other):
        cond1 = self.package_points == other.package_points
        cond2 = self.delivery_points == other.delivery_points
        return cond1 and cond2

    def copy_packages(self, copy_env, old_package_created, copy_package_created):
        package_coordinate = {node.get_x_y_coordinate() for node in self.package_points}
        agent_packages = {package for node in self.agent_nodes for package in node.agent.packages}
        copy_env.package_points = {copy_env.graph[x][y] for x, y in package_coordinate}

        for package_node in self.package_points:
            package_copy = copy(package_node.package)
            copy_env.add_package(package_copy)
            old_package_created.add(package_node.package)
            copy_package_created.add(package_copy)

        for package in agent_packages:
            package_copy = copy(package)
            old_package_created.add(package)
            copy_package_created.add(package_copy)

    def copy_package_appear_dict(self, copy_env, old_packages_created, copy_package_created):
        package_appear_dict_copy = {}
        for package_appear_time, package_list in self.package_appear_dict.items():
            new_package_list = [copy(curr_package) for curr_package in package_list if curr_package not in old_packages_created]
            copy_package_created.update(new_package_list)
            package_appear_dict_copy[package_appear_time] = new_package_list
        copy_env.package_appear_dict = package_appear_dict_copy

    def copy_package_disappear_dict(self, copy_env, copy_package_created):
        package_disappear_dict_copy = {}
        for package_disappear_time, package_list in self.package_disappear_dict.items():
            package_disappear_dict_copy[package_disappear_time] = [package for package in copy_package_created if package.time_delivery + 1 == package_disappear_time]
        copy_env.package_disappear_dict = package_disappear_dict_copy

    def copy_agents(self, copy_env, copy_package_created):
        agent_node_coordinate = [node.get_x_y_coordinate() for node in self.agent_nodes]
        copy_env.agent_nodes = [copy_env.graph[x][y] for x, y in agent_node_coordinate]
        for agent_node in self.agent_nodes:
            x, y = agent_node.get_x_y_coordinate()
            copy_env.graph[x][y].agent = Agent.copy_with_packages(agent_node.agent, copy_package_created, copy_env)

    def get_delivery_nodes(self):
        set_pos_x_y = {node.package.get_delivery_x_y() for node in self.package_points}
        return {self.graph[x][y] for x, y in set_pos_x_y}

    def create_all_edges(self):
        for x in range(self.width + 1):
            for y in range(self.height + 1):
                self.create_edges_for_node(x, y)

    def create_edges_for_node(self, x, y):
        self.create_horizontal_edges(x, y)
        self.create_vertical_edges(x, y)

    def create_horizontal_edges(self, x, y):
        self.connect_nodes(x, y, x - 1, y)
        self.connect_nodes(x, y, x + 1, y)

    def create_vertical_edges(self, x, y):
        self.connect_nodes(x, y, x, y + 1)
        self.connect_nodes(x, y, x, y - 1)

    def connect_nodes(self, x1, y1, x2, y2):
        # Check if the edge already exists
        if x2 < 0 or x2 > self.width or y2 < 0 or y2 > self.height:
            return

        if (x1, y1, x2, y2) in self.edges_dict or (x2, y2, x1, y1) in self.edges_dict:
            return

        if (x1, y1, x2, y2) in self.blocked_edges or (x2, y2, x1, y1) in self.blocked_edges:
            return
        if self.fragile_edges is not None:
            edge = Edge(is_fragile=((x1, y1, x2, y2) in self.fragile_edges or (x2, y2, x1, y1) in self.fragile_edges))
        else:
            edge = Edge()
        edge.add_nodes(self.graph[x1][y1], self.graph[x2][y2])
        self.edges_dict[(x1, y1, x2, y2)] = edge
        self.graph[x1][y1].add_edge(edge)
        self.graph[x2][y2].add_edge(edge)

    def get_edge_from_nodes(self, node_1, node_2):
        x1, y1 = node_1.get_x_y_coordinate()
        x2, y2 = node_2.get_x_y_coordinate()
        return next(self.edges_dict[edge] for edge in self.edges_dict if (x1, y1, x2, y2) == edge or (x2, y2, x1, y1) == edge)

    def get_edge_from_coordinates(self, edge_coordinate_tuple):
        reverse_coordinate = (edge_coordinate_tuple[2], edge_coordinate_tuple[3], edge_coordinate_tuple[0], edge_coordinate_tuple[1])
        if edge_coordinate_tuple in self.edges_dict:
            return self.edges_dict[edge_coordinate_tuple]
        return self.edges_dict[reverse_coordinate]

    def create_clique(self):
        clique = Clique()

        # Create a copy of the nodes and edges from the original graph
        node_set = self.package_points | self.delivery_points
        node_set.update(self.agent_nodes)
        old_to_new_nodes_dict = {node: Node(node.x, node.y) for node in node_set}

        distance_dict = {}

        # Add nodes to the clique
        for node in old_to_new_nodes_dict.values():
            clique.add_node(node)

        # Add edges based on the shortest paths
        for node1, node2 in combinations(node_set, 2):
            if node1 in self.agent_nodes and node2 in self.agent_nodes:
                continue

            if node1 not in distance_dict:
                dijkstra_algo = Dijkstra(start_node=node1, env=self, destination_node=node2)
                _, distances = dijkstra_algo.run_search()
                distance_dict[node1] = distances

            distances = distance_dict[node1]
            clique.add_edge(node1, node2, distances[node2], old_to_new_nodes_dict)

        return clique

    def set_package_appear_dict(self, package_appear_dict):
        self.package_appear_dict = package_appear_dict

    def set_package_disappear_dict(self, package_disappear_dict):
        self.package_disappear_dict = package_disappear_dict

    def update_packages_state_if_needed(self, timer):
        if self.package_appear_dict is not None and timer in self.package_appear_dict:
            for curr_new_package in self.package_appear_dict[timer]:
                # self.graph[curr_new_package.pos_x][curr_new_package.pos_y].add_package(curr_new_package, env=self)
                self.add_package(curr_new_package)

        if self.package_disappear_dict is not None and timer in self.package_disappear_dict:
            for curr_package in self.package_disappear_dict[timer]:
                curr_package.remove_self_from_env(env=self)

    def update_agents_list(self, agent_list):
        self.agent_nodes = [agent.curr_node for agent in agent_list]

    def switch_agent_nodes(self, old_node, new_node):
        old_node.agent = None
        index_to_insert = self.agent_nodes.index(old_node)
        self.agent_nodes.remove(old_node)
        self.agent_nodes.insert(index_to_insert, new_node)

    def remove_package_from_env(self, package):
        package_node = self.graph[package.pos_x][package.pos_y]
        package_delivery_node = self.graph[package.dest_pos_x][package.dest_pos_y]
        if package_node in self.package_points:  # package already delivered
            package_node.package = None
            self.package_points.remove(package_node)
        if package_delivery_node in self.delivery_points:
            self.delivery_points.remove(package_delivery_node)

    def remove_package_after_pickup(self, package):
        package_node = self.graph[package.pos_x][package.pos_y]
        if package_node in self.package_points:
            package_node.package = None
            self.package_points.remove(package_node)

    def remove_package_after_drop(self, package):
        package_delivery_node = self.graph[package.dest_pos_x][package.dest_pos_y]
        if package_delivery_node in self.delivery_points:
            self.delivery_points.remove(package_delivery_node)

    def add_package(self, package):
        package_node = self.graph[package.pos_x][package.pos_y]
        package_delivery_node = self.graph[package.dest_pos_x][package.dest_pos_y]
        package_node.package = package
        self.delivery_points.add(package_delivery_node)
        self.package_points.add(package_node)

    def copy_agent_list(self, copy_env):
        agent_node_list = [curr_agent.curr_node.get_x_y_coordinate() for curr_agent in self.agents_list]
        copy_env_agents_list = [copy_env.graph[x][y].agent for x, y in agent_node_list]
        copy_env.agents_list = copy_env_agents_list

    def get_agent_from_index(self, agent_index):
        return self.agents_list[agent_index]

    def get_agent_node_from_index(self, agent_index):
        return self.agents_list[agent_index].curr_node
