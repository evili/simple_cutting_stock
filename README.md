# simple_cutting_stock

A minimalistic naive approach to the
[cutting stock problem](https://en.wikipedia.org/wiki/Cutting_stock_problem).
The (only) advantage of this method is that it cant take several lengths for the stock rolls.


## Inputs

* `order_cuts.csv`: List of cuts to be done (with repetitions), first column label, second label length.
* `stock_rolls.csv`: List of stock rolls to cut from (with repetitions), first column label, second label length.

## Strategy

* Begin with the largest stock roll
* Try to cut the largest pending cut from the present stock roll.
* If there are no cuts that can fit on the current roll, advance to the next roll.
