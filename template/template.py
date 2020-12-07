#!/usr/bin/env python3

import argparse

"""
Description of problem goes here
"""

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  # Read and parse input, e.g. with
  #   `with open(args.input) as input_file:`

  # Print solution, e.g. with
  #   `print("Solution to part 1:", solution_to_part_1)`
  #   `print("Solution to part 2:", solution_to_part_2)`

if __name__ == '__main__':
  main()