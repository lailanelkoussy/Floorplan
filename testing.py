from LinearOrdering import linearOrdering
from Cluster_Growth import cluster_growth
from Block import Block
from Coordinate import Coordinate
import random
from PIL import Image, ImageDraw

if __name__ == "__main__":
    blocks = []
    for x in range(1, 7):
        block = Block(x, random.randint(1, 20), random.randint(1, 10))  # random width and height, unimportant
        blocks.append(block)

    print("Input:")

    # block = Block(1, 6, 8)
    # blocks.append(block)
    # block = Block(2, 6, 1)
    # blocks.append(block)
    # block = Block(3, 6, 1)
    # blocks.append(block)
    # block = Block(4, 4, 6)
    # blocks.append(block)
    # block = Block(5, 6, 1)
    # blocks.append(block)
    # block = Block(6, 6, 1)
    # blocks.append(block)

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

    # Output blocks
    for b in blocks:
        print("Component ", b.block_id, ": ", "width = ", b.width, ", height = ", b.height, sep="")
        print("\tConnections: [", end="")
        for i in range(len(b.connections)):
            print(b.connections[i], end=",]"[i == len(b.connections)-1])
        print()
        print()

    # Run linear Ordering
    print("\nRunning Linear Ordering Algorithm...")
    input()
    order = linearOrdering(blocks)

    # Print order
    print("Order:", end=" ")
    for x in order:
        print(x.block_id, end=" ")
    print()

    # Run cluster growth
    print("\nRunning Cluster Growth Algorithm...")
    input()

    floorplan = cluster_growth(order)

    # Displaying the Floorplan as a grid with colors
    print("Floorplan: ")
    fp_colors = ["white", "yellow", "green", "purple", "blue", "cyan", "red"]
    step_count = 50
    width = step_count * floorplan.cur_width
    height = step_count * floorplan.cur_height

    image = Image.new(mode='RGBA', size=(width+1, height+1), color="white")
    draw = ImageDraw.Draw(image)

    for y in range(floorplan.cur_height):
        for x in range(floorplan.cur_width):
            draw.rectangle(((x * step_count, y * step_count), ((x + 1) * step_count, (y + 1) * step_count)), fill=fp_colors[floorplan.grid[y][x]], outline="black")

            print(floorplan.grid[y][x], end=" ")
        print()
    print("Final Area:", floorplan.cur_width * floorplan.cur_height)
    del draw
    image.show()

    pass
