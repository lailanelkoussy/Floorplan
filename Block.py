class Block:
    def __init__(self, width, height, block_id):
        self.width = width
        self.height = height
        self.block_id = block_id
        self.connections = []
        placed = False
