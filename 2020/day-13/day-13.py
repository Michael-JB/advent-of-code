#!/usr/bin/env python3

import argparse

"""
Part 1:
Given a target time and a list of bus arrival frequencies, determine the frequency which, when
multiplied by some value, is both above and closest to the target time.

Part 2:
Bus arrivals are said to converge at time `t` iff. it holds that the bus at index `i` arrives at
time `t + i` for all i. For example, consider the following input:
  7,13,x,x,59
These busses converge at time 350, as 7*50=350, 27*13=351 and 59*6=354. Calculate the time of the
first convergence of the busses in the input.

Assumption: well-formed input
"""

def exceed_target(value, target):
  total = 0
  while total < target: total = total + value
  return value, total

# Determines whether the busses fulfill the requirements of convergence at the given time
def have_converged(time, busses):
  if time == 0: return False
  for index, value in busses:
    if (time + index) % value != 0: return False
  return True

# Efficiently computes the time of the first convergence of all busses
# The efficiency comes from the observation that, after the initial convergence, the time between
# subsequent convergences is constant. This function exploits this fact to narrow the search area
def first_convergence(busses):
  time, increment = 0, busses[0][1]
  for i in range(1, len(busses) + 1):
    first_i_busses = busses[:i]
    time = next_convergence(time, increment, first_i_busses)
    increment = next_convergence(time + increment, increment, first_i_busses) - time
  return time

# Starting at the given time, incrementally checks subsequent times until a convergence is found
def next_convergence(time, increment, busses):
  while not have_converged(time, busses): time = time + increment
  return time

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  with open(args.input) as input_file:
    lines = input_file.read().splitlines()
    target = int(lines[0])
    # Format busses in (index, id) pairs
    busses = [(i, int(v)) for i, v in enumerate(lines[1].split(',')) if v.isnumeric()]

    # Solve problems
    arrival = min([exceed_target(v[1], target) for v in busses], key=lambda pair: pair[1])
    print("Solution to part 1:", (arrival[1] - target) * arrival[0])
    print("Solution to part 2:", first_convergence(busses))

if __name__ == '__main__':
  main()