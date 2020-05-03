from Floorplan import Floorplan
from Coordinate import Coordinate


def get_corners(floorplan):
    grid = floorplan.get_grid()
    corners = set()

    w, h = floorplan.get_cur_dims()
    # Add outermost edges
    corners.add(Coordinate(w, 0))
    if h != 0:
        corners.add(Coordinate(0, h))

    # Find and add all other corners
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 0:
                if x == 0 and y != 0:
                    if grid[y - 1][x] > 0:
                        corners.add(Coordinate(x, y))
                elif x != 0 and y == 0:
                    if grid[y][x - 1] > 0:
                        corners.add(Coordinate(x, y))
                elif x != 0 and y != 0:
                    if grid[y][x - 1] > 0 and grid[y - 1][x] > 0:
                        corners.add(Coordinate(x, y))
    return corners


def try_placement(floorplan, corner, block):
    if floorplan.can_place(block, corner.x, corner.y):
        floorplan_width, floorplan_height = floorplan.get_cur_dims()
        floorplan_width = max(corner.x + block.get_width(), floorplan_width)
        floorplan_height = max(corner.y + block.get_height(), floorplan_height)
    else:
        floorplan_width, floorplan_height = floorplan.get_max_dims()

    return floorplan_width * floorplan_height


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
                    floorplan, corner, block)
            else:
                cur_cost = try_placement(
                    floorplan, corner, block)

            if cur_cost < min_cost:
                min_cost = cur_cost
                min_corner = corner
                min_flipped = flipped

    # Place Block
    if min_flipped:
        block.swap_dims()

    block.set_x(min_corner.x)
    block.set_y(min_corner.y)
    floorplan.blocks.append(block)
    floorplan.place_block(block, min_corner.x, min_corner.y)


def cluster_growth(order):
    floorplan = Floorplan(1000, 1000)

    for block in order:
        add_to_floorplan(floorplan, block)

    floorplan.update_current_dims()
    return floorplan
