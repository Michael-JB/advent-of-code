#!/usr/bin/env python3

import argparse

"""
Part 1:
Given a list of numbers ('joltages'), find the distribution of differences of the ordered joltages,
returning the sum of the count of 1-jolt and 3-jolt differences.

Part 2:
Count the number of possible joltage chains such that each link in each chain spans no more than 3.

Assumption: well-formed input
"""

# Sorts the input joltages, prepends 0 and appends the maximum joltage plus three
def prepare_joltages(joltages):
  joltages.sort()
  return [0] + joltages + [joltages[-1] + 3]

# Returns the differences between each joltage (i.e. the length spanned by each link in the chain)
def get_differences(prepared_joltages):
  pairs = zip(prepared_joltages[:-1], prepared_joltages[1:])
  return list(map(lambda pair : pair[1] - pair[0], pairs))

# Counts the number of alternative chains to the one that includes all joltages
# This function is recursive, and is optimised with memoization
def count_alternative_permutations(joltages, mem={}):
  current_joltage, remaining_joltages, permutations = joltages[0], joltages[1:], 0
  candidate_next_joltages = filter(lambda j : current_joltage + 3 >= j, remaining_joltages[:3])
  for i, joltage in enumerate(candidate_next_joltages):
    if joltage not in mem:
      mem[joltage] = count_alternative_permutations(remaining_joltages[i:], mem)
    permutations = permutations + mem[joltage] + (1 if i > 0 else 0)
  return permutations

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  with open(args.input) as input_file:
    joltages = prepare_joltages([int(value) for value in input_file.readlines()])

    # Solve problems
    differences = get_differences(joltages)
    print("Solution to part 1:", differences.count(1) * differences.count(3))
    print("Solution to part 2:", 1 + count_alternative_permutations(joltages))

if __name__ == '__main__':
  main()