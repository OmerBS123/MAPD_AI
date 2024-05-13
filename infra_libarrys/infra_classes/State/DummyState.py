from infra_libarrys.infra_classes.State.State import State


class MinValueState(State):
    def __init__(self, env=None, curr_node=None, time=None, goal_score=None):
        super().__init__(env, curr_node, time, goal_score)

    @staticmethod
    def get_zero_sum_score():
        return float("-inf")

    @staticmethod
    def get_semi_cop_core():
        return float("-inf")

    @staticmethod
    def get_fully_cop_score():
        return float("-inf")


class MaxValueState(State):
    def __init__(self, env=None, curr_node=None, time=None, goal_score=None):
        super().__init__(env, curr_node, time, goal_score)

    @staticmethod
    def get_zero_sum_score():
        return float("inf")


DUMMY_STATES = [MaxValueState, MinValueState]
