from copy import deepcopy, copy

from infra_libarrys.infra_classes.GameTree.GameTreeNodes.game_tree_base_node import GameTreeNode
from infra_libarrys.infra_classes.State.GameTreeState import GameTreeState


class GameTreeNodeSemiCop(GameTreeNode):
    def __init__(self, old_player_index, state, prev_actions=None, parent_node=None):
        super().__init__()
        self.curr_player_index = (old_player_index + 1) % 2
        self.parent_node = parent_node
        self.prev_actions = prev_actions
        self.curr_state = state

    def __lt__(self, other):
        if self.curr_state.get_semi_cop_core() == other.curr_state.get_semi_cop_core():
            self_second_agent = self.curr_state.env.get_agent_from_index((self.curr_player_index + 1) % 2)
            other_second_agent = other.curr_state.env.get_agent_from_index((other.curr_player_index + 1) % 2)
            return self_second_agent.score < other_second_agent.score
        return self.curr_state.get_semi_cop_core() < other.curr_state.get_semi_cop_core()

    def __gt__(self, other):
        if self.curr_state.get_semi_cop_core() == other.curr_state.get_semi_cop_core():
            self_second_agent = self.curr_state.env.get_agent_from_index((self.curr_player_index + 1) % 2)
            other_second_agent = other.curr_state.env.get_agent_from_index((other.curr_player_index + 1) % 2)
            return self_second_agent.score > other_second_agent.score
        return self.curr_state.get_semi_cop_core() > other.curr_state.get_semi_cop_core()

    def __le__(self, other):
        return self.curr_state.get_semi_cop_core() <= other.curr_state.get_semi_cop_core()

    def __ge__(self, other):
        return self.curr_state.get_semi_cop_core() >= other.curr_state.get_semi_cop_core()

    def get_children_list(self):
        for curr_edge in self.curr_state.curr_node.edges:
            if self._agent_on_other_node(curr_edge):  # todo: add this on the flow func
                continue
            new_prev_actions = self._get_new_prev_actions(curr_edge)
            parent_node = self
            new_state = self.create_state_from_edge(curr_edge)
            curr_tree_node = GameTreeNodeSemiCop(old_player_index=self.curr_player_index, state=new_state, prev_actions=new_prev_actions, parent_node=parent_node)
            yield curr_tree_node

        # new_state = self.create_state_with_no_op()
        # parent_node = self
        # new_prev_actions = self._get_new_prev_actions_with_no_op()
        # curr_tree_node = GameTreeNodeSemiCop(old_player_index=self.curr_player_index, state=new_state, prev_actions=new_prev_actions, parent_node=parent_node)
        # yield curr_tree_node

    def create_state_with_no_op(self):
        copy_env = copy(self.curr_state.env)
        x, y = self.curr_state.curr_node.get_x_y_coordinate()
        new_curr_node = copy_env.graph[x][y]
        new_state = GameTreeState(copy_env, curr_node=new_curr_node, time=self.curr_state.time, agent=self.curr_state.agent, goal_score=self.curr_state.goal_score)
        new_state.update_state_with_agent_index(old_edge=None, time_delta=0, old_agent_index=self.curr_player_index)
        return new_state

    def _get_new_prev_actions_with_no_op(self):
        prev_action = None
        new_prev_actions = deepcopy(self.prev_actions)
        new_prev_actions[self.curr_player_index].append(prev_action)
        return new_prev_actions

    def _agent_on_other_node(self, curr_edge):
        return curr_edge.get_neighbor_node(self.curr_state.curr_node).agent is not None

    def _get_new_prev_actions(self, edge):
        prev_action = edge.get_edge_coordinate()
        new_prev_actions = deepcopy(self.prev_actions)
        new_prev_actions[self.curr_player_index].append(prev_action)
        return new_prev_actions

    def create_state_from_edge(self, edge):
        copy_env = copy(self.curr_state.env)
        x, y = self.curr_state.curr_node.get_x_y_coordinate()
        new_curr_node = copy_env.graph[x][y]
        new_state = GameTreeState(copy_env, curr_node=new_curr_node, time=self.curr_state.time, agent=self.curr_state.agent, goal_score=self.curr_state.goal_score)
        new_state.update_state_with_agent_index(old_edge=edge, time_delta=edge.weight, old_agent_index=self.curr_player_index)
        return new_state

    def get_maximazing_player_index(self):
        return self.curr_state.agent.agent_index

    def get_start_node(self):
        curr_node = self
        while curr_node.parent_node is not None:
            curr_node = curr_node.parent_node
        return curr_node
