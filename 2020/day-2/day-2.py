#!/usr/bin/env python3

import argparse

"""
Part 1:
Given an input with a 'policy' and a 'password' on each line, as follows:
  1-3 a: abcde
  1-3 b: cdefg
  2-9 c: ccccccccc
calculate the number of valid passwords in the input, where a password is valid iff the count of the
policy letter in the password is within the policy interval.

Part 2:
Same as above, though now a password is valid iff the letter occurs at exactly one of the two locations
indexed by the policy

Assumption: well-formed input
"""

# This could be improved with RegEx, and it would be nicer to store the data in a more structured manner
def parse_policy(policy):
  dash_split = policy.split('-')
  first_number = int(dash_split[0])
  space_split = dash_split[1].split(' ')
  second_number = int(space_split[0])
  letter = space_split[1]
  return first_number, second_number, letter

def validate_with_count_policy(policy, password):
  count = password.count(policy[2])
  return policy[0] <= count <= policy[1]

def validate_with_index_policy(policy, password):
  extracted_letters = password[policy[0] - 1] + password[policy[1] - 1]
  return extracted_letters.count(policy[2]) == 1

def count_valid_passwords(values, validation_function):
  valid_values = [(policy, password) for (policy, password) in values if validation_function(policy, password)]
  return len(valid_values)

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  with open(args.input) as input_file:
    values = list(tuple(value.split(': ')) for value in input_file.readlines())
    parsed_values = [(parse_policy(value[0]), value[1].strip()) for value in values]

    # Solve problems
    solution_to_part_1 = count_valid_passwords(parsed_values, validate_with_count_policy)
    print("Solution to part 1:", solution_to_part_1)

    solution_to_part_2 = count_valid_passwords(parsed_values, validate_with_index_policy)
    print("Solution to part 2:", solution_to_part_2)


if __name__ == '__main__':
  main()