import collections

from infra_libarrys.consts_and_enums.general_consts import GeneralPosConsts
from infra_libarrys.consts_and_enums.EdgeConsts import BlockedEdgeConsts, FragileEdgeConsts
from infra_libarrys.consts_and_enums.package_consts import PackageConsts
from infra_libarrys.consts_and_enums.agents_consts import AgentConsts
from infra_libarrys.infra_classes.Agent.GameFullCopAgent import GameFullCopAgent
from infra_libarrys.infra_classes.Agent.GameSemiCopAgent import GameSemiCopAgent
from infra_libarrys.infra_classes.Agent.GameZeroSumAgent import GameZeroSumAgent
from infra_libarrys.infra_classes.Agent.RealTimeAstar import RealTimeAstar
from infra_libarrys.infra_classes.Package import Package
from infra_libarrys.infra_classes.Agent.InterferingAgent import InterferingAgent
from infra_libarrys.infra_classes.Agent.HumanAgent import HumanAgent
from infra_libarrys.consts_and_enums.parser_consts import ParserFlags
from infra_libarrys.infra_classes.Env import Env


def get_flow_args(parser_dict):
    env = get_env(parser_dict)
    agents_list = get_agents_list(parser_dict, env)
    env.update_agents_list(agents_list)

    return env, agents_list


def get_package_dict(parser_dict):
    package_appear_dict = collections.defaultdict(list)
    package_disappear_dict = collections.defaultdict(list)
    for package in parser_dict[ParserFlags.P]:
        package_appear_dict[package.time_appearance].append(package)
        package_disappear_dict[package.time_delivery + 1].append(package)
    return package_appear_dict, package_disappear_dict


def get_agents_list(parser_dict, env):
    agents_list = []
    for agent_index, agent_tuple_args in enumerate(parser_dict[ParserFlags.AGENTS]):
        agent_flag, x, y = agent_tuple_args
        curr_node = env.graph[x][y]
        if agent_flag == AgentConsts.NORMAL_AGENT_FLAG:
            agents_list.append(RealTimeAstar(curr_node, env, get_goal_score(env)))
        elif agent_flag == AgentConsts.INTERFERING_AGENT_FLAG:
            agents_list.append(InterferingAgent(curr_node, env))
        elif agent_flag == AgentConsts.ZERO_SUM_AGENT_FLAG:
            agents_list.append(GameZeroSumAgent(curr_node=curr_node, env=env, agent_index=agent_index, time=0))
        elif agent_flag == AgentConsts.SEMI_COP_AGENT_FLAG:
            agents_list.append(GameSemiCopAgent(curr_node=curr_node, env=env, agent_index=agent_index, time=0))
        elif agent_flag == AgentConsts.FULL_COP_AGENT_FLAG:
            agents_list.append(GameFullCopAgent(curr_node=curr_node, env=env, agent_index=agent_index, time=0))
        else:
            agents_list.append(HumanAgent(curr_node, env))

    return agents_list


def get_env(parser_dict):
    package_appear_dict, package_disappear_dict = get_package_dict(parser_dict)
    x = parser_dict[ParserFlags.X][0]
    y = parser_dict[ParserFlags.Y][0]
    blocked_edges = set(parser_dict[ParserFlags.B])
    fragile_edges = set(parser_dict[ParserFlags.F])
    env = Env(x, y, blocked_edges=blocked_edges, fragile_edges=fragile_edges, package_appear_dict=package_appear_dict, package_disappear_dict=package_disappear_dict)
    return env


def parse_x_flag(line, parser_dict):
    splitted_line = line.split()
    parser_dict[ParserFlags.X].append(int(splitted_line[GeneralPosConsts.POS_FOR_X]))


def parse_y_flag(line, parser_dict):
    splitted_line = line.split()
    parser_dict[ParserFlags.Y].append(int(splitted_line[GeneralPosConsts.POS_FOR_Y]))


def parse_p_flag(line, parser_dict):
    splitted_line = line.split()
    args_package = (int(splitted_line[PackageConsts.POS_FOR_X]), int(splitted_line[PackageConsts.POS_FOR_Y]), int(splitted_line[PackageConsts.POS_DEST_X]), int(splitted_line[PackageConsts.POS_DEST_Y]),
                    int(splitted_line[PackageConsts.POS_APPEAR_TIME]), int(splitted_line[PackageConsts.POS_DELIVERY_TIME]))
    package = Package(*args_package)
    parser_dict[ParserFlags.P].append(package)


def parse_b_flag(line, parser_dict):
    splitted_line = line.split()
    from_pos = (int(splitted_line[BlockedEdgeConsts.POS_X_FROM]), int(splitted_line[BlockedEdgeConsts.POS_Y_FROM]))
    to_pos = (int(splitted_line[BlockedEdgeConsts.POS_X_TO]), int(splitted_line[BlockedEdgeConsts.POS_Y_TO]))
    parser_dict[ParserFlags.B].append((*from_pos, *to_pos))


def parse_f_flag(line, parser_dict):
    splitted_line = line.split()
    from_pos = (int(splitted_line[FragileEdgeConsts.POS_X_FROM]), int(splitted_line[FragileEdgeConsts.POS_Y_FROM]))
    to_pos = (int(splitted_line[FragileEdgeConsts.POS_X_TO]), int(splitted_line[FragileEdgeConsts.POS_Y_TO]))
    parser_dict[ParserFlags.F].append((*from_pos, *to_pos))


def parse_agent_flag(line, parser_dict):
    splitted_line = line.split()
    pos_x = int(splitted_line[AgentConsts.POS_X])
    pos_y = int(splitted_line[AgentConsts.POS_Y])
    agent_flag = splitted_line[AgentConsts.POS_FLAG]
    agent_tuple = (agent_flag, pos_x, pos_y)
    parser_dict[ParserFlags.AGENTS].append(agent_tuple)


def get_goal_score(env):
    return sum(len(lst) for lst in env.package_appear_dict.values())
