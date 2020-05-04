import math

import numpy
from Block import Block
from Coordinate import Coordinate
from Floorplan import Floorplan
from random import seed
from random import randint
import copy


def stopping_criterion(switched_prev, switched, possibilities, init_sol, cur_sol, beta):
    if not (switched_prev or switched):
        return True

    if cur_sol.get_cost(beta) > 1.3 * init_sol.get_cost(beta):
        return True

    for row in possibilities:
        for entry in row:
            if entry is False:
                return False

    return True


# chooses two pairs to perturb
def get_pair(floorplan, i, possibilities):
    possible_range = len(floorplan.blocks)
    seed(i)
    choose = randint(0, possible_range - 1)
    index = 0

    while True:
        for x in range(0, possible_range - 1):
            for y in range(0, possible_range - 1):
                if possibilities[x][y] is False:
                    if choose == index:
                        block_a = floorplan.get_block(x + 1)
                        block_b = floorplan.get_block(y + 1)
                        assert (block_a is not None), "block_a does not exist"
                        assert (block_b is not None), "block_b does not exist!"
                        return block_a, block_b
                    else:
                        index += 1
        print("Could not choose pair! Resetting possibilities")
        possibilities = initialize_possibilities(possible_range)


def get_possible_switch_options(floorplan, block_a_original, block_b_original):
    test_floorplan = copy.deepcopy(floorplan)
    block_a = copy.deepcopy(block_a_original)
    block_b = copy.deepcopy(block_b_original)
    block_a_x, block_a_y = block_a.get_bottom_left_coordinates()
    block_b_x, block_b_y = block_b.get_bottom_left_coordinates()

    test_floorplan.remove_block(block_a)
    test_floorplan.remove_block(block_b)

    place_a = test_floorplan.can_place(block_a, block_b_x, block_b_y)

    block_a.swap_dims()
    place_a_swapped = test_floorplan.can_place(block_a, block_b_x, block_b_y)
    block_a.swap_dims()

    place_b = test_floorplan.can_place(block_b, block_a_x, block_a_y)

    block_b.swap_dims()
    place_b_swapped = test_floorplan.can_place(block_b, block_a_x, block_a_y)
    block_b.swap_dims()
    return place_a, place_a_swapped, place_b, place_b_swapped


# tries switching block_a and block_b
# if multiple options, will choose minimum cost one
# if unable, will return same floorplan
def try_switch(floorplan, block_a_original, block_b_original, beta):
    test_floorplan = copy.deepcopy(floorplan)
    block_a = test_floorplan.get_block(block_a_original.get_id())
    block_b = test_floorplan.get_block(block_b_original.get_id())
    place_a, place_a_swapped, place_b, place_b_swapped = get_possible_switch_options(test_floorplan, block_a, block_b)
    block_a_x, block_a_y = block_a_original.get_bottom_left_coordinates()
    block_b_x, block_b_y = block_b_original.get_bottom_left_coordinates()
    cost_a_b = 10000
    cost_a_swapped_b = 10000
    cost_a_b_swapped = 10000
    cost_both_swapped = 10000

    test_floorplan.remove_block(block_b)
    test_floorplan.remove_block(block_a)

    if place_a and place_b:
        test_floorplan.place_block(block_a, block_b_x, block_b_y)
        test_floorplan.place_block(block_b, block_a_x, block_a_y)
        cost_a_b = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block_b)
        test_floorplan.remove_block(block_a)

    if place_a and place_b_swapped:
        test_floorplan.place_block(block_a, block_b_x, block_b_y)
        block_b.swap_dims()
        test_floorplan.place_block(block_b, block_a_x, block_a_y)
        cost_a_b_swapped = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block_b)
        test_floorplan.remove_block(block_a)
        block_b.swap_dims()

    if place_a_swapped and place_b:
        block_a.swap_dims()
        test_floorplan.place_block(block_a, block_b_x, block_b_y)
        test_floorplan.place_block(block_b, block_a_x, block_a_y)
        cost_a_swapped_b = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block_b)
        test_floorplan.remove_block(block_a)
        block_a.swap_dims()

    if place_a_swapped and place_b_swapped:
        block_a.swap_dims()
        test_floorplan.place_block(block_a, block_b_x, block_b_y)
        block_b.swap_dims()
        test_floorplan.place_block(block_b, block_a_x, block_a_y)
        cost_both_swapped = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block_b)
        test_floorplan.remove_block(block_a)
        block_a.swap_dims()
        block_b.swap_dims()

    min_cost = min(cost_a_b, cost_a_swapped_b, cost_a_b_swapped, cost_both_swapped)

    if min_cost == 10000:
        return None
    elif min_cost == cost_a_swapped_b:
        block_a.swap_dims()
    elif min_cost == cost_a_b_swapped:
        block_b.swap_dims()
    elif min_cost == cost_both_swapped:
        block_a.swap_dims()
        block_b.swap_dims()

    test_floorplan.place_block(block_a, block_b_x, block_b_y)
    test_floorplan.place_block(block_b, block_a_x, block_a_y)
    block_a.set_x(block_b_x)
    block_a.set_y(block_b_y)
    block_b.set_x(block_a_x)
    block_b.set_y(block_a_y)
    test_floorplan.update_current_dims()
    return test_floorplan


