#!/usr/bin/env python3
#
# Stock Cutting
#
import numpy as np
from read_lengths import get_data
#order_cuts.txt  stock_rolls.txt
stock_rolls = get_data('stock_rolls.txt')
# [1000, 1000, 650]
order_cuts =  get_data('order_cuts.txt')
# [450, 656, 400, 234, 234, 444,95,12]
#
# Sorted version
#
stock_rolls.sort(reverse=True)
order_cuts.sort(reverse=True)
#
# Check Stock Length
#
stock_total = np.sum(stock_rolls)
order_total = np.sum(order_cuts)
assert stock_total >= order_total, f"Not enough stock roll ({stock_total}) for order ({order_total})"
#
# Roll Cuts
#
roll_cuts=[]
for roll in stock_rolls:
    roll_cuts.append([])
print("THE NAIVE CUTTING PROBLEM STRATEGY:")
print(f"Cutting {order_cuts} order from {stock_rolls} stock rolls")
print(f"Order length: {order_total}, stock length: {stock_total}")
#
# Take the maximal cut
#
pivot_roll = 0
uncut_orders = order_cuts.copy()
not_fitted_orders = []
cutted_orders = []

while pivot_roll < len(stock_rolls):
    largest_cut = np.max(uncut_orders)
    next_cut = uncut_orders.index(largest_cut)
    if (stock_rolls[pivot_roll] - sum(cutted_orders)) >= largest_cut:
        # add to cutted_orders
        print(f"Cutting {largest_cut} from {pivot_roll}")
        cutted_orders.append(uncut_orders.pop(next_cut))
    else:
        # add to not_fitted_orders
        print(f"Cut {largest_cut} does not fit on {pivot_roll}")
        not_fitted_orders.append(uncut_orders.pop(next_cut))

    if (len(uncut_orders) == 0):
        # No more cuttable orders exist.
        # Move to the next stock_roll
        print(f"Roll {pivot_roll} exhausted")
        roll_cuts[pivot_roll] = cutted_orders.copy()
        cutted_orders = []
        uncut_orders = not_fitted_orders.copy()
        not_fitted_orders = []
        pivot_roll += 1

#
# We have tried to cut all rolls so there should be no uncut_orders
#
print("==> RESULTS:")
wasted_length = []
for roll_index, roll_length in enumerate(stock_rolls):
    wasted_length.append(roll_length-sum(roll_cuts[roll_index]))
    print(f"Roll {roll_index} ({roll_length}): {roll_cuts[roll_index]}; W: {wasted_length[roll_index]}")
print(f"Total WASTE: {sum(wasted_length)}")
if len(uncut_orders) > 0:
    print(f"Uncut orders: {uncut_orders}")
    print(f"Sorry there are still som cuts to be done: {uncut_orders}")
else:
    print(f"Job DONE!")

#
# Refine the cut
#
if max(wasted_length) >= min(order_cuts):
    print(f"Cut could be refined: {max(wasted_length)} {min(order_cuts)}")
else:
    print("Cut is OPTIMAL")
