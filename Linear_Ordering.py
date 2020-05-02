from Block import Block


# using block with least number of connections
def get_initial_block(blocks):
    initial_block = blocks[0]
    for block in blocks:
        if len(block.connections) < len(initial_block.connections):
            initial_block = block

    return initial_block


# calculating the number of blocks connected to the block that are already placed
def get_num_of_terminating_nets(block, blocks):
    count = 0
    for x in blocks:
        if x.block_id in block.connections:
            if x.placed:
                count += 1
    return count


# calculating
def get_num_of_new_nets(block, blocks):
    count = 0
    for x in blocks:
        if x.block_id in block.connections:
            if not x.placed:
                count += 1
    return count


def get_num_of_cont_nets(block, blocks):
    return get_num_of_terminating_nets(block, blocks)


def get_gain(block, blocks):
    return get_num_of_terminating_nets(block, blocks) - get_num_of_new_nets(block, blocks)


def get_next_block(unplaced_blocks, blocks):
    gain = []
    max_gain = -999
    # line 5: blocks with maximum gain
    for i in range(len(unplaced_blocks)):
        gain.append(get_gain(unplaced_blocks[i], blocks))
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
            terminating_nets.append(get_num_of_terminating_nets(max_gain_blocks[i], blocks))
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
            continuing_nets.append(get_num_of_terminating_nets(max_gain_blocks[i], blocks))
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
            connected_nets.append(get_num_of_cont_nets(max_gain_blocks[i], blocks))
            if connected_nets[i] < min_connected_number:
                min_connected_number = connected_nets[i]

        for i in range(len(max_gain_blocks)):
            if connected_nets[i] == min_connected_number:
                min_continuing_blocks.append(max_gain_blocks[i])
        max_gain_blocks = max_continuing_blocks.copy()

    return max_gain_blocks[0]


def linear_ordering(blocks):
    unplaced_blocks = blocks.copy()
    initial_block = get_initial_block(blocks)
    initial_block.placed = True
    unplaced_blocks.remove(initial_block)
    order = [initial_block]

    while len(unplaced_blocks) > 0:
        new_block = get_next_block(unplaced_blocks, blocks)
        new_block.placed = True
        unplaced_blocks.remove(new_block)
        order.append(new_block)

    for x in order:
        x.placed = False

    return order


