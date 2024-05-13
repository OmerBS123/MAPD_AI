from infra_libarrys.consts_and_enums.gui_consts import GuiColorConsts
from infra_libarrys.infra_classes.Agent.Agent import Agent
from infra_libarrys.consts_and_enums.agents_consts import AgentConsts
from infra_libarrys.consts_and_enums.agents_consts import AgentName
from infra_libarrys.infra_classes.Reduction.ReducedEnv import ReducedEnv
from infra_libarrys.infra_classes.SearchAlgorithem.Dijkstra import Dijkstra


class InterferingAgent(Agent):
    def __init__(self, curr_node, env):
        super().__init__(curr_node, env)
        self.env = env
        self.agent_type = AgentName.INTERFERING
        self.tag = AgentConsts.INTERFERING_AGENT_FLAG
        self.agent_color = GuiColorConsts.RED

    def run_agent_step(self):
        if not self.env.fragile_edges:
            return
        run_search = self.finish_crossing_with_curr_edge()
        if not run_search:
            return
        search_algo = self.get_search_algo()
        next_node = self.get_next_node_from_search_algo(search_algo)
        if next_node is None:
            return
        else:
            edge_to_pass = self.curr_node.get_edge_from_node(next_node)
            self.step_over_edge(edge_to_pass)

    def get_search_algo(self):
        reduced_env = ReducedEnv(self.env)
        dijkstra_algo = Dijkstra(start_node=reduced_env.original_to_reduced_mapping[self.curr_node], env=reduced_env)
        return dijkstra_algo

    def get_next_node_from_search_algo(self, search_algo):
        reduced_path, _ = search_algo.run_search()
        if reduced_path is None:
            return None
        path = self.convert_reduced_path(reduced_path)
        return path[1]

    @staticmethod
    def convert_reduced_path(reduced_path):
        new_path = [curr_node.original_object for curr_node in reduced_path[:-1]]
        last_node = reduced_path[-1].original_object.get_neighbor_node(new_path[-1])
        new_path.append(last_node)
        return new_path

    def pickup_package_if_exists(self):
        pass
