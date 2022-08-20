# stock_cutting

A minimalistic naive approach to the stock cutting problem

## Inputs
order_cuts.txt: List of cuts to be done (with repetitions).
stock_rolls.txt: List of stock rolls to cut from (with repetitions).

## Strategy

* Begin with the largest stock roll
* Try to cut the largest pending cut from the present stock roll.
* If there are no cuts that can fit on the current roll, advance to the next roll.
