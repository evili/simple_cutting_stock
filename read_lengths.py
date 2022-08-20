import pathlib
from typing import List
import re
from math import ceil
def get_data(infile:str)->List[float]:
    """ Reads a file of numbers and returns a list of (count, number) pairs."""
    _p = pathlib.Path(infile)
    input_text = _p.read_text()
    numbers = [float(n) for n in re.findall(r'[0-9.]+', _p.read_text())]
    return numbers 

