#!/usr/bin/env python3

import argparse
import re

"""
Part 1:
Given an input containing masks and memory writes of the form:
  mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
  mem[8] = 11
  mem[7] = 101
  mem[8] = 0
Calculate the sum of the values in memory after all writes are processed, where the non-'X' bits in
the mask replace the corresponding bits in each subsequent value written to memory.

Part 2:
Decoder version 2: masks apply to memory addresses, not values, and now only overwrite address bits
when the corresponding mask bits are set. 'X' now corresponds to a floating bit, where each floating
bit takes on both possible values. As such, each single memory write command may modify more than
one memory address.

Assumption: well-formed input
"""

# Mask constants
X, SET, UNSET = 'X', '1', '0'

# Define opcodes
MASK, MEM = 0, 1

def parse_file(input_file_name):
  mask_re = re.compile(r'^mask\s=\s([X01]{36})$')
  mem_re  = re.compile(r'^mem\[(\d+)\]\s=\s(\d+)$')
  program = []
  with open(input_file_name) as input_file:
    for line in input_file:
      mask_match = mask_re.match(line.strip())
      mem_match = mem_re.match(line.strip())
      if mask_match:  program.append((MASK, mask_match[1]))
      elif mem_match: program.append((MEM, (int(mem_match[1]), int(mem_match[2]))))
  return program

# Returns an integer value after replacing in the value all provided bits in the mask
def apply_version_1_mask(mask, value):
  and_mask, or_mask = int(mask.replace(X, SET), 2), int(mask.replace(X, UNSET), 2)
  return (value & and_mask) | or_mask

# Returns the binary string of the value ORed with the mask, retaining the floating bits
def apply_version_2_mask(mask, value):
  masked_value = value | int(mask.replace(X, UNSET), 2)
  value_string = format(masked_value, '036b')
  floating_indices = [i for i, val in enumerate(mask) if val == X]
  return ''.join([X if i in floating_indices else val for i, val in enumerate(value_string)])

# Given a string value (potentially with floating bits), return all possible decoded values
def expand_floating(value):
  if X not in value: return [int(value, 2)]
  return expand_floating(value.replace(X, UNSET, 1)) + expand_floating(value.replace(X, SET, 1))

# Runs a parsed program using the semantics of the given decoder version
def run_program(program, decoder_version):
  mem = {}
  current_mask = X * 36
  for opcode, operand in program:
    if opcode == MASK:
      current_mask = operand
    elif opcode ==  MEM:
      if decoder_version == 1:
        mem[operand[0]] = apply_version_1_mask(current_mask, operand[1])
      elif decoder_version == 2:
        addresses = expand_floating(apply_version_2_mask(current_mask, operand[0]))
        for address in addresses:
          mem[address] = operand[1]
  return mem

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  program = parse_file(args.input)

  print("Solution to part 1:", sum(run_program(program, 1).values()))
  print("Solution to part 2:", sum(run_program(program, 2).values()))

if __name__ == '__main__':
  main()