from Floorplan import Floorplan
from Coordinate import Coordinate


def get_corners(floorplan):
    grid = floorplan.get_grid()
    corners = set()

    w, h = floorplan.get_cur_dims()
    # Add outermost edges
    corners.add(Coordinate(w, 0))
    corners.add(Coordinate(0, h))

    # Find and add all other corners
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 0:
                if x == 0 and y == 0:
                    corners.add(Coordinate(x, y))
                elif x == 0 and y != 0:
                    if grid[y-1][x] > 0:
                        corners.add(Coordinate(x, y))
                elif x != 0 and y == 0:
                    if grid[y][x-1] > 0:
                        corners.add(Coordinate(x, y))
                elif x != 0 and y != 0:
                    if grid[y][x - 1] == 1 and grid[y - 1][x] > 0:
                        corners.add(Coordinate(x, y))
    return corners


def can_place(floorplan, corner, block_width, block_height):
    grid = floorplan.get_grid()
    for x in range(corner.x, corner.x + block_width):
        for y in range(corner.y, corner.y + block_height):
            if grid[y][x] != 0:
                return False
    return True


def try_placement(floorplan, corner, block_width, block_height):
    if can_place(floorplan, corner, block_width, block_height):
        floorplan_width, floorplan_height = floorplan.get_cur_dims()
        floorplan_width = max(corner.x + block_width, floorplan_width)
        floorplan_height = max(corner.y + block_height, floorplan_height)
    else:
        floorplan_width, floorplan_height = floorplan.get_max_dims()

    cost = floorplan_width * floorplan_height

    return cost


def add_to_floorplan(floorplan, block):
    corners = get_corners(floorplan)

    max_width, max_height = floorplan.get_max_dims()

    # Initialize minimum cost (Total Area) placement
    min_cost = max_width * max_height
    min_corner = Coordinate(-1, -1)
    min_flipped = False

    # Check minimum cost placement
    for flipped in [False, True]:
        for corner in corners:
            if not flipped:
                cur_cost = try_placement(
                    floorplan, corner, block.get_width(), block.get_height())
            else:
                cur_cost = try_placement(
                    floorplan, corner, block.get_height(), block.get_width())

            if cur_cost < min_cost:
                min_cost = cur_cost
                min_corner = corner
                min_flipped = flipped

    # Place Block
    block.set_placed(True)
    block.set_x(min_corner.x)
    block.set_y(min_corner.y)
    if min_flipped:
        block.swap_dims()

    floorplan.place_block(block)


def cluster_growth(order):
    floorplan = Floorplan(1000, 1000)

    for block in order:
        add_to_floorplan(floorplan, block)

    return floorplan
