#!/usr/bin/env python3

import argparse
from itertools import combinations

"""
Part 1:
Given a list of numbers, find the first value which is not the sum of any two of the preceding 25
numbers. The list of numbers is prepended by 25 random numbers (the 'preamble').

Part 2:
Find a contiguous sub-list of at least length two which sums to the invalid number from part 1.
Return the sum of the smallest and largest number in this sub-list.

Assumption: well-formed input
"""

def find_invalid_value(values, preamble_length):
  for i, value in enumerate(values[preamble_length:]):
    preceding_values = values[i:i+preamble_length]
    preceding_pairs = combinations(preceding_values, 2)
    if not any(map(lambda v : v == value, map(sum, preceding_pairs))):
      return value

def find_contiguous_sum(values, target):
  left_ptr, right_ptr = 0, 0
  while True:
    sublist = values[left_ptr:right_ptr]
    sublist_sum = sum(sublist)
    if   sublist_sum == target: return sublist
    elif sublist_sum <  target: right_ptr = right_ptr + 1
    elif sublist_sum >  target: left_ptr  = left_ptr  + 1

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  parser.add_argument('preamble_length', metavar='preamble-length',
    help='the number of values to consider as the input preamble', type=int)
  args = parser.parse_args()

  with open(args.input) as input_file:
    values = [int(value) for value in input_file.readlines()]

    # Solve problems
    invalid_value = find_invalid_value(values, args.preamble_length)
    print("Solution to part 1:", invalid_value)
    contiguous_sublist = find_contiguous_sum(values, invalid_value)
    print("Solution to part 2:", min(contiguous_sublist) + max(contiguous_sublist))

if __name__ == '__main__':
  main()