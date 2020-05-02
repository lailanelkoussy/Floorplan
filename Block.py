class Block:

    def __init__(self, block_id, width, height, ):
        self.width = width
        self.height = height
        self.block_id = block_id
        self.connections = []  # assuming connections are pair relations
        self.x = -1
        self.y = -1
        self.placed = False

    def addConnection(self, connection_block_id):
        self.connections.append(connection_block_id)

    def swap_dims(self):
        self.width, self.height = self.height, self.width

    def get_id(self):
        return self.block_id

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_placed(self, placed):
        self.placed = placed

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_bottom_left_coordinates(self):
        return self.x, self.y

    def get_top_right_coordinate(self):
        return self.x + self.width, self.y + self.height

    def get_connections(self):
        return self.connections