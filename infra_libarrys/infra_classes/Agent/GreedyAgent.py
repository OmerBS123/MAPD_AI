from infra_libarrys.consts_and_enums.agents_consts import AgentName, AgentConsts
from infra_libarrys.consts_and_enums.gui_consts import GuiColorConsts
from infra_libarrys.infra_classes.Agent.AstarAgent import AstarAgent


class GreedyAgent(AstarAgent):
    def __init__(self, curr_node, env, goal_score):
        super().__init__(curr_node, env, goal_score)
        self.agent_type = AgentName.GREEDY_ASTAR
        self.tag = AgentConsts.GREEDY_ASTAR_AGENT_FLAG
        self.agent_color = GuiColorConsts.GREEN
