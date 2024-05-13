import os
import threading

from infra_libarrys.infra_classes.Log import Log
from infra_libarrys.infra_functions.infra_functions import parse_args
from infra_libarrys.infra_functions.parser_functions import get_flow_args
from infra_libarrys.infra_classes.Flow import Flow
from infra_libarrys.infra_classes.Gui import GraphUI


def main():
    config_path = os.path.join(os.path.dirname(__file__), "support_files", "config.txt")
    parser_dict = parse_args(config_path)
    env, agents_list = get_flow_args(parser_dict) #todo: needs to add run with time delay to parser
    env.agents_list = agents_list
    log = Log()

    gui = GraphUI(env, agents_list)
    flow = Flow(env, agents_list, env.package_appear_dict, env.package_disappear_dict, gui_handler=gui, log=log, run_with_time_delay=True)
    gui.set_flow(flow)
    flow_thread = threading.Thread(target=flow.run_flow_game)
    flow_thread.start()
    gui.run_ui()


if __name__ == "__main__":
    main()
