import Linear_Ordering
import Cluster_Growth
import Simulated_Annealing
from Block import Block


def make_floorplan(JSON, beta, T0=500, T_min=20, alpha=0.85):
    print("Analyzing SoC...")
    blocks = get_blocks_and_connections(JSON)
    print("Obtaining initial solution...")
    init_sol = get_initial_floorplan(blocks)
    print("Initial solution obtained...")
    print("Running Simulated Annealing Algorithm...")
    print("Initial Area:", init_sol.get_area())
    print("Initial Wire Length:", init_sol.get_total_wire_length())
    print("Initial Cost: ", init_sol.get_cost(beta))
    init_sol.display().show()
    final_sol = Simulated_Annealing.simulated_annealing(init_sol, beta, T0, T_min, alpha)
    final_sol.display().show()
    print("Final Area:", final_sol.get_area())
    print("Final Wire Length:", final_sol.get_total_wire_length())
    print("Final Cost: ", final_sol.get_cost(beta))


    return final_sol


def get_blocks_and_connections(JSON):
    chip = JSON["soc"]
    buses = chip["buses"]
    blocks = get_blocks(chip)
    connect_blocks(blocks, chip)
    return blocks


def get_blocks(chip):
    components = chip["components"]
    blocks = []

    for component in components:
        block_id = component["component_id"]
        name = component["component_type"]
        width = component["width"]
        height = component["height"]
        block = Block(name, block_id, width, height)
        blocks.append(block)

    return blocks


def connect_blocks(blocks, chip):
    chip_buses = chip["buses"]
    chip_components = chip["components"]
    for bus in chip_buses:
        single_bus_connections = []
        for component in chip_components:
            connection_1 = component["connection_1"]
            if connection_1["bus_id"] == bus["bus_id"]:
                single_bus_connections.append(component["component_id"])
            if "connection_2" in component:
                connection_2 = component["connection_2"]
                if connection_2["bus_id"] == bus["bus_id"]:
                    single_bus_connections.append(component["component_id"])
        connect_blocks_on_bus(blocks, single_bus_connections)


def connect_blocks_on_bus(blocks, bus):
    for i in range(len(bus)):
        curr_block = get_block(blocks, bus[i])
        for j in range(len(bus)):
            if j != i:
                curr_block.add_connection(bus[j])


def get_block(blocks, block_id):
    for x in blocks:
        if x.get_id() == block_id:
            return x


def get_initial_floorplan(blocks):
    order = Linear_Ordering.linear_ordering(blocks)

    init_sol = Cluster_Growth.cluster_growth(order)
    return init_sol
