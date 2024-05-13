from infra_libarrys.consts_and_enums.agents_consts import AgentName
from infra_libarrys.infra_classes.CustomException import CounterLimitExceededAstar, CounterLimitExceededRtaAstar

counter = 0
limit_dict = {AgentName.ASTAR: 10000,
              AgentName.REAL_TIME_ASTAR: 10}


def counter_decorator():
    def decorator(func):
        def wrapper(*args, **kwargs):
            global counter, limit_dict
            agent_type = args[0].state.agent.agent_type
            limit = limit_dict[agent_type]
            counter += 1
            if limit is not None and counter > limit:
                if agent_type == AgentName.ASTAR:
                    print(f"Counter exceed limit of {limit} executing no step")
                    raise CounterLimitExceededAstar("Exceed limit exception")
                else:
                    counter = 0
                    print(f"Counter exceed limit of {limit} executing best current step")
                    raise CounterLimitExceededRtaAstar("Exceed limit exception")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def reset_counter():
    global counter
    counter = 0
