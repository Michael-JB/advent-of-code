#!/usr/bin/env python3

import argparse
from operator import mul
from functools import reduce

"""
Part 1:
Given an input 'ski slope', where '.'s represent open space and '#'s represent trees:
  ..##.......
  #...#...#..
  .#....#..#.
  ..#.#...#.#
  .#...##..#.
  ..#.##.....
  .#.#.#....#
  .#........#
  #.##...#...
  #...##....#
  .#..#...#.#
calculate the number of trees encountered when moving from the top left to below the bottom row
with vector steps of (3 right, 1 down).

Part 2:
Calculate the product of the number of trees encountered when moving with each of the following
vectors: (1, 1), (3, 1), (5, 1), (7, 1), (1, 2)

Assumption: well-formed input
"""

def count_trees(slope, step_col, step_row):
  slope_width, slope_height = len(slope[0]), len(slope)
  count = col = 0
  for row in range(0, slope_height, step_row):
    col_wrapped = col % slope_width
    if slope[row][col_wrapped]: count = count + 1
    col = col + step_col
  return count

def parse_row(row):
  return [False if obj == '.' else True for obj in row.strip()]

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  with open(args.input) as input_file:
    slope = [parse_row(row) for row in input_file.readlines()]

    # Solve problems
    solution_to_part_1 = count_trees(slope, 3, 1)
    print("Solution to part 1:", solution_to_part_1)

    part_2_vectors = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    part_2_counts = [count_trees(slope, vector[0], vector[1]) for vector in part_2_vectors]
    solution_to_part_2 = reduce(mul, part_2_counts, 1)
    print("Solution to part 2:", solution_to_part_2)

if __name__ == '__main__':
  main()