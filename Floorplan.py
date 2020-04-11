# Floorplan class
import copy


class Floorplan:
    def __init__(self, max_width, max_height):
        self.cur_width = 0
        self.cur_height = 0
        self.max_width = max_width
        self.max_height = max_height
        self.grid = [[0 for x in range(max_width)] for y in range(max_height)]
        self.blocks = []

    def place_block(self, block):
        self.blocks.append(copy.deepcopy(block))

        self.cur_width = max(block.x + block.width, self.cur_width)
        self.cur_height = max(block.y + block.height, self.cur_height)

        for x in range(block.x, block.x + block.width):
            for y in range(block.y, block.y + block.height):
                assert (self.grid[y][x] == 0), "Place not free to place block!"
                self.grid[y][x] = block.block_id

    def get_grid(self):
        return self.grid

    def get_cur_dims(self):
        return self.cur_width, self.cur_height

    def get_max_dims(self):
        return self.max_width, self.max_height
