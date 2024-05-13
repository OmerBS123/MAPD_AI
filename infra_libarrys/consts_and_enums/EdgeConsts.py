from enum import Enum

DEFAULT_WEIGHT = 1


class BlockedEdgeConsts:
    POS_Y_FROM = 2
    POS_X_FROM = 1
    POS_X_TO = 3
    POS_Y_TO = 4


class FragileEdgeConsts:
    POS_Y_FROM = 2
    POS_X_FROM = 1
    POS_X_TO = 3
    POS_Y_TO = 4


class EdgeState(Enum):
    REGULAR = 'regular'
    FRAGILE = 'fragile'
    BLOCKED = 'blocked'
