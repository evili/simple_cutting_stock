#!/usr/bin/env python3
#
# Stock Cutting
#
import numpy as np
from read_lengths import get_data
LABEL = 0
LENGTH = 1

def length_list(label_length):
    return list(x[LENGTH] for x in label_length)

def label_list(label_lengt):
    return list(x[LABEL] for x in label_length)

# order_cuts.txt  stock_rolls.txt
stocks = sorted(get_data('stock_rolls.txt'), key=lambda roll: roll[LENGTH], reverse=True)
# stock_labels, stock_rolls = get_data('stock_rolls.txt')
# [1000, 1000, 650]
orders = sorted(get_data('order_cuts.txt'), key=lambda cut: cut[LENGTH], reverse=True)
# order_labels, order_cuts =  get_data('order_cuts.txt')
# [450, 656, 400, 234, 234, 444,95,12]
#
# Sorted version
#

stock_rolls = length_list(stocks)
order_cuts = length_list(orders)

# print(f"Stock Rolls: {stock_rolls}")
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
# _cuts.copy()
not_fitted_orders = []
cutted_orders = []

while pivot_roll < len(stock_rolls):
    largest_cut = np.max(length_list(uncut_orders))
    #print(f"Largest cut: {largest_cut}")
    next_cut = length_list(uncut_orders).index(largest_cut)
    if (stock_rolls[pivot_roll] - sum(length_list(cutted_orders))) >= largest_cut:
        # add to cutted_orders
        #print(f"Cutting {largest_cut} from {pivot_roll}")
        cutted_orders.append(uncut_orders.pop(next_cut))
    else:
        # add to not_fitted_orders
        #print(f"Cut {largest_cut} does not fit on {pivot_roll}")
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
# Now fill the largest waste with the largest piece from other roll. 
#
progress = True
previous_max = stock_total
flip = True

while progress or flip:
#while previous_max > max_wasted_length:
    wasted_length = []
    for roll_index, roll_length in enumerate(stock_rolls):
        wasted_length.append(roll_length-sum(length_list(roll_cuts[roll_index])))
    total_wasted_length = sum(wasted_length)
    max_wasted_length = max(wasted_length)
    index_max_wasted_length = wasted_length.index(max_wasted_length)
    other_rolls = list(range(len(wasted_length)))
    other_rolls.pop(index_max_wasted_length)
    max_less_than_max_wasted = 0.0
    index_max_less = -1
    index_roll_max_less = -1
    for other_index in other_rolls:
        other = roll_cuts[other_index]
        #print("Other: ", other)
        for cut_index, cut in enumerate(other):
            if cut[LENGTH] > max_less_than_max_wasted and cut[LENGTH] < max_wasted_length:
                max_less_than_max_wasted = cut[LENGTH]
                index_roll_max_less = other_index
                index_max_less = cut_index
    if index_max_less > 0 and index_roll_max_less > 0:
        # We move from roll index_roll_max_less, cut number index_max_less to index_max_wasted_length
        #print("Index Roll:", index_roll_max_less,", Index Cut: ",index_max_less)
        #print("Roll Cuts: ", roll_cuts[index_roll_max_less])
        the_cut = roll_cuts[index_roll_max_less].pop(index_max_less)
        roll_cuts[index_max_wasted_length].append(the_cut)
        print(f"Previous Max: {previous_max}, New Max: {max_wasted_length} (Flip: {flip})")
        progress = previous_max > max_wasted_length
        previous_max = max_wasted_length
        flip = not flip
        continue
    else:
        print("No other wasted fits rolls")
        break

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
