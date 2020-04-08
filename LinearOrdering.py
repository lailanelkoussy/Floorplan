from Block import Block

# using block with least number of connections
def getInitialBlock(blocks):
    initial_block = blocks[0]
    for block in blocks:
        if len(block.connections) < len(initial_block.connections):
            initial_block = block

    return initial_block


# calculating the number of blocks connected to the block that are already placed
def getNumOfTerminatingNets(block, blocks):
    count = 0
    for x in blocks:
        if x.block_id in block.connections:
            if x.placed:
                count += 1
    return count


# calculating
def getNumOfNewNets(block, blocks):
    count = 0
    for x in blocks:
        if x.block_id in block.connections:
            if not x.placed:
                count += 1
    return count


def getNumOfContNets(block, blocks):
    return getNumOfTerminatingNets(block, blocks)


def getGain(block, blocks):
    return getNumOfTerminatingNets(block, blocks) - getNumOfNewNets(block, blocks)


def getNextBlock(unplaced_blocks, blocks):
    gain = []
    max_gain = -999
    # line 5: blocks with maximum gain
    for i in range(len(unplaced_blocks)):
        gain.append(getGain(unplaced_blocks[i], blocks))
        if gain[i] > max_gain:
            max_gain = gain[i]

    max_gain_blocks = []
    for i in range(len(unplaced_blocks)):
        if gain[i] == max_gain:
            max_gain_blocks.append(unplaced_blocks[i])

    # line 10: among those with max gain, those with most terminating ends
    terminating_nets = []  # has all the numbers of terminating nets
    max_terminating_number = -999
    max_terminating_blocks = []

    if len(max_gain_blocks) > 1:
        for i in range(len(max_gain_blocks)):
            terminating_nets.append(getNumOfTerminatingNets(max_gain_blocks[i], blocks))
            if terminating_nets[i] > max_terminating_number:
                max_terminating_number = terminating_nets[i]

        for i in range(len(max_gain_blocks)):
            if terminating_nets[i] == max_terminating_number:
                max_terminating_blocks.append(max_gain_blocks[i])
        max_gain_blocks = max_terminating_blocks.copy()

    # line 12: most continuing nets
    continuing_nets = []
    max_continuing_number = -999
    max_continuing_blocks = []
    if len(max_gain_blocks) > 1:
        for i in range(len(max_gain_blocks)):
            continuing_nets.append(getNumOfTerminatingNets(max_gain_blocks[i], blocks))
            if continuing_nets[i] > max_continuing_number:
                max_continuing_number = continuing_nets[i]

        for i in range(len(max_gain_blocks)):
            if continuing_nets[i] == max_continuing_number:
                max_continuing_blocks.append(max_gain_blocks[i])
        max_gain_blocks = max_continuing_blocks.copy()

    # line 14: fewest connected nets
    connected_nets = []
    min_connected_number = 999
    min_continuing_blocks = []
    if len(max_gain_blocks) > 1:
        for i in range(len(max_gain_blocks)):
            connected_nets.append(getNumOfContNets(max_gain_blocks[i], blocks))
            if connected_nets[i] < min_connected_number:
                min_connected_number = connected_nets[i]

        for i in range(len(max_gain_blocks)):
            if connected_nets[i] == min_connected_number:
                min_continuing_blocks.append(max_gain_blocks[i])
        max_gain_blocks = max_continuing_blocks.copy()

    return max_gain_blocks[0]


def linearOrdering(blocks):
    unplaced_blocks = blocks.copy()
    initial_block = getInitialBlock(blocks)
    initial_block.placed = True
    unplaced_blocks.remove(initial_block)
    order = [initial_block]

    while len(unplaced_blocks) > 0:
        new_block = getNextBlock(unplaced_blocks, blocks)
        new_block.placed = True
        unplaced_blocks.remove(new_block)
        order.append(new_block)
    return order


################### TESTING ################

blocks = []
for x in range(6):
    block = Block(x + 1, x, x) #random width and height, unimportant
    blocks.append(block)

blocks[0].addConnection(4)
blocks[3].addConnection(1)

blocks[1].addConnection(3)
blocks[2].addConnection(2)

blocks[1].addConnection(4)
blocks[3].addConnection(2)

blocks[1].addConnection(5)
blocks[4].addConnection(2)

blocks[1].addConnection(6)
blocks[5].addConnection(2)

blocks[2].addConnection(4)
blocks[3].addConnection(3)

blocks[4].addConnection(6)
blocks[5].addConnection(5)

order = linearOrdering(blocks)

print(order)
