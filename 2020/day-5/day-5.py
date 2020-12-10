#!/usr/bin/env python3

import argparse
import math

"""
Part 1:
Implement a 'binary space partitioning' parser. Given a list of 10-letter inputs each
comprising 'F', 'B', 'L' and 'R', compute the row and column which the inputs encode.
Starting with the number range 0-127, a leading 'F' corresponds to the lower half (0-63)
and a leading 'B' corresonds to the upper half (64-127). The second letter corresponds to
the position in the remaining half, with the column being similarly encoded with 'L' and
'R' in the latter three letters. The unique seat id is computed with: row * 8 + column

Examples:
  BFFFBBFRRR: row 70, column 7, seat ID 567.
  FFFBBBFRRR: row 14, column 7, seat ID 119.
  BBFFBBFRLL: row 102, column 4, seat ID 820.

Part 2:
Find the only id s.t. both (id-1) amd (id+1) are valid ids in the input

Assumption: well-formed input
"""

# Returns the row and column, respectively, encoded by the input
def decode(code):
  row_low, row_high = 0, 127
  col_low, col_high = 0, 7

  for letter in code:
    if   letter == 'F': row_high = row_low + math.floor((row_high - row_low) / 2)
    elif letter == 'B': row_low = row_low + math.ceil((row_high - row_low) / 2)
    elif letter == 'L': col_high = col_low + math.floor((col_high - col_low) / 2)
    elif letter == 'R': col_low = col_low + math.ceil((col_high - col_low) / 2)

  return row_low, col_low

def compute_id(row, column):
  return row * 8 + column

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  with open(args.input) as input_file:
    codes = [row.strip() for row in input_file.readlines()]

    decoded_codes = [decode(code) for code in codes]
    ids = [compute_id(row, column) for row, column in decoded_codes]

    # Solve problems
    print("Solution to part 1:", max(ids))

    ids.sort()
    for i in range(len(ids) - 1):
      if ids[i + 1] - ids[i] != 1: print("Solution to part 2:", ids[i] + 1)

if __name__ == '__main__':
  main()