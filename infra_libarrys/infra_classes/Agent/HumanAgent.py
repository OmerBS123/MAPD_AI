import keyboard

from infra_libarrys.infra_classes.Agent.Agent import Agent
from infra_libarrys.consts_and_enums.agents_consts import AgentConsts
from infra_libarrys.consts_and_enums.gui_consts import GuiColorConsts
from infra_libarrys.consts_and_enums.keyboard_consts import KeyboardNameConsts
from infra_libarrys.consts_and_enums.agents_consts import AgentName


class HumanAgent(Agent):
    def __init__(self, curr_node, env):
        super().__init__(curr_node, env)
        self.agent_type = AgentName.HUMAN
        self.tag = AgentConsts.HUMAN_AGENT_FLAG
        self.agent_color = GuiColorConsts.ORANGE

    def run_agent_step(self):
        pass
        # try_again = True
        # while try_again:
        #     edge = self.get_edge_to_cross()
        #     if edge is not None:
        #         try_again = False
        #         self.step_over_edge(edge)

    def get_edge_to_cross(self):
        print("Press where you want to go")
        event = keyboard.read_event(suppress=True)
        edge = self.process_keyboard_press_event(event)
        return edge

    def process_keyboard_press_event(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == KeyboardNameConsts.UP:
                edge = self.make_up_if_possible()
            elif event.name == KeyboardNameConsts.DOWN:
                edge = self.make_down_if_possible()
            elif event.name == KeyboardNameConsts.LEFT:
                edge = self.make_left_if_possible()
            elif event.name == KeyboardNameConsts.RIGHT:
                edge = self.make_right_if_possible()
            else:
                edge = None
            return edge
        return None

    def make_right_if_possible(self):
        curr_pos_x, curr_pos_y = self.curr_node.get_x_y_coordinate()
        if curr_pos_x > self.env.width + 1:
            return None
        next_node_to_cross = self.env.graph[curr_pos_x + 1][curr_pos_y]
        edge_to_cross = self.env.get_edge_from_nodes(self.curr_node, next_node_to_cross)
        return edge_to_cross

    def make_left_if_possible(self):
        curr_pos_x, curr_pos_y = self.curr_node.get_x_y_coordinate()
        if curr_pos_x <= 0:
            return False
        next_node_to_cross = self.env.graph[curr_pos_x - 1][curr_pos_y]
        edge_to_cross = self.env.get_edge_from_nodes(self.curr_node, next_node_to_cross)
        return edge_to_cross

    def make_down_if_possible(self):
        curr_pos_x, curr_pos_y = self.curr_node.get_x_y_coordinate()
        if curr_pos_y <= 0:
            return False
        next_node_to_cross = self.env.graph[curr_pos_x][curr_pos_y - 1]
        edge_to_cross = self.env.get_edge_from_nodes(self.curr_node, next_node_to_cross)
        return edge_to_cross

    def make_up_if_possible(self):
        curr_pos_x, curr_pos_y = self.curr_node.get_x_y_coordinate()
        if curr_pos_y > self.env.height + 1:
            return False
        next_node_to_cross = self.env.graph[curr_pos_x][curr_pos_y + 1]
        edge_to_cross = self.env.get_edge_from_nodes(self.curr_node, next_node_to_cross)
        return edge_to_cross
