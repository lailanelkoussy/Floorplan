# Floorplan class
import copy
import Block
import math
from PIL import Image, ImageDraw



def dist(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


class Floorplan:
    def __init__(self, max_width, max_height):
        self.cur_width = 0
        self.cur_height = 0
        self.max_width = max_width
        self.max_height = max_height
        self.grid = [[0 for x in range(max_width)] for y in range(max_height)]
        self.blocks = []

    def get_block(self, block_id):
        for block in self.blocks:
            if block.get_id() == block_id:
                return block
        return None

    def display(self):
        fp_colors = ["white", "yellow", "green", "purple", "blue", "cyan", "red"]
        step_count = 50
        width = step_count * self.cur_width
        height = step_count * self.cur_height

        image = Image.new(mode='RGBA', size=(width + 1, height + 1), color="white")
        draw = ImageDraw.Draw(image)

        for y in range(self.cur_height):
            for x in range(self.cur_width):
                draw.rectangle(((x * step_count, y * step_count), ((x + 1) * step_count, (y + 1) * step_count)),
                               fill=fp_colors[self.grid[y][x]], outline="black")

                print(self.grid[y][x], end=" ")
            print()

        del draw
        image.show()

    def can_place(self, block, x, y):
        for i in range(x, x + block.get_width() + 1):
            for j in range(y, y + block.get_height() + 1):
                if self.grid[j][i] != 0:
                    return False
        return True

    def update_current_dims(self):
        max_x = 0
        max_y = 0
        for block in self.blocks:
            block_xt, block_yt = block.get_top_right_coordinate()
            if block_xt > max_x:
                max_x = block_xt
            if block_yt > max_y:
                max_y = block_yt

        self.cur_height = max_y
        self.cur_width = max_x

    def place_block(self, block, x, y):
        block.set_placed(True)
        xt = x + block.get_width()
        yt = y + block.get_height()

        for i in range(x, xt + 1):
            for j in range(y, yt + 1):
                assert (self.grid[j][i] == 0), "Place not free to place block!"
                self.grid[j][i] = block.block_id

        self.update_current_dims()

    def remove_block(self, block):
        xt, yt = self.get_max_dims()
        for i in range(0, xt):
            for j in range(0, yt):
                if self.grid[j][i] == block.get_id():
                    self.grid[j][i] = 0

    def get_grid(self):
        return self.grid

    def get_block(self, block_id):
        for block in self.blocks:
            if block.get_id() == block_id:
                return block
        return 0.

    def get_cur_dims(self):
        return self.cur_width, self.cur_height

    def get_max_dims(self):
        return self.max_width, self.max_height

    def get_cost(self, beta):
        return beta * self.cur_height * self.cur_height + (1 - beta) * self.get_total_wire_length()

    def get_total_wire_length(self):
        wire_length = 0
        for block in self.blocks:
            connections = block.get_connections()
            for connection in connections:
                connection_block = self.get_block(connection)
                wire_length += self.block_distance(block, connection_block)
        return wire_length / 2

    def block_distance(self, block1, block2):
        x1, y1 = block1.get_bottom_left_coordinates()
        x1b, y1b = block1.get_top_right_coordinate()

        x2, y2 = block2.get_bottom_left_coordinates()
        x2b, y2b = block2.get_top_right_coordinate()

        left = x2b < x1
        right = x1b < x2
        bottom = y2b < y1
        top = y1b < y2
        if top and left:
            return dist((x1, y1b), (x2b, y2))
        elif left and bottom:
            return dist((x1, y1), (x2b, y2b))
        elif bottom and right:
            return dist((x1b, y1), (x2, y2b))
        elif right and top:
            return dist((x1b, y1b), (x2, y2))
        elif left:
            return x1 - x2b
        elif right:
            return x2 - x1b
        elif bottom:
            return y1 - y2b
        elif top:
            return y2 - y1b
        else:  # rectangles intersect
            return 0.
