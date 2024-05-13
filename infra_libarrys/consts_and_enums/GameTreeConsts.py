from infra_libarrys.infra_classes.GameTree.GameTreeNodes.game_tree_node_zero_sum import GameTreeNodeZeroSum
from infra_libarrys.infra_classes.State.DummyState import MinValueState, MaxValueState


class GameConsts:
    INFINITY_VALUE_ZERO_SUM_NODE = GameTreeNodeZeroSum(old_player_index=0, parent_node=None, prev_actions=None, state=MaxValueState())
    MINUS_INFINITY_VALUE_ZERO_SUM_NODE = GameTreeNodeZeroSum(old_player_index=0, parent_node=None, prev_actions=None, state=MinValueState())
    MINUS_INFINITY_VALUE_SEMI_COP_NODE = GameTreeNodeZeroSum(old_player_index=0, parent_node=None, prev_actions=None, state=MinValueState())
    MAX_DEPTH_CUTOFF = 10
