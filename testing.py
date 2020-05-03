from Linear_Ordering import linear_ordering
from Cluster_Growth import cluster_growth
from Block import Block
from Coordinate import Coordinate
import Simulated_Annealing
import random
from PIL import Image, ImageDraw

if __name__ == "__main__":
    beta = 0.5

    blocks = []
    for x in range(1, 7):
        block = Block(x, random.randint(1, 20), random.randint(1, 10))  # random width and height, unimportant
        blocks.append(block)

    print("Input:")


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
    order = linear_ordering(blocks)

    # Print order
    print("Order:", end=" ")
    for x in order:
        print(x.block_id, end=" ")
    print()

    # Run cluster growth
    print("\nRunning Cluster Growth Algorithm...")

    initial_floorplan = cluster_growth(order)

    # Displaying the Floorplan as a grid with colors
    print("Floorplan: ")
    fp_colors = ["white", "yellow", "green", "purple", "blue", "cyan", "red"]
    step_count = 50
    width = step_count * initial_floorplan.cur_width
    height = step_count * initial_floorplan.cur_height

    image = Image.new(mode='RGBA', size=(width+1, height+1), color="white")
    draw = ImageDraw.Draw(image)

    for y in range(initial_floorplan.cur_height):
        for x in range(initial_floorplan.cur_width):
            draw.rectangle(((x * step_count, y * step_count), ((x + 1) * step_count, (y + 1) * step_count)), fill=fp_colors[initial_floorplan.grid[y][x]], outline="black")

            print(initial_floorplan.grid[y][x], end=" ")
        print()
    print("Initial Area:", initial_floorplan.cur_width * initial_floorplan.cur_height)
    print("Initial Wire Length:", initial_floorplan.get_total_wire_length())
    print("Initial Cost: ", initial_floorplan.get_cost(beta))

    del draw
    image.show()

    print("Running simulated annealing...")
    final_floorplan = Simulated_Annealing.simulated_annealing(initial_floorplan, beta)


    print("Final Floorplan: ")
    width = step_count * final_floorplan.cur_width
    height = step_count * final_floorplan.cur_height

    image = Image.new(mode='RGBA', size=(width+1, height+1), color="white")
    draw = ImageDraw.Draw(image)

    for y in range(final_floorplan.cur_height):
        for x in range(final_floorplan.cur_width):
            draw.rectangle(((x * step_count, y * step_count), ((x + 1) * step_count, (y + 1) * step_count)), fill=fp_colors[final_floorplan.grid[y][x]], outline="black")

            print(final_floorplan.grid[y][x], end=" ")
        print()
    print("Final Area:", final_floorplan.cur_width * final_floorplan.cur_height)
    print("Final Wire Length:", final_floorplan.get_total_wire_length())
    print("Final Cost: ", final_floorplan.get_cost(beta))
    del draw
    image.show()

    pass
