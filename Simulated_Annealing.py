import math

import numpy
from Block import Block
from Coordinate import Coordinate
from Floorplan import Floorplan
from random import seed
from random import randint
import copy


def stopping_criterion(switched_prev, switched):
    if not switched_prev and not switched:
        return False
    return True


# chooses two pairs to perturb
def get_pair(floorplan, i):
    possible_range = len(floorplan.blocks)
    seed(i)
    while True:
        a_index = randint(0, possible_range - 1)
        b_index = randint(0, possible_range - 1)
        if a_index != b_index:
            break
    return floorplan.blocks[a_index], floorplan.blocks[b_index]


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

    place_b = test_floorplan.can_place(block_b, block_a_x, block_a_y)
    block_b.swap_dims()
    place_b_swapped = test_floorplan.can_place(block_b, block_a_x, block_a_y)

    return place_a, place_a_swapped, place_b, place_b_swapped


# tries switching block_a and block_b
# if multiple options, will choose minimum cost one
# if unable, will return same floorplan
def try_switch(floorplan, block_a, block_b, beta):
    test_floorplan = copy.deepcopy(floorplan)
    block_a_x, block_a_y = block_a.get_bottom_left_coordinates()
    block_b_x, block_b_y = block_b.get_bottom_left_coordinates()
    cost_a_b = 10000
    cost_a_swapped_b = 10000
    cost_a_b_swapped = 10000
    cost_both_swapped = 10000
    place_a, place_a_swapped, place_b, place_b_swapped = get_possible_switch_options(floorplan, block_a, block_b)

    test_floorplan.remove_block(block_a)
    test_floorplan.remove_block(block_b)

    if test_floorplan.can_place(block_a, block_b_x, block_b_y):
        test_floorplan.place_block(block_a, block_b_x, block_b_y)
        if test_floorplan.can_place(block_b, block_a_x, block_a_y):
            test_floorplan.place_block(block_b, block_a_x, block_a_y)
            cost_a_b = test_floorplan.get_cost(beta)
            test_floorplan.remove_block(block_b)
        block_b.swap_dims()
        if test_floorplan.can_place(block_b, block_a_x, block_a_y):
            test_floorplan.place_block(block_b, block_a_x, block_a_y)
            cost_a_b_swapped = test_floorplan.get_cost(beta)
            test_floorplan.remove_block(block_b)
        block_b.swap_dims()

        test_floorplan.remove_block(block_a)

    block_a.swap_dims()
    if test_floorplan.can_place(block_a, block_b_x, block_b_y):
        test_floorplan.place_block(block_a, block_b_x, block_b_y)
        if test_floorplan.can_place(block_b, block_a_x, block_a_y):
            test_floorplan.place_block(block_b, block_a_x, block_a_y)
            cost_a_swapped_b = test_floorplan.get_cost(beta)
            test_floorplan.remove_block(block_b)
        block_b.swap_dims()
        if test_floorplan.can_place(block_b, block_a_x, block_a_y):
            test_floorplan.place_block(block_b, block_a_x, block_a_y)
            cost_both_swapped = test_floorplan.get_cost(beta)
            test_floorplan.remove_block(block_b)
        block_b.swap_dims()
        test_floorplan.remove_block(block_a)
    block_a.swap_dims()

    min_cost = min(cost_a_b, cost_a_swapped_b, cost_a_b_swapped, cost_both_swapped)

    if min_cost == 10000:
        return floorplan
    if min_cost == cost_a_swapped_b:
        block_a.swap_dims()
    if min_cost == cost_a_b_swapped:
        block_b.swap_dims()
    if min_cost == cost_both_swapped:
        block_a.swap_dims()
        block_b.swap_dims()

    test_floorplan.remove_block(block_a)
    test_floorplan.remove_block(block_b)

    test_floorplan.place_block(block_a, block_b_x, block_b_y)
    block_a.set_x(block_b_x)
    block_a.set_y(block_b_y)
    test_floorplan.place_block(block_b, block_a_x, block_a_y)
    block_b.set_x(block_a_x)
    block_b.set_y(block_a_y)
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
    cost_top_right = 10000
    cost_top_left = 10000
    cost_bottom = 10000
    cost_bottom_right = 10000
    cost_bottom_left = 10000
    cost_right = 10000
    cost_left = 10000
    x, y = block.get_bottom_left_coordinates()

    test_floorplan.remove_block(block)
    if top:
        test_floorplan.place_block(block, x, y + 1)
        cost_top = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block)
        if right:
            if test_floorplan.can_place(block, x + 1, y + 1):
                test_floorplan.place_block(block, x + 1, y + 1)
                cost_top_right = test_floorplan.get_cost(beta)
                test_floorplan.remove_block(block)
        if left:
            if test_floorplan.can_place(block, x - 1, y + 1):
                test_floorplan.place_block(block, x - 1, y + 1)
                cost_top_left = test_floorplan.get_cost(beta)
                test_floorplan.remove_block(block)

    if bottom:
        test_floorplan.place_block(block, x, y - 1)
        cost_bottom = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block)
        if right:
            if test_floorplan.can_place(block, x + 1, y - 1):
                test_floorplan.place_block(block, x + 1, y - 1)
                cost_bottom_right = test_floorplan.get_cost(beta)
                test_floorplan.remove_block(block)
        if left:
            if test_floorplan.can_place(block, x - 1, y - 1):
                test_floorplan.place_block(block, x - 1, y - 1)
                cost_bottom_left = test_floorplan.get_cost(beta)
                test_floorplan.remove_block(block)

    if right:
        test_floorplan.place_block(block, x + 1, y)
        cost_right = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block)
    if left:
        test_floorplan.place_block(block, x - 1, y)
        cost_left = test_floorplan.get_cost(beta)
        test_floorplan.remove_block(block)

    min_cost = min(cost_top, cost_top_right, cost_top_left, cost_bottom, cost_bottom_right, cost_bottom_left,
                   cost_right, cost_left)

    if min_cost == 10000:
        return floorplan

    test_floorplan.remove_block(block)

    if min_cost == cost_top:
        test_floorplan.place_block(block, x, y + 1)
    if min_cost == cost_top_right:
        test_floorplan.place_block(block, x + 1, y + 1)
    if min_cost == cost_top_left:
        test_floorplan.place_block(block, x - 1, y + 1)
    if min_cost == cost_bottom:
        test_floorplan.place_block(block, x, y - 1)
    if min_cost == cost_bottom_right:
        test_floorplan.place_block(block, x + 1, y - 1)
    if min_cost == cost_bottom_left:
        test_floorplan.place_block(block, x - 1, y - 1)
    if min_cost == cost_right:
        test_floorplan.place_block(block, x + 1, y)
    if min_cost == cost_left:
        test_floorplan.place_block(block, x - 1, y)
    return test_floorplan


