import collections
from copy import copy

from infra_libarrys.consts_and_enums.GameTreeConsts import GameConsts
from infra_libarrys.consts_and_enums.agents_consts import AgentName, AgentConsts
from infra_libarrys.consts_and_enums.gui_consts import GuiColorConsts
from infra_libarrys.infra_classes.Agent.Agent import Agent
from infra_libarrys.infra_classes.GameTree.GameTreeNodes.game_tree_node_semi_cop import GameTreeNodeSemiCop
from infra_libarrys.infra_classes.GameTree.game_tree_functions import maximax_semi_cop, get_semi_cop_score_curr_level_index
from infra_libarrys.infra_classes.State.GameTreeState import GameTreeState


class GameSemiCopAgent(Agent):
    def __init__(self, curr_node, env, agent_index, time):
        super().__init__(curr_node, env, agent_index)
        self.agent_type = AgentName.ZERO_SUM
        self.tag = AgentConsts.ZERO_SUM_AGENT_FLAG
        self.agent_color = GuiColorConsts.RED if self.agent_index == 0 else GuiColorConsts.GREEN
        self.actions_stack = None
        self.time = time

    def run_agent_step(self, log):
        make_next_step = self.finish_crossing_with_curr_edge(log)
        if not make_next_step:
            return
        next_edge = self._get_player_next_action()
        if next_edge is None:
            log.info(f"Player number {self.agent_index + 1} is executing a no-op action and will not move")
            return

        self.step_over_edge(next_edge, log)
        self.time += 1

    def _get_player_next_action(self):
        first_agent = self
        copy_env = copy(self.env)
        start_state = GameTreeState(env=copy_env, curr_node=first_agent.curr_node, time=self.time, agent=first_agent, goal_score=None)
        start_game_tree_node = GameTreeNodeSemiCop(old_player_index=self.agent_index + 1, state=start_state, prev_actions=collections.defaultdict(list))
        leaf_node = maximax_semi_cop(start_game_tree_node, GameConsts.MAX_DEPTH_CUTOFF)
        prev_actions = leaf_node.prev_actions
        self.actions_stack = prev_actions[self.agent_index]
        if not self.actions_stack:
            return
        next_action = self._get_next_step_from_actions_stack()
        return next_action

    def _get_next_step_from_actions_stack(self):
        next_step = self.actions_stack.pop(0)
        if next_step is None:
            return next_step
        x1, y1, x2, y2 = next_step
        edge_coordinate_1, edge_coordinate_2 = (x1, y1, x2, y2), (x2, y2, x1, y1)
        if edge_coordinate_1 in self.env.edges_dict:
            return self.env.edges_dict[edge_coordinate_1]
        return self.env.edges_dict[edge_coordinate_2]
