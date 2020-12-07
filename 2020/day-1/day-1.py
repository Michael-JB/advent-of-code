#!/usr/bin/env python3

import argparse

"""
Part 1: Find the product of a pair    of numbers in the input such that their sum is 2020
Part 2: Find the product of a triplet of numbers in the input such that their sum is 2020

Assumption by me: the same number can be used multiple times, e.g. an input containing 1010.
"""

# Finds two numbers in `values` which sum to `target`
def find_pair_for_sum(values, target):
  for value in values:
    remainder = target - value
    if remainder in values:
      return value, remainder

def solve_part_1(values):
  solution = find_pair_for_sum(values, 2020)
  if solution is not None:
    return solution[0] * solution[1]

def solve_part_2(values):
  # Here we perform a nested loop. Alternatively, we could compute the cartesian product of `values` to avoid nesting.
  for value in values:
    remainder = 2020 - value
    solution = find_pair_for_sum(values, remainder)
    if solution is not None:
      return value * solution[0] * solution[1]

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  # Read input into a set (fast lookup, duplicates are not a concern)
  with open(args.input) as input_file:
    values = set(int(value) for value in input_file.readlines())

    # Solve problems
    solution_to_part_1 = solve_part_1(values)
    print("Solution to part 1:", solution_to_part_1)

    solution_to_part_2 = solve_part_2(values)
    print("Solution to part 2:", solution_to_part_2)

if __name__ == '__main__':
  main()