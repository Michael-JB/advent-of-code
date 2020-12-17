#!/usr/bin/env python3

import argparse
import re

"""
Part 1:
Read in a set of ship movement actions and compute the manhattan distance from the starting point
after applying each action in turn. Possible actions:
  N: move north by the given value.
  S: move south by the given value.
  E: move east by the given value.
  W: move west by the given value.
  L: turn left the given number of degrees.
  R: turn right the given number of degrees.
  F: move forward by the given value in the direction the ship is currently facing.

Part 2:
Again calculate the manhattan distance from the starting point, but this time a waypoint is
introduced whose position is relative to the ship. The actions now mean:
  N: move the waypoint north by the given value.
  S: move the waypoint south by the given value.
  E: move the waypoint east by the given value.
  W: move the waypoint west by the given value.
  L: rotate the waypoint about the ship anti-clockwise the given number of degrees.
  R: rotate the waypoint about the ship clockwise the given number of degrees.
  F: move forward to the waypoint a number of times equal to the given value.

Assumption: well-formed input
"""

NORTH, SOUTH, EAST, WEST, LEFT, RIGHT, FORWARD = 'N', 'S', 'E', 'W', 'L', 'R', 'F'
COMPASS = [NORTH, EAST, SOUTH, WEST]

def parse_file(input_file_name):
  actions = ''.join([NORTH, SOUTH, EAST, WEST, LEFT, RIGHT, FORWARD])
  action_re = re.compile(r"^([" + actions + r"])(\d+)$")
  with open(input_file_name) as input_file:
    actions = [action_re.match(action).groups() for action in input_file]
    return [(action, int(value)) for action, value in actions]

def apply_action(action, ship, wp=None):
  a, v = action
  if   a in COMPASS: wp.compass_move(a, v)                if wp else ship.compass_move(a, v)
  elif a == FORWARD: ship.vector_move(wp.x * v, wp.y * v) if wp else ship.compass_move(ship.r, v)
  else             : wp.rotate_about_origin(a, v)         if wp else ship.rotate_about_self(a, v)

def apply_actions(actions, ship, waypoint=None):
  for action in actions: apply_action(action, ship, waypoint)

class NauticalObject:
  def __init__(self, x, y):
    self.x, self.y = x, y

  def compass_move(self, compass_direction, distance):
    if   compass_direction == NORTH: self.y = self.y + distance
    elif compass_direction == SOUTH: self.y = self.y - distance
    elif compass_direction ==  EAST: self.x = self.x + distance
    elif compass_direction ==  WEST: self.x = self.x - distance

  def vector_move(self, x, y):
    self.x = self.x + x
    self.y = self.y + y

  def manhattan_distance(self):
    return abs(self.x) + abs(self.y)

  def rotate_about_origin(self, direction, angle):
    direction_sign = 1 if direction == RIGHT else -1
    for _ in range(0, int((angle % 360) / 90)):
      self.x, self.y = direction_sign * self.y, -direction_sign * self.x

class Ship(NauticalObject):
  def __init__(self, x, y, r):
    super().__init__(x, y)
    self.r = r

  def rotate_about_self(self, direction, angle):
    angle_sign = 1 if direction == RIGHT else -1
    self.r = COMPASS[(COMPASS.index(self.r) + int(angle * angle_sign / 90)) % len(COMPASS)]

class Waypoint(NauticalObject):
  pass

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  actions = parse_file(args.input)

  # Solve problems
  ship = Ship(0, 0, EAST)
  apply_actions(actions, ship)
  print("Solution to part 1:", ship.manhattan_distance())

  ship, waypoint = Ship(0, 0, EAST), Waypoint(10, 1)
  apply_actions(actions, ship, waypoint)
  print("Solution to part 2:", ship.manhattan_distance())

if __name__ == '__main__':
  main()