def check_movement_options(floorplan, block):
    x, y = block.get_bottom_left_coordinates()
    xt, yt = block.get_top_right_coordinate()

    test_floorplan = copy.deepcopy(floorplan)
    test_floorplan.remove_block(block)

    # checking if can be pushed to the bottom by 1
    if y != 0:
        bottom = test_floorplan.can_place(block, x, y - 1)
    else:
        bottom = False

    # checking if can be pushed to the top by 1
    if yt != floorplan.max_height:
        top = test_floorplan.can_place(block, x, y + 1)
    else:
        top = False

    # checking if can be pushed to the left by 1
    if x != 0:
        left = test_floorplan.can_place(block, x - 1, y)
    else:
        left = False

    # checking if can be pushed to the right by 1
    if xt != floorplan.max_width:
        right = test_floorplan.can_place(block, x + 1, y)
    else:
        right = False

    return top, bottom, left, right


# function sees in which directions the block can move (top, bottom, left, right)
# tries all possible combinations of possible movements
# finds minimum cost solution and returns it
# if impossible to move, then returns original solution
def try_moving_in_neighborhood(floorplan, block, beta):
    top, bottom, left, right = check_movement_options(floorplan, block)
    test_floorplan = copy.deepcopy(floorplan)
    cost_top = 10000
    cost_bottom = 10000
    cost_right = 10000
    cost_left = 10000
    x, y = block.get_bottom_left_coordinates()

    test_floorplan.remove_block(block)

    if top:
        test_floorplan.place_block(block, x, y + 1)
        cost_top = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block)

    if bottom:
        test_floorplan.place_block(block, x, y - 1)
        cost_bottom = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block)

    if left:
        test_floorplan.place_block(block, x - 1, y)
        cost_left = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block)

    if right:
        test_floorplan.place_block(block, x + 1, y)
        cost_right = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block)

    min_cost = min(cost_top, cost_bottom, cost_right, cost_left)

    if min_cost == 10000:
        return None

    test_floorplan.remove_block(block)

    if min_cost == cost_top:
        test_floorplan.place_block(block, x, y + 1)
    elif min_cost == cost_bottom:
        test_floorplan.place_block(block, x, y - 1)
    elif min_cost == cost_right:
        test_floorplan.place_block(block, x + 1, y)
    elif min_cost == cost_left:
        test_floorplan.place_block(block, x - 1, y)

    test_floorplan.update_current_dims()
    return test_floorplan


# function tries three things
# floorplan_1: switching block_a and block_b
# floorplan_2: moving block_a around a little
# floorplan_3: moving block_b around
# then chooses best cost floorplan out of the three to return
def try_move(floorplan, block_a, block_b, beta):
    print("Trying to switch block", block_a.get_id(), "and block", block_b.get_id())
    floorplan_1 = try_switch(floorplan, block_a, block_b, beta)
    if floorplan_1 is None:
        print("Not possible...")
    else:
        print("Possible solution found!")
    print("Trying to move block", block_a.get_id(), "around...")
    floorplan_2 = try_moving_in_neighborhood(floorplan, block_a, beta)
    if floorplan_2 is None:
        print("Not possible...")
    else:
        print("Possible solution found!")
    print("Trying to move block", block_b.get_id(), "around...")
    floorplan_3 = try_moving_in_neighborhood(floorplan, block_b, beta)
    if floorplan_3 is None:
        print("Not possible...")
    else:
        print("Possible solution found!")

    return get_min_cost_floorplan(floorplan_1, floorplan_2, floorplan_3, beta)


