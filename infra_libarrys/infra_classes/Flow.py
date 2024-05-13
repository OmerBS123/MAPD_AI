import traceback
import time

from infra_libarrys.consts_and_enums.agents_consts import AgentName


class Flow:
    def __init__(self, env, agents_list, package_appear_dict, package_disappear_dict, gui_handler, log, run_with_time_delay):
        self.env = env
        self.agents_list = agents_list
        self.package_appear_dict = package_appear_dict
        self.package_disappear_dict = package_disappear_dict
        self.timer = 0
        self.gui_handler = gui_handler
        self.running = True
        self.final_time = max(self.package_disappear_dict.keys())
        self.last_package_appear_time = max(self.package_appear_dict.keys())
        self.log = log
        self.run_with_time_delay = run_with_time_delay

    def run_flow(self):
        if self.run_with_time_delay:
            time.sleep(1)
        self.log.info("Flow thread started")
        while self.running:
            self.timer += 1
            self.gui_handler.update_timer(self.timer)
            self.update_packages_state_if_needed()
            # get_steps_for_agents
            for curr_agent in self.agents_list:
                curr_agent.run_agent_step(self.timer)
            if self.run_with_time_delay:
                time.sleep(1)
            if self.should_finish():
                self.finish_run()

        # self.gui_handler.close_ui()

    def run_flow_game(self):
        try:
            self.log.info("Started the simulator")
            if self.run_with_time_delay:
                time.sleep(1)

            if any(curr_agent.agent_type == AgentName.FULL_COP for curr_agent in self.agents_list):
                for curr_agent in self.agents_list:
                    curr_agent.make_actions_stack()

            while self.running:
                self.gui_handler.update_timer(self.timer)
                self.update_packages_state_if_needed()
                for curr_agent in self.agents_list:
                    curr_agent.run_agent_step(log=self.log)
                if self.run_with_time_delay:
                    time.sleep(1)
                self._print_curr_state_of_game()
                self.timer += 1
                if self.should_finish_game_simulation():
                    self.running = False
        except Exception as e:
            self.log.error(f"Caught the exception {e} while running simulator exiting...")
            traceback.print_exc()

        finally:
            self.finish_run()

    def update_packages_state_if_needed(self):
        if self.timer in self.package_appear_dict:
            for curr_new_package in self.package_appear_dict[self.timer]:
                self.env.add_package(curr_new_package)
                # self.env.graph[curr_new_package.pos_x][curr_new_package.pos_y].add_package(curr_new_package, env=self.env)

        if self.timer in self.package_disappear_dict:
            for curr_package in self.package_disappear_dict[self.timer]:
                curr_package.remove_self_from_env(env=self.env)

    def finish_run(self):
        self._print_end_of_game_simulation()
        self.log.flush_logs()
        self.gui_handler.close_ui()

    def should_finish(self):
        cond1 = self.timer > self.final_time
        cond2 = self.timer > self.last_package_appear_time and not self.env.delivery_points
        return cond1 or cond2

    def should_finish_game_simulation(self):
        cond1 = max(self.env.package_appear_dict.keys()) < self.timer
        cond2 = sum({len(curr_agent.packages) for curr_agent in self.env.agents_list}) == 0
        cond3 = len(self.env.package_points) == 0
        return cond1 and cond2 and cond3

    def _print_end_of_game_simulation(self):
        self.log.info("The game is finished with the following result:")
        agent_1 = self.agents_list[0]
        agent_2 = self.agents_list[1]
        if agent_1.score == agent_2.score:
            self.log.info(f"The game ended with a Tie!!!")
            return
        winning_agent = max(self.agents_list)
        losing_agent = min(self.agents_list)
        self.log.info(f"The final score of the game is:\n{winning_agent} score:{winning_agent.score}\n{losing_agent} score:{losing_agent.score}")
        self.log.info(f"The winner is:{winning_agent} with a score of {winning_agent.score}")

    def _print_curr_state_of_game(self):
        self.log.info("Current state of game:")
        score_dict = {f'Agent number {agent.agent_index + 1} score': agent.score for agent in self.agents_list}
        agent_pos_dict = {f'Agent number {agent.agent_index + 1} pos': str(agent.curr_node) for agent in self.agents_list}
        packages_to_appear_dict = {key: str(value) for key, value in self.package_appear_dict.items() if key > self.timer}
        self.log.info(f"The current time is:{self.timer}")
        self.log.info(f"Score is:\n{score_dict}")
        self.log.info(f"The agents locations are:\n{agent_pos_dict}")
        if self.env.package_points:
            self.log.info(f"The nodes left with package on map:\n{[str(package_point) for package_point in self.env.package_points]}")
        if packages_to_appear_dict:
            self.log.info(f"The packages that are left to appear are:\n{packages_to_appear_dict}")
