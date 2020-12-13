#!/usr/bin/env python3

import argparse
import re

"""
Part 1:
The input program comprises 'nop', 'acc' and 'jmp' instructions, each paired with a signed value,
where 'nop' does nothing, 'acc' increases the value of the accumulator by the value, and 'jmp' jumps
to the line indexed by the sum of the instruction line and the value. Compute the value of the
accumulator at the the point just before an instruction is run for the second time.

Part 2:
Exactly one 'nop' or 'jmp' instruction in the input might be corrupted such that the program does
not terminate. By changing either a 'jmp' to a 'nop', or vice versa, determine the resulting
accumulator value when the program successfully terminates by reaching the EOF.

Assumption: well-formed input
"""

def parse_file(input_file_name):
  instruction_re = re.compile(r"^(nop|acc|jmp)\s((?:\+|-)\d+)$")
  program = []
  with open(input_file_name) as input_file:
    for line in input_file:
      instruction = instruction_re.match(line)
      program.append((instruction[1], int(instruction[2])))
  return program

# Runs a program until an instruction is called twice or the EOF is reached
# Returns the resulting accumulator value, as well as whether or not the EOF was reached
def run(program):
  accumulator, line_number, executed_line_numbers = 0, 0, []
  while line_number not in executed_line_numbers and line_number < len(program):
    executed_line_numbers.append(line_number)
    opcode, operand = program[line_number]
    if opcode == 'nop':
      line_number = line_number + 1
    elif opcode == 'acc':
      accumulator = accumulator + operand
      line_number = line_number + 1
    elif opcode == 'jmp':
      line_number = line_number + operand
  return accumulator, line_number >= len(program)

# Returns all possible programs where exactly one 'jmp' is changed to a 'nop', or vice versa
def get_uncorrupted_candidates(program):
  alternatives = []
  for line_number, (opcode, operand) in enumerate(program):
    if opcode != 'acc':
      alternatives.append([instruction if index != line_number else
                          ('jmp' if opcode == 'nop' else 'nop', operand)
                          for index, instruction in enumerate(program)])
  return alternatives

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  program = parse_file(args.input)

  # Solve problems
  print("Solution to part 1:", run(program)[0])

  # Run all potential uncorrupted candidate programs, and find the first run which reaches EOF
  runs = map(run, get_uncorrupted_candidates(program))
  terminating_run = next(run for run in runs if run[1])
  print("Solution to part 2:", terminating_run[0])

if __name__ == '__main__':
  main()