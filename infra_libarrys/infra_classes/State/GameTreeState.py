from infra_libarrys.infra_classes.State.State import State

zero_sum_max_agent_index = 0


class GameTreeState(State):
    def __init__(self, env, curr_node, time, goal_score, agent=None):
        super().__init__(env, curr_node, time, goal_score, agent)

    def update_state_with_agent_index(self, old_edge, time_delta, old_agent_index):
        if old_agent_index == 0:
            self.update_packages_state_if_needed(time_delta)

        move_edge = self.get_edge_from_old_edge(old_edge) if old_edge else None

        if move_edge and move_edge.is_fragile:
            move_edge.remove_self_from_env(self.env)

        self.update_agent(old_edge)
        self.curr_agent_pickup_and_drop_package()

        self.update_agent_with_index(old_agent_index)

    def update_agent_with_index(self, agent_index):
        other_agent = self.env.get_agent_from_index((agent_index + 1) % 2)
        new_curr_node = self.env.get_agent_node_from_index((agent_index + 1) % 2)
        self.curr_node = new_curr_node
        self.agent = other_agent

    def curr_agent_pickup_and_drop_package(self):
        self.agent.pickup_package_if_exists()
        self.agent.drop_package_if_possible()

    def get_zero_sum_score(self):
        global zero_sum_max_agent_index
        max_agent_score = self.env.agents_list[zero_sum_max_agent_index].score
        min_agent_score = self.env.agents_list[(zero_sum_max_agent_index + 1) % 2].score
        return max_agent_score - min_agent_score

    def get_semi_cop_core(self):
        return self.agent.score

    def get_fully_cop_score(self):
        return sum([curr_agent.score for curr_agent in self.env.agents_list])

    @staticmethod
    def change_zero_sum_max_player_index(new_max_player_index):
        global zero_sum_max_agent_index
        zero_sum_max_agent_index = new_max_player_index
