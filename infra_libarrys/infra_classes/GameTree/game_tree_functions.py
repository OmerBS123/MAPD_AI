from infra_libarrys.consts_and_enums.GameTreeConsts import GameConsts

curr_level_agent_index = 0


def minimax(position, depth, alpha, beta, maximizing_player):
    if position.at_end_game() or depth == 0:
        return position

    if maximizing_player:
        max_eval_node = GameConsts.MINUS_INFINITY_VALUE_ZERO_SUM_NODE
        # children_list = list(position.get_children_list())
        # children_list.sort(key=heuristic)
        for child in position.get_children_list():
            # child = children_list.pop()
            curr_eval_node = minimax(child, depth - 1, alpha, beta, False)
            if curr_eval_node is None:
                continue
            max_eval_node = max(max_eval_node, curr_eval_node)
            alpha = max(alpha, curr_eval_node)
            if beta <= alpha:
                return None
        if max_eval_node.curr_state.env is None:
            return None
        return max_eval_node
    else:
        min_eval_node = GameConsts.INFINITY_VALUE_ZERO_SUM_NODE
        # children_list = list(position.get_children_list())
        # children_list.sort(key=heuristic)
        for child in position.get_children_list():
            # child = children_list.pop()
            curr_eval_node = minimax(child, depth - 1, alpha, beta, True)
            if curr_eval_node is None:
                continue
            min_eval_node = min(min_eval_node, curr_eval_node)
            beta = min(beta, curr_eval_node)
            if beta <= alpha:
                return None
        if min_eval_node.curr_state.env is None:
            return None
        return min_eval_node


def maximax_semi_cop(position, depth):
    if position.at_end_game() or depth == 0:
        return position

    max_eval_node = None
    for child in position.get_children_list():
        curr_eval_node = maximax_semi_cop(child, depth - 1)
        if curr_eval_node is None:
            continue
        global curr_level_agent_index
        curr_level_agent_index = position.curr_player_index
        max_eval_node = get_max_eval_node_for_semi_cop(max_eval_node, curr_eval_node)
    if max_eval_node is None:
        return None
    if max_eval_node.curr_state.env is None:
        return None
    return max_eval_node


def maximax_full_cop(position, depth):
    if position.at_end_game() or depth == 0:
        return position

    max_eval_node = GameConsts.MINUS_INFINITY_VALUE_ZERO_SUM_NODE
    for child in position.get_children_list():
        curr_eval_node = maximax_full_cop(child, depth - 1)
        if curr_eval_node is None:
            continue
        max_eval_node = max(max_eval_node, curr_eval_node)

    if max_eval_node.curr_state.env is None:
        return None
    return max_eval_node


def full_co_op__heuristic(node):
    state = node.curr_state
    heuristic_list = [curr_agent.score + 0.5 * len(curr_agent.packages) + 0.25 * len(state.env.package_points) for curr_agent in state.env.agents_list]
    return sum(heuristic_list)


def get_semi_cop_score_curr_level_index(semi_cop_node):
    global curr_level_agent_index
    return semi_cop_node.curr_state.env.agents_list[curr_level_agent_index].score


def get_semi_cop_score_curr_level_index_tie_breaker(semi_cop_node):
    global curr_level_agent_index
    return semi_cop_node.curr_state.env.agents_list[(curr_level_agent_index + 1) % 2].score


def get_max_eval_node_for_semi_cop(semi_cop_node_1, semi_cop_node_2):
    if semi_cop_node_1 is None:
        return semi_cop_node_2
    semi_cop_score_node_1 = get_semi_cop_score_curr_level_index(semi_cop_node_1)
    semi_cop_score_node_2 = get_semi_cop_score_curr_level_index(semi_cop_node_2)
    if semi_cop_score_node_1 < semi_cop_score_node_2:
        return semi_cop_node_2
    elif semi_cop_score_node_1 > semi_cop_score_node_2:
        return semi_cop_node_1
    else:
        semi_cop_score_node_1 = get_semi_cop_score_curr_level_index_tie_breaker(semi_cop_node_1)
        semi_cop_score_node_2 = get_semi_cop_score_curr_level_index_tie_breaker(semi_cop_node_2)
        if semi_cop_score_node_1 < semi_cop_score_node_2:
            return semi_cop_node_2
        elif semi_cop_score_node_1 < semi_cop_score_node_2:
            return semi_cop_node_1

    semi_cop_node_1_mst = get_mst_for_semi_cop_node(semi_cop_node_1)
    semi_cop_node_2_mst = get_mst_for_semi_cop_node(semi_cop_node_2)
    if semi_cop_node_1_mst < semi_cop_node_2_mst:
        return semi_cop_node_1
    else:
        return semi_cop_node_2


def get_mst_for_semi_cop_node(semi_cop_node):
    starting_node = semi_cop_node.get_start_node()
    next_action = semi_cop_node.prev_actions[curr_level_agent_index][0]
    if next_action is None:
        return starting_node.curr_state.get_mst_weight()
    next_action = get_next_action_from_edge_coordinate(next_action, starting_node)
    new_state = starting_node.create_state_from_edge(next_action)
    return new_state.get_mst_weight()


def get_next_action_from_edge_coordinate(edge_coordinate, semi_cop_node):
    x1, y1, x2, y2 = edge_coordinate
    edge_coordinate_1, edge_coordinate_2 = (x1, y1, x2, y2), (x2, y2, x1, y1)
    if edge_coordinate_1 in semi_cop_node.curr_state.env.edges_dict:
        return semi_cop_node.curr_state.env.edges_dict[edge_coordinate_1]
    return semi_cop_node.curr_state.env.edges_dict[edge_coordinate_2]
