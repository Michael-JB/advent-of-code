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

def count_occurrences(letter, list_of_strings):
  return len([string for string in list_of_strings if letter in string])

def count_shared_letters(group):
  return len([l for l in set("".join(group)) if count_occurrences(l, group) == len(group)])

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  groups = parse_file(args.input)

  # Solve problems
  unique_counts = sum(map(lambda group : len(set("".join(group))), groups))
  print("Solution to part 1:", unique_counts)

  shared_counts = sum(map(count_shared_letters, groups))
  print("Solution to part 2:", shared_counts)

if __name__ == '__main__':
  main()