import tkinter as tk
from tkinter import Text, RIGHT, END, Y
from PIL import Image, ImageTk

from infra_libarrys.consts_and_enums.gui_consts import GuiSizeConsts, GuiColorConsts, GuiFontConsts, GuiImagePathConsts


class GraphUI:
    def __init__(self, env, agents_list):
        self.env = env
        self.root = tk.Tk()
        self.root.title("Graph Simulation")

        self.canvas = tk.Canvas(self.root, width=GuiSizeConsts.DEFAULT_WIDTH, height=GuiSizeConsts.DEFAULT_HEIGHT, bg=GuiColorConsts.WHITE)
        self.canvas.pack()

        self.timer_label = tk.Label(self.root, text="Timer: 0")
        self.timer_label.pack(side=tk.TOP, anchor=tk.CENTER)

        self.scoreboard_text = Text(self.root, height=10, width=30, wrap="none")
        self.scoreboard_text.pack(side=RIGHT, fill=Y)
        self.scoreboard_text.insert(END, "Scoreboard:\n\n")

        self.offset_x = 0
        self.offset_y = 0

        self.agents_list = agents_list
        self.root.protocol("WM_DELETE_WINDOW", self.close_ui)
        self.flow = None
        self.should_close = False
        self.timer = 0

        self.package_image = self.get_image_obj()
        self.delivery_image = self.get_delivery_image()

    def set_flow(self, flow):
        self.flow = flow

    def update_ui(self, timer_label):
        self.update_offsets()
        self.draw_graph()
        self.draw_agents()
        self.update_timer_label(timer_label=timer_label)
        self.update_scoreboard()
        self.root.update_idletasks()

    def update_offsets(self):
        self.root.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.offset_x = (canvas_width - self.env.width * GuiSizeConsts.SCALE_SIZE) // 2
        self.offset_y = (canvas_height - self.env.height * GuiSizeConsts.SCALE_SIZE) // 2

    def run_ui(self):
        self.root.after(0, self.update_ui_after)
        self.root.after(GuiSizeConsts.SECOND_IN_MILLI, self.check_close_flag)
        self.root.mainloop()

    def close_ui(self):
        self.flow.running = False
        self.should_close = True

    def draw_graph(self):
        self.canvas.delete("all")
        drawn_edges = set()
        for x in range(self.env.width + 1):
            for y in range(self.env.height + 1):
                node = self.env.graph[x][y]
                if node.package is None:
                    self.canvas.create_oval(x * GuiSizeConsts.SCALE_SIZE + self.offset_x, y * GuiSizeConsts.SCALE_SIZE + self.offset_y, x * GuiSizeConsts.SCALE_SIZE + GuiSizeConsts.OVAL_SIZE + self.offset_x,
                                            y * GuiSizeConsts.SCALE_SIZE + GuiSizeConsts.OVAL_SIZE + self.offset_y, fill=GuiColorConsts.BLUE)
                else:
                    self.canvas.create_oval(x * GuiSizeConsts.SCALE_SIZE + self.offset_x, y * GuiSizeConsts.SCALE_SIZE + self.offset_y, x * GuiSizeConsts.SCALE_SIZE + GuiSizeConsts.OVAL_SIZE + self.offset_x,
                                            y * GuiSizeConsts.SCALE_SIZE + GuiSizeConsts.OVAL_SIZE + self.offset_y, fill=GuiColorConsts.PINK)
                    self.canvas.create_image(x * GuiSizeConsts.SCALE_SIZE + self.offset_x + 30,
                                             y * GuiSizeConsts.SCALE_SIZE + self.offset_y + 30,
                                             anchor='center',
                                             image=self.package_image)

                for edge in node.edges:
                    if edge in drawn_edges:
                        continue
                    drawn_edges.add(edge)
                    node1, node2 = edge.nodes
                    x1, y1 = node1.get_x_y_coordinate()
                    x2, y2 = node2.get_x_y_coordinate()
                    mid_x = (x1 + x2) * 0.5 * GuiSizeConsts.SCALE_SIZE + self.offset_x + GuiSizeConsts.LINE_SIZE
                    mid_y = (y1 + y2) * 0.5 * GuiSizeConsts.SCALE_SIZE + self.offset_y + GuiSizeConsts.LINE_SIZE
                    edge_fill = GuiColorConsts.RED if edge.is_fragile else GuiColorConsts.BLACK
                    line_width = 2 if edge.is_fragile else 1
                    self.canvas.create_line(x1 * GuiSizeConsts.SCALE_SIZE + GuiSizeConsts.LINE_SIZE + self.offset_x, y1 * GuiSizeConsts.SCALE_SIZE + GuiSizeConsts.LINE_SIZE + self.offset_y,
                                            x2 * GuiSizeConsts.SCALE_SIZE + GuiSizeConsts.LINE_SIZE + self.offset_x, y2 * GuiSizeConsts.SCALE_SIZE + GuiSizeConsts.LINE_SIZE + self.offset_y, fill=edge_fill, width=line_width)
                    self.canvas.create_text(mid_x, mid_y, text=f"{edge.weight}", fill=GuiColorConsts.GREY, font=GuiFontConsts.EDGE_WEIGHT_FONT)

    def draw_agents(self):
        for curr_agent in self.agents_list:
            agent_ui_pos_x = None
            agent_ui_pos_y = None
            if curr_agent.curr_crossing_edge is None:
                x, y = curr_agent.curr_node.get_x_y_coordinate()
                agent_ui_pos_x = x * GuiSizeConsts.SCALE_SIZE + 10 + self.offset_x
                agent_ui_pos_y = y * GuiSizeConsts.SCALE_SIZE - 5 + self.offset_y
                self.canvas.create_text(agent_ui_pos_x, agent_ui_pos_y, text=curr_agent.tag, fill=curr_agent.agent_color, font=GuiFontConsts.EDGE_WEIGHT_FONT)  # Display agent's tag above it
            else:
                node1, node2 = curr_agent.curr_crossing_edge.nodes
                x1, y1 = node1.get_x_y_coordinate()
                x2, y2 = node2.get_x_y_coordinate()
                mid_x = (x1 + x2) * 0.5 * GuiSizeConsts.SCALE_SIZE + self.offset_x + GuiSizeConsts.LINE_SIZE
                mid_y = (y1 + y2) * 0.5 * GuiSizeConsts.SCALE_SIZE + self.offset_y + GuiSizeConsts.LINE_SIZE
                agent_ui_pos_x = mid_x + GuiSizeConsts.AGENT_OFFSET_ON_EDGE
                agent_ui_pos_y = mid_y
                self.canvas.create_text(agent_ui_pos_x, agent_ui_pos_y, text=curr_agent.tag, fill=curr_agent.agent_color, font=GuiFontConsts.EDGE_WEIGHT_FONT)

            if curr_agent.packages:
                num_of_packages = len(curr_agent.packages)
                self.canvas.create_image(agent_ui_pos_x + 30,
                                         agent_ui_pos_y + 30,
                                         anchor='center',
                                         image=self.package_image)

                self.canvas.create_text(agent_ui_pos_x + 30,
                                        agent_ui_pos_y + 30,
                                        text=str(num_of_packages),
                                        anchor='center',
                                        fill=GuiColorConsts.BLACK,
                                        font=GuiFontConsts.PACKAGE_COUNT_FONT)

                for curr_package in curr_agent.packages:
                    delivery_pos_x, delivery_pos_y = curr_package.get_delivery_x_y()
                    x, y = delivery_pos_x * GuiSizeConsts.SCALE_SIZE + self.offset_x, delivery_pos_y * GuiSizeConsts.SCALE_SIZE + self.offset_y
                    self.canvas.create_image(x,
                                             y,
                                             anchor='center',
                                             image=self.delivery_image)

    def update_timer_label(self, timer_label):
        current_time = timer_label
        self.timer_label.config(text=f"Timer: {current_time}")

    def check_close_flag(self):
        if self.should_close:
            self.root.destroy()
        else:
            self.root.after(GuiSizeConsts.SECOND_IN_MILLI, self.check_close_flag)

    def update_ui_after(self):
        self.update_ui(self.timer)
        self.root.after(GuiSizeConsts.SECOND_IN_MILLI // 4, self.update_ui_after)

    def update_timer(self, new_time):
        self.timer = new_time

    def update_scoreboard(self):
        self.scoreboard_text.delete("1.0", END)  # Clear the current scoreboard content
        self.scoreboard_text.insert(END, "Scoreboard:\n\n")
        for agent in self.agents_list:
            self.scoreboard_text.insert(END, f"{agent.tag}: {agent.score}\n")
        self.scoreboard_text.update_idletasks()

    @staticmethod
    def get_image_obj():
        package_image_path = GuiImagePathConsts.PACKAGE

        # Open and resize the image using Pillow
        original_image = Image.open(package_image_path)
        resized_image = original_image.resize((GuiSizeConsts.PACKAGE_SIZE, GuiSizeConsts.PACKAGE_SIZE), Image.LANCZOS)

        # Convert the resized image to a Tkinter PhotoImage
        return ImageTk.PhotoImage(resized_image)

    @staticmethod
    def get_delivery_image():
        delivery_image_path = GuiImagePathConsts.DELIVERY

        # Open and resize the image using Pillow
        original_image = Image.open(delivery_image_path)
        resized_image = original_image.resize((GuiSizeConsts.PACKAGE_SIZE, GuiSizeConsts.PACKAGE_SIZE), Image.LANCZOS)

        # Convert the resized image to a Tkinter PhotoImage
        return ImageTk.PhotoImage(resized_image)
