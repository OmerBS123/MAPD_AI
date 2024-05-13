from infra_libarrys.consts_and_enums.agents_consts import AgentName, AgentConsts
from infra_libarrys.consts_and_enums.gui_consts import GuiColorConsts
from infra_libarrys.infra_classes.Agent.Agent import Agent
from infra_libarrys.infra_classes.SearchAlgorithem.Astar import Astar
from infra_libarrys.infra_classes.State.State import State
from infra_libarrys.infra_classes.Wrappers.AstarNodeWrapper import AstarNodeWrapper


class AstarAgent(Agent):
    def __init__(self, curr_node, env, goal_score):
        super().__init__(curr_node, env)
        self.agent_type = AgentName.ASTAR
        self.tag = AgentConsts.ASTAR_AGENT_FLAG
        self.agent_color = GuiColorConsts.SILVER
        self.goal_score = goal_score
        self.actions_stack = None

    def get_actions_stack(self, curr_time):
        search_algo = self.get_search_algo(curr_time)
        last_node = search_algo.run_search()
        if last_node is None:
            return []
        return last_node.get_actions_path()

    def get_next_step(self):
        if not self.actions_stack:
            return None
        edge_coordinates = self.actions_stack.pop()
        if edge_coordinates is None:
            return None
        return self.env.get_edge_from_coordinates(edge_coordinates)

    def get_search_algo(self, curr_time):
        start_state = State(env=self.env, curr_node=self.curr_node, time=curr_time, agent=self, goal_score=self.goal_score)
        h = AstarNodeWrapper.get_h_for_state(start_state)
        first_a_star_node = AstarNodeWrapper(state=start_state, parent_node=None, g=AgentConsts.G_INITIAL_VALUE, h=h)
        a_star_algo = Astar(start_node=first_a_star_node, original_env=self.env, running_agent=self)
        return a_star_algo

    def run_agent_step(self, curr_time=AgentConsts.AGENT_START_TIME):
        self.pickup_package_if_exists()
        self.drop_package_if_possible()
        if self.actions_stack is None:
            self.actions_stack = self.get_actions_stack(curr_time)
        make_next_step = self.finish_crossing_with_curr_edge()
        if not make_next_step:
            return
        next_edge = self.get_next_step()
        if next_edge is None:
            return
        self.step_over_edge(next_edge)
