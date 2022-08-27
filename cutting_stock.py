#!/usr/bin/env python3
#
# Cutting Stock
#
import numpy as np
from read_lengths import get_data
LABEL = 0
LENGTH = 1
#
# Helper funcionts
#
def length_list(label_length):
    return list(x[LENGTH] for x in label_length)

def label_list(label_lengt):
    return list(x[LABEL] for x in label_length)
#
# Input data
#
stocks = sorted(get_data('stock_rolls.csv'), key=lambda roll: roll[LENGTH], reverse=True)
orders = sorted(get_data('order_cuts.csv'), key=lambda cut: cut[LENGTH], reverse=True)

#
# Sorted version
#
stock_rolls = length_list(stocks)
order_cuts = length_list(orders)

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
print("\n\nTHE NAIVE CUTTING PROBLEM STRATEGY:")
#print(f"\tCutting {order_cuts} order from {stock_rolls} stock rolls")
print(f"\tOrder length: {order_total}, stock length: {stock_total}\n\n")
#
# Take the maximal cut
#
pivot_roll = 0
uncut_orders = orders
not_fitted_orders = []
cutted_orders = []

while pivot_roll < len(stock_rolls):
    largest_cut = np.max(length_list(uncut_orders))
    next_cut = length_list(uncut_orders).index(largest_cut)
    if (stock_rolls[pivot_roll] - sum(length_list(cutted_orders))) >= largest_cut:
        # add to cutted_orders
        cutted_orders.append(uncut_orders.pop(next_cut))
    else:
        # add to not_fitted_orders
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
print("\n\n===> RESULTS:")
wasted_length = []
for roll_index, roll_length in enumerate(stock_rolls):
    wasted_length.append(roll_length-sum(length_list(roll_cuts[roll_index])))
    print(f"\nRoll {roll_index}: {stocks[roll_index][LABEL]} of  {roll_length}:\n\tWasted:\t\t{wasted_length[roll_index]:5.1f}")
    for cut in roll_cuts[roll_index]:
        print(f"\t{cut[LABEL]:8s} of\t{cut[LENGTH]:5.1f}")
print(f"\nTotal WASTE: {sum(wasted_length)}")
if len(uncut_orders) > 0:
    print(f"Uncut orders: {uncut_orders}")
    print(f"Sorry there are still som cuts to be done: {uncut_orders}")
else:
    print(f"Job DONE!")
