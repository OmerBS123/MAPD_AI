from infra_libarrys.infra_classes.State.DummyState import DUMMY_STATES, MaxValueState, MinValueState


class GameTreeNode:
    def __init__(self):
        self.curr_player_index = None
        self.parent_node = None
        self.prev_actions = None
        self.curr_state = None

    def get_score(self):
        pass

    def at_end_game(self):
        return self.curr_state.at_end_game()

    def heuristic(self):
        if isinstance(self.curr_state, MaxValueState):
            return float("inf")

        elif isinstance(self.curr_state, MinValueState):
            return float("-inf")

        return self.curr_state.agent.score + 0.5 * len(self.curr_state.agent.packages) + 0.25 * len(self.curr_state.env.package_points)
