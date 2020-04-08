class Block:

    def __init__(self, block_id, width, height, ):
        self.width = width
        self.height = height
        self.block_id = block_id
        self.connections = []  # assuming connections are pair relations
        self.placed = False

    def addConnection(self, connection_block_id):
        self.connections.append(connection_block_id)
