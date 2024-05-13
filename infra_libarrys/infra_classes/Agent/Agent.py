class Agent:
    def __init__(self, curr_node, env, agent_index):
        self.env = env
        self.curr_node = None
        self.put_self_on_node(curr_node)
        self.packages = set()
        self.time_left_to_cross_edge = 0
        self.curr_crossing_edge = None
        self.agent_type = None
        self.agent_color = None
        self.score = 0
        self.agent_index = agent_index

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __str__(self):
        return f"Agent number {self.agent_index + 1}"

    @classmethod
    def copy_with_packages(cls, original_agent, created_packages, new_env):
        x, y = original_agent.curr_node.get_x_y_coordinate()
        new_curr_node = new_env.graph[x][y]
        new_agent = cls(new_curr_node, new_env, original_agent.agent_index)
        old_agent_package_coordinate = {(package.pos_x, package.pos_y, package.time_appearance, package.time_delivery) for package in original_agent.packages}
        new_agent_packages = {package for package in created_packages if (package.pos_x, package.pos_y, package.time_appearance, package.time_delivery) in old_agent_package_coordinate}
        new_agent.packages = new_agent_packages
        for package in new_agent_packages:
            package.agent = new_agent
        new_agent.time_left_to_cross_edge = original_agent.time_left_to_cross_edge
        new_agent.curr_crossing_edge = None
        new_agent.agent_type = original_agent.agent_type
        new_agent.agent_color = original_agent.agent_color
        new_agent.score = original_agent.score
        return new_agent

    def drop_package(self, package, log=None):
        if log is not None:
            log.info(f"The package {package} has been delivered by agent number {self.agent_index + 1}")
        self.packages.remove(package)
        package.agent = None
        self.env.remove_package_after_drop(package)

    def step_over_edge(self, edge, log=None):
        self.curr_crossing_edge = edge
        self.time_left_to_cross_edge = edge.weight
        self.finish_crossing_with_curr_edge(log)

    def finish_crossing_with_curr_edge(self, log):
        if self.time_left_to_cross_edge <= 0:
            return True
        self.time_left_to_cross_edge -= 1
        if self.time_left_to_cross_edge > 0:
            log.info(f"Player number {self.agent_index + 1} is still crossing an edge no move will be executed")
            log.info(f"Player number {self.agent_index + 1} is on edge {self.curr_crossing_edge}")
            return False
        next_node = self.curr_crossing_edge.get_neighbor_node(self.curr_node)
        self.put_self_on_node(next_node)
        log.info(f"Player number {self.agent_index + 1} has moved to node {self.curr_node}")
        if self.curr_crossing_edge.is_fragile:
            self.curr_crossing_edge.remove_self_from_env(env=self.env)
            log.info(f"The fragile edge {self.curr_crossing_edge} has been blocked")
        self.curr_crossing_edge = None
        self.pickup_package_if_exists(log)
        self.drop_package_if_possible(log)
        return True

    def drop_package_if_possible(self, log=None):
        if not self.packages:
            return
        package_to_remove = self.curr_node.is_node_destination(self.packages)
        if package_to_remove is None:
            return
        self.drop_package(package_to_remove, log)
        self.score += 1
        if log is not None:
            log.info(f"Agent number {self.agent_index + 1} score is now:{self.score}")

    def put_self_on_node(self, new_curr_node):
        new_curr_node.agent = self
        if self.curr_node is not None:
            self.env.switch_agent_nodes(old_node=self.curr_node, new_node=new_curr_node)
        self.curr_node = new_curr_node

    def pickup_package_if_exists(self, log=None):
        if self.curr_node.package is None:
            return

        self.packages.add(self.curr_node.package)
        if log is not None:
            log.info(f"The package: {self.curr_node.package} has been picked up by agent number: {self.agent_index + 1} and will be removed from node {self.curr_node}")
        self.curr_node.package.agent = self
        self.env.remove_package_after_pickup(self.curr_node.package)

    def run_agent_step(self, log):
        pass
