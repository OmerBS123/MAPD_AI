from copy import copy

from infra_libarrys.consts_and_enums.agents_consts import AgentName
from infra_libarrys.infra_classes.Mst import Mst
from infra_libarrys.infra_classes.State.State import State
from infra_libarrys.infra_decorators import counter_decorator


class AstarNodeWrapper:
    def __init__(self, state, parent_node, g, h, prev_action=None):
        self.state = state
        self.parent_node = parent_node
        self.g = g
        self.h = h
        self.prev_action = prev_action
        self.children = set()

    def __lt__(self, other):
        if self.calculate_f() == other.calculate_f():
            return self.state.agent.score > other.state.agent.score

        return self.calculate_f() < other.calculate_f()

    def calculate_f(self):
        return self.g + self.h

    @counter_decorator()
    def expand(self):
        new_node_list = []
        for curr_edge in self.state.curr_node.edges:
            previous_action = curr_edge.get_edge_coordinate()
            g = self.g + curr_edge.weight if self.state.agent.agent_type == AgentName.ASTAR else 0
            parent_node = self
            new_state = self.create_state_from_edge(curr_edge)
            h = self.get_h_for_state(new_state)
            new_node = AstarNodeWrapper(state=new_state, parent_node=parent_node, g=g, prev_action=previous_action, h=h)
            new_node_list.append(new_node)

        no_op_node = self.get_no_op_action()
        new_node_list.append(no_op_node)

        return new_node_list

    def create_state_from_edge(self, edge):
        copy_env = copy(self.state.env)
        x, y = self.state.curr_node.get_x_y_coordinate()
        new_curr_node = copy_env.graph[x][y]
        new_state = State(copy_env, curr_node=new_curr_node, time=self.state.time, agent=self.state.agent, goal_score=self.state.goal_score)
        new_state.update_state(old_edge=edge, time_delta=edge.weight)
        return new_state

    @staticmethod
    def get_h_for_state(state):
        clique = state.env.create_clique()
        mst = Mst(clique)
        mst.create_mst()
        return mst.get_mst_weight()

    def get_actions_path(self):
        return self.get_actions_path_helper(self, [])

    @staticmethod
    def get_actions_path_helper(node, path_acc):
        if node.parent_node is not None:
            path_acc.append(node.prev_action)
            node.get_actions_path_helper(node.parent_node, path_acc)
        return path_acc

    def get_no_op_action(self):
        previous_action = None
        g = self.g + 1
        parent_node = self
        copy_env = copy(self.state.env)
        x, y = self.state.curr_node.get_x_y_coordinate()
        new_curr_node = copy_env.graph[x][y]
        new_state = State(copy_env, curr_node=new_curr_node, time=self.state.time, agent=new_curr_node.agent, goal_score=self.state.goal_score)
        new_state.update_packages_state_if_needed(1)
        new_state.all_agents_pickup_and_drop_package()
        h = self.get_h_for_state(new_state)
        new_node = AstarNodeWrapper(state=new_state, parent_node=parent_node, g=g, prev_action=previous_action, h=h)
        return new_node
