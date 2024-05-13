import heapq
import logging

from infra_libarrys.infra_classes.CustomException import CounterLimitExceededAstar, CounterLimitExceededRtaAstar
from infra_libarrys.infra_classes.SearchAlgorithem.SearchAlgorithm import SearchAlgorithm

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Astar(SearchAlgorithm):
    def __init__(self, start_node, original_env, running_agent, destination_node=None):
        super().__init__(start_node=start_node, env=original_env, destination_node=destination_node)
        self.running_agent = running_agent
        self.open_nodes = [self.start_node]
        self.closed_nodes = set()

    def run_search(self):
        try:
            while True:
                if not self.open_nodes:
                    return None
                curr_node = heapq.heappop(self.open_nodes)
                if curr_node.state.is_goal():
                    return curr_node
                same_state_node = self.get_same_state_node(curr_node)
                if same_state_node is None or curr_node.calculate_f() < same_state_node.calculate_f():
                    if same_state_node is not None:
                        self.closed_nodes.remove(same_state_node)
                    self.closed_nodes.add(curr_node)
                    new_node_list = curr_node.expand()
                    for new_node in new_node_list:
                        heapq.heappush(self.open_nodes, new_node)
        except CounterLimitExceededAstar as _:
            return None
        except CounterLimitExceededRtaAstar as _:
            return curr_node

    def get_same_state_node(self, node):
        state_singleton = {curr_node for curr_node in self.closed_nodes if node.state == curr_node.state}
        if state_singleton:
            return state_singleton.pop()
        return None
