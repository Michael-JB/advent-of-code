#!/usr/bin/env python3

import argparse

"""
Part 1:
Given a seating plan, where 'L's correspond to empty seats, '.'s correspond to floor and '#'s
correspond to occupied seats, apply the following rules until a stable state is reached:
  - If a seat is empty and there are no occupied seats adjacent (including diagonals) to it, the
    seat becomes occupied.
  - If a seat is occupied and four or more seats adjacent to it are also occupied, the seat becomes
    empty.
  - Otherwise, the seats state does not change.
Calculate the number of occupied seats in this stable state.

Part 2:
Rather than considering adjacent seats, raycast in each of the eight directions and consider the
first visible seat. Apply the same rule as before, this time with a vacation threshold of 5 visible
occupied seats.

Assumption: well-formed input
"""

EMPTY, OCCUPIED, FLOOR = 'L', '#', '.'
VACATE_THRESHOLD_PART_1, VACATE_THRESHOLD_PART_2 = 4, 5

def parse_file(input_file_name):
  seating_plan = []
  with open(input_file_name) as input_file:
    for row in input_file:
      seating_plan.append([seat for seat in row.strip()])
  return seating_plan

# Returns a list containing all adjacent seats
def adjacent_seats(row, col, seating_plan):
  seats = []
  for r in range(row-1, row+2):
    for c in range(col-1, col+2):
      if r >= 0 and r < len(seating_plan) and c >= 0 and c < len(seating_plan[r]):
        if not (r == row and c == col): seats.append(seating_plan[r][c])
  return seats

# Returns a list containing the first encountered seat in each of the eight directions
def visible_seats(row, col, seating_plan):
  width, height = len(seating_plan[0]), len(seating_plan)
  inc_r, inc_c = range(row + 1, height), range(col + 1, width)
  dec_r, dec_c = range(row - 1, -1, -1), range(col - 1, -1, -1)
  const_r, const_c = [row] * height, [col] * width

  directions = [
    zip(dec_r,   const_c), # North
    zip(dec_r,   inc_c  ), # North-East
    zip(const_r, inc_c  ), # East
    zip(inc_r,   inc_c  ), # South-East
    zip(inc_r,   const_c), # South
    zip(inc_r,   dec_c  ), # South-West
    zip(const_r, dec_c  ), # West
    zip(dec_r,   dec_c  )  # North-West
  ]

  seats = []
  for direction in directions:
    for location in direction:
      seat = seating_plan[location[0]][location[1]]
      if seat != FLOOR:
        seats.append(seat)
        break

  return seats

# Determines the next state of a seat, given its adjacent seats
def apply_rule(seat, vacate_threshold, adjacent_seats):
  if seat == FLOOR: return FLOOR
  elif OCCUPIED not in adjacent_seats: return OCCUPIED
  elif adjacent_seats.count(OCCUPIED) >= vacate_threshold: return EMPTY
  else: return seat

# Advances the seating plan to its next state
def epoch(seating_plan, vacate_threshold, adjacency_function):
  return [[apply_rule(seat, vacate_threshold, adjacency_function(r, c, seating_plan))
         for c, seat in enumerate(row)]
         for r, row  in enumerate(seating_plan)]

# Advances the seating plan until it is in a stable, unchanging state
def epoch_until_unchanged(seating_plan, vacate_threshold, adjacency_function):
  while True:
    new_seating_plan = epoch(seating_plan, vacate_threshold, adjacency_function)
    if seating_plan == new_seating_plan:
      break
    seating_plan = new_seating_plan
  return seating_plan

def count_occupied(seating_plan):
  return len([seat for row in seating_plan for seat in row if seat == OCCUPIED])

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  seating_plan = parse_file(args.input)

  stable_plan_1 = epoch_until_unchanged(seating_plan, VACATE_THRESHOLD_PART_1, adjacent_seats)
  print("Solution to part 1:", count_occupied(stable_plan_1))
  stable_plan_2 = epoch_until_unchanged(seating_plan, VACATE_THRESHOLD_PART_2, visible_seats)
  print("Solution to part 2:", count_occupied(stable_plan_2))

if __name__ == '__main__':
  main()