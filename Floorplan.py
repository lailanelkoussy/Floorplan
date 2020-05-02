# Floorplan class
import copy
import Block
import math


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

    def can_place(self, block, x, y):
        for x in range(x, x + block.get_width()):
            for y in range(y, y + block.get_height()):
                if self.grid[y][x] != 0:
                    return False
        return True

    def place_block(self, block, x, y):
        block.set_placed(True)
        block.set_x(x)
        block.set_y(y)
        self.blocks.append(block)
        self.cur_width = max(block.x + block.width, self.cur_width)
        self.cur_height = max(block.y + block.height, self.cur_height)

        for x in range(block.x, block.x + block.width):
            for y in range(block.y, block.y + block.height):
                assert (self.grid[y][x] == 0), "Place not free to place block!"
                self.grid[y][x] = block.block_id

    def remove_block(self, block):
        x, y = block.get_bottom_left_coordinates()
        xb, yb = block.get_top_right_coordinate()
        for i in range(x, xb):
            for j in range(y, yb):
                assert (self.grid[y][x] == block.get_id()), "Place not taken up by this block!"
                self.grid[j][i] = 0

        self.blocks.remove(block)

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
