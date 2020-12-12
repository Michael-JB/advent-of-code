#!/usr/bin/env python3

import argparse
import re

"""
Part 1:
Given an input with a 'policy' and a 'password' on each line, as follows:
  1-3 a: abcde
  1-3 b: cdefg
  2-9 c: ccccccccc
calculate the number of valid passwords in the input, where a password is valid iff. the count of
the policy letter in the password is within the policy interval.

Part 2:
Same as above, though now a password is valid iff the letter occurs at exactly one of the two
locations indexed by the policy

Assumption: well-formed input
"""

policy_re = re.compile(r'^(\d+)-(\d+)\s([a-z]):\s([a-z]+)$')

def parse_line(policy_string):
  parsed_value = policy_re.match(policy_string)
  return (int(parsed_value[1]), int(parsed_value[2]), parsed_value[3]), parsed_value[4]

def validate_with_count_policy(policy, password):
  count = password.count(policy[2])
  return policy[0] <= count <= policy[1]

def validate_with_index_policy(policy, password):
  extracted_letters = password[policy[0] - 1] + password[policy[1] - 1]
  return extracted_letters.count(policy[2]) == 1

def count_valid_passwords(values, validation_function):
  valid_values = [(pol, pas) for pol, pas in values if validation_function(pol, pas)]
  return len(valid_values)

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  with open(args.input) as input_file:
    values = [parse_line(policy_string.strip()) for policy_string in input_file.readlines()]

    # Solve problems
    solution_to_part_1 = count_valid_passwords(values, validate_with_count_policy)
    print("Solution to part 1:", solution_to_part_1)

    solution_to_part_2 = count_valid_passwords(values, validate_with_index_policy)
    print("Solution to part 2:", solution_to_part_2)


if __name__ == '__main__':
  main()