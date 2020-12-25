#!/usr/bin/env python3

import argparse

"""
Part 1:
Given a starting list of numbers, what is the number after 2020 turns if on each turn the following
rules are applied:
  - If the latest number has not been seen before, the next number is 0
  - Otherwise, the next number is the count of turns since the number was last seen

Part 2:
With the same rules as before, what is the number after 30000000 turns?

Assumption: well-formed input
"""

# Computes the resulting number after the starting numbers are continued to the given turn count
# This function is made more efficient by maintaining the history of numbers in an inverted index,
# where the keys are the numbers and the values are the index of the last occurrence of the key.
def play(starting_numbers, turns):
  history = {number: i + 1 for i, number in enumerate(starting_numbers[:-1])}
  current_number = starting_numbers[-1]
  for i in range(len(starting_numbers), turns):
    next_number = i - history[current_number] if current_number in history else 0
    history[current_number] = i
    current_number = next_number
  return current_number

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  with open(args.input) as input_file:
    numbers = [int(n) for n in input_file.readline().split(',')]

    print("Solution to part 1:", play(numbers, 2020))
    print("Solution to part 2:", play(numbers, 30000000))

if __name__ == '__main__':
  main()