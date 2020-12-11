#!/usr/bin/env python3

import argparse

"""
Part 1:
Count the sum of the number of unique letters in each input group, where the groups are
separated by a blank line

Part 2:
Count the sum of the number of shared letters in each input group

Assumption: well-formed input
"""

def parse_file(input_file_name):
  groups = []
  with open(input_file_name) as input_file:
    current_group = []
    for line in input_file:
      stripped_line = line.strip()
      if stripped_line != "":
        current_group.append(stripped_line)
      else:
        groups.append(current_group)
        current_group = []
    # If input doesn't end with a newline, handle this
    if current_group != []: groups.append(current_group)
  return groups

def count_answers(groups, set_function):
  return sum([len(set_function(*map(set, group))) for group in groups])

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  groups = parse_file(args.input)

  # Solve problems
  print("Solution to part 1:", count_answers(groups, set.union))
  print("Solution to part 2:", count_answers(groups, set.intersection))

if __name__ == '__main__':
  main()