def get_min_cost_floorplan(floorplan_1, floorplan_2, floorplan_3, beta):
    if floorplan_1 is None:
        cost_1 = 10000
    else:
        cost_1 = floorplan_1.get_cost(beta)

    if floorplan_2 is None:
        cost_2 = 10000
    else:
        cost_2 = floorplan_2.get_cost(beta)
    if floorplan_3 is None:
        cost_3 = 10000
    else:
        cost_3 = floorplan_3.get_cost(beta)

    if cost_1 == 10000 and cost_2 == 10000 and cost_3 == 10000:
        return None

    min_cost = min(cost_1, cost_2, cost_3)

    if min_cost == cost_1:
        return floorplan_1
    elif min_cost == cost_2:
        return floorplan_2
    else:
        return floorplan_3


def initialize_possibilities(number_of_blocks):
    possibilities = [[False for x in range(number_of_blocks)] for y in range(number_of_blocks)]

    for x in range(number_of_blocks):
        possibilities[x][x] = True

    return possibilities


# init_sol : initial solution
# beta: ratio between [0,1] indicating importance of area vs. wire length
# T0: initial temperature, better be high
# T_min: minimum temperature
# alpha: ratio between (0,1) indicating rate of cooling , optimal when higher
def simulated_annealing(init_sol, beta, T0=200, T_min=50, alpha=0.80):
    T = T0
    i = 0
    print("Initial temperature:", T0)
    print("T_min:", T_min)
    print("beta:", beta)
    curr_sol = copy.deepcopy(init_sol)
    curr_cost = init_sol.get_cost(beta)
    switched = True
    gif = [init_sol.display()]
    while T > T_min:
        possibilities = initialize_possibilities(len(init_sol.blocks))
        while True:
            switched_prev = switched
            switched = False
            i = i + 1
            print("Iteration number: ", i)
            a, b = get_pair(curr_sol, i, possibilities)
            possibilities[a.get_id() - 1][b.get_id() - 1] = True
            possibilities[b.get_id() - 1][a.get_id() - 1] = True
            print("Chosen pair: block", a.get_id(), ", block ", b.get_id())
            print("Finding possible actions...")
            trial_sol = try_move(curr_sol, a, b, beta)
            if trial_sol is not None:
                print("Trial solution obtained...")
                trial_cost = trial_sol.get_cost(beta)
                delta_cost = trial_cost - curr_cost
                if delta_cost < 0:
                    print("Trial solution better than current solution!")
                    curr_cost = trial_cost
                    curr_sol = copy.deepcopy(trial_sol)
                    gif.append(curr_sol.display())
                    switched = True
                    print("Switching solution...")
                else:
                    r = numpy.random.uniform()
                    print("Trial solution not better than current solution...")
                    if r < math.exp(-delta_cost / T):
                        curr_cost = trial_cost
                        curr_sol = copy.deepcopy(trial_sol)
                        gif.append(curr_sol.display())
                        switched = True
                        print("Switching solution anyways...")
            else:
                print("No possible moves for this pair...")
                switched = False

            print("Current Area:", curr_sol.get_area())
            print("Current Wire Length:", curr_sol.get_total_wire_length())
            print("Current Cost: ", curr_sol.get_cost(beta), "\n")

            if stopping_criterion(switched_prev, switched, possibilities, init_sol, curr_sol, beta):
                print("Stopping criterion met, cooling down...")
                break
        T = alpha * T  # decreasing the temperature
        print("Current temperature: ", T)
        gif[0].save('anitest.gif',
                    save_all=True,
                    append_images=gif[1:],
                    duration=200,
                    loop=0)

    return curr_sol