# function tries three things
# floorplan_1: switching block_a and block_b
# floorplan_2: moving block_a around a little
# floorplan_3: moving block_b around
# then chooses best cost floorplan out of the three to return
def try_move(floorplan, block_a, block_b, beta):
    floorplan_1 = try_switch(floorplan, block_a, block_b, beta)
    floorplan_2 = try_moving_in_neighborhood(floorplan, block_a, beta)
    floorplan_3 = try_moving_in_neighborhood(floorplan, block_b, beta)

    return get_min_cost_floorplan(floorplan_1, floorplan_2, floorplan_3, beta)


def get_min_cost_floorplan(floorplan_1, floorplan_2, floorplan_3, beta):
    cost_1 = floorplan_1.get_cost(beta)
    cost_2 = floorplan_2.get_cost(beta)
    cost_3 = floorplan_3.get_cost(beta)

    if cost_1 < cost_2:
        if cost_1 < cost_3:
            return floorplan_1
    else:
        if cost_2 < cost_3:
            return floorplan_2
        else:
            return floorplan_3


# init_sol : initial solution
# beta: ratio between [0,1] indicating importance of area vs. wire length
# T0: initial temperature, better be high
# T_min: minimum temperature
# alpha: ratio between (0,1) indicating rate of cooling , optimal when lower
def simulated_annealing(init_sol, beta, T0=100, T_min=50, alpha=0.2):
    T = T0
    i = 0
    curr_sol = copy.deepcopy(init_sol)
    curr_cost = init_sol.get_cost(beta)
    while T > T_min:
        switched = True
        while True:
            switched_prev = switched
            switched = False
            i = i + 1
            a, b = get_pair(curr_sol, i)
            trial_sol = try_move(curr_sol, a, b, beta)
            trial_cost = trial_sol.get_cost(beta)
            delta_cost = trial_cost - curr_cost
            if delta_cost < 0:
                curr_cost = trial_cost
                curr_sol = copy.deepcopy(trial_sol)
                switched = True
            else:
                r = numpy.random.uniform()
                if r < math.exp(-delta_cost / T):
                    curr_cost = trial_cost
                    curr_sol = copy.deepcopy(trial_sol)
                    switched = True

            if stopping_criterion(switched_prev, switched):
                break

    T = alpha * T  # decreasing the temperature

    return curr_sol
