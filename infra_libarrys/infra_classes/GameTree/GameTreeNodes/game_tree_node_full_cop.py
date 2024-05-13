from copy import copy, deepcopy

from infra_libarrys.infra_classes.GameTree.GameTreeNodes.game_tree_base_node import GameTreeNode
from infra_libarrys.infra_classes.State.GameTreeState import GameTreeState


class GameTreeNodeFullCop(GameTreeNode):
    def __init__(self, old_player_index, state, player_to_make_move_index, prev_actions=None, parent_node=None):
        super().__init__()
        self.curr_player_index = (old_player_index + 1) % 2
        self.parent_node = parent_node
        self.prev_actions = prev_actions
        self.curr_state = state
        self.player_to_make_move_index = player_to_make_move_index

    def __lt__(self, other):
        self_heuristic = heuristic(self)
        other_heuristic = heuristic(other)
        return self_heuristic < other_heuristic
        # if self.curr_state.get_fully_cop_score() == other.curr_state.get_fully_cop_score():
        #     return self.get_heuristic_tie_breaker() > other.get_heuristic_tie_breaker()
        # return self.curr_state.get_fully_cop_score() < other.curr_state.get_fully_cop_score()

    def __gt__(self, other):
        if self.curr_state.get_fully_cop_score() == other.curr_state.get_fully_cop_score():
            return self.get_heuristic_tie_breaker() < other.get_heuristic_tie_breaker()
        return self.curr_state.get_fully_cop_score() > other.curr_state.get_fully_cop_score()

    def get_children_list(self):
        for curr_edge in self.curr_state.curr_node.edges:
            if self._agent_on_other_node(curr_edge):  # todo: add this on the flow func
                continue
            new_prev_actions = self._get_new_prev_actions(curr_edge)
            parent_node = self
            new_state = self.create_state_from_edge(curr_edge)
            curr_tree_node = GameTreeNodeFullCop(old_player_index=self.curr_player_index, state=new_state, prev_actions=new_prev_actions, parent_node=parent_node, player_to_make_move_index=self.player_to_make_move_index)
            yield curr_tree_node

        new_state = self.create_state_with_no_op()
        parent_node = self
        new_prev_actions = self._get_new_prev_actions_with_no_op()
        curr_tree_node = GameTreeNodeFullCop(old_player_index=self.curr_player_index, state=new_state, prev_actions=new_prev_actions, parent_node=parent_node, player_to_make_move_index=self.player_to_make_move_index)
        yield curr_tree_node

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

    def get_start_node(self):
        curr_node = self
        while curr_node.parent_node is not None:
            curr_node = curr_node.parent_node
        return curr_node

    def get_mst_value(self):
        starting_node = self.get_start_node()
        next_action = self.prev_actions[self.player_to_make_move_index][0]
        if next_action is None:
            return starting_node.curr_state.get_mst_weight()
        next_action = self.get_next_action_from_edge_coordinate(next_action, starting_node)
        new_state = starting_node.create_state_from_edge(next_action)
        return new_state.get_mst_weight()

    @staticmethod
    def get_next_action_from_edge_coordinate(edge_coordinate, starting_node):
        x1, y1, x2, y2 = edge_coordinate
        edge_coordinate_1, edge_coordinate_2 = (x1, y1, x2, y2), (x2, y2, x1, y1)
        if edge_coordinate_1 in starting_node.curr_state.env.edges_dict:
            return starting_node.curr_state.env.edges_dict[edge_coordinate_1]
        return starting_node.curr_state.env.edges_dict[edge_coordinate_2]

    def get_heuristic_tie_breaker(self):
        return self.curr_state.time + self.get_mst_value()
