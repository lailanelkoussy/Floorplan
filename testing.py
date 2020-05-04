from Linear_Ordering import linear_ordering
from Cluster_Growth import cluster_growth
from Block import Block
from Coordinate import Coordinate
import Simulated_Annealing
import random

if __name__ == "__main__":
    beta = 0.6

    blocks = []
    for x in range(1, 7):
        block = Block("name", x, random.randint(1, 10), random.randint(1, 10))  # random width and height, unimportant
        blocks.append(block)

    print("Input:")

    blocks[0].add_connection(4)
    blocks[3].add_connection(1)

    blocks[1].add_connection(3)
    blocks[2].add_connection(2)

    blocks[1].add_connection(4)
    blocks[3].add_connection(2)

    blocks[1].add_connection(5)
    blocks[4].add_connection(2)

    blocks[1].add_connection(6)
    blocks[5].add_connection(2)

    blocks[2].add_connection(4)
    blocks[3].add_connection(3)

    blocks[4].add_connection(6)
    blocks[5].add_connection(5)

    # Output blocks
    for b in blocks:
        print("Component ", b.block_id, ": ", "width = ", b.width, ", height = ", b.height, sep="")
        print("\tConnections: [", end="")
        for i in range(len(b.connections)):
            print(b.connections[i], end=",]"[i == len(b.connections) - 1])
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
    initial_floorplan.update_current_dims()

    # Displaying the Floorplan as a grid with colors
    print("Floorplan: ")
    initial_floorplan.display().show()
    print("Initial Area:", initial_floorplan.get_area())
    print("Initial Wire Length:", initial_floorplan.get_total_wire_length())
    print("Initial Cost: ", initial_floorplan.get_cost(beta))

    print("Running Simulated Annealing Algorithm...")
    final_floorplan = Simulated_Annealing.simulated_annealing(initial_floorplan, beta)

    print("Final Floorplan: ")
    final_floorplan.display().show()

    print("Final Area:", final_floorplan.get_area())
    print("Final Wire Length:", final_floorplan.get_total_wire_length())
    print("Final Cost: ", final_floorplan.get_cost(beta))
