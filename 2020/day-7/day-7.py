#!/usr/bin/env python3

import argparse
import re

"""
Part 1:
Given a number of bag rules, determine the count of unique enclosing bags for a given input
bag name. For example, given the following input, a "shiny gold" bag can be contained in 4
bags: "bright white" and "muted yellow" directly, and "light red" and "dark orange" indirectly.
  light red bags contain 1 bright white bag, 2 muted yellow bags.
  dark orange bags contain 3 bright white bags, 4 muted yellow bags.
  bright white bags contain 1 shiny gold bag.
  muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
  shiny gold bags contain no other bags.
  faded blue bags contain no other bags.

Part 2:
Count the number of (sub-)bags contained within the input bag. For example, in the above input,
"light red" bags contain 1 + 1 + 2 + 2 * (2 + 9) = 26.

Assumption: well-formed input
"""

def parse_file(input_file_name):
  parent_re = re.compile(r"^([a-zA-Z]+\s[a-zA-Z]+)")
  child_re  = re.compile(r"(\d+)\s([a-zA-Z]+\s[a-zA-Z]+)")
  bags = {}
  with open(input_file_name) as input_file:
    for line in input_file:
      key = parent_re.match(line)[0]
      children = [(int(match[1]), match[2]) for match in child_re.finditer(line)]
      bags[key] = children
  return bags

# Finds the unique outer-most bags which can contain the input bag name
def get_top_level_bags(bags, bag_name):
  parent_bags = set(find_bags_which_contain(bags, bag_name).keys())
  top_level_bags = set()
  for bag in parent_bags:
    top_level_bags |= get_top_level_bags(bags, bag)
  return parent_bags.union(top_level_bags)

# Returns a dictionary with all bags which contain the input bag name
def find_bags_which_contain(bags, bag_name):
  return {bag: contents for bag, contents in bags.items() if bag_name in [c[1] for c in contents]}

# Counts the total number of (sub-)bags contained within the given bag
def count_contents(bags, bag):
  return sum([c[0] + c[0] * count_contents(bags, c[1]) for c in bags[bag]])

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  parser.add_argument('bag', help='the bag name to solve for, e.g. "shiny gold"')
  args = parser.parse_args()

  bags = parse_file(args.input)

  # Solve problems
  print("Solution to part 1:", len(get_top_level_bags(bags, args.bag)))
  print("Solution to part 2:", count_contents(bags, args.bag))

if __name__ == '__main__':
  main()