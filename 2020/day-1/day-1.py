import argparse

# Finds two numbers in `values` which sum to `target`
def find_pair_for_sum(values, target):
  for value in values:
    remainder = target - value
    if remainder in values:
      return value, remainder
  return None

def solve_part_1(values):
  solution = find_pair_for_sum(values, 2020)
  if solution is not None:
    return solution[0] * solution[1]
  return None

def solve_part_2(values):
  for value in values:
    remainder = 2020 - value
    filtered_values = set(values)
    filtered_values.remove(value)
    solution = find_pair_for_sum(filtered_values, remainder)
    if solution is not None:
      return value * solution[0] * solution[1]
  return None

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  # Read input into set
  values = set()
  with open(args.input) as input_file:
    for value in input_file:
      values.add(int(value))

  # Solve problems
  solution_to_part_1 = solve_part_1(values)
  print("Solution to part 1:", solution_to_part_1)

  solution_to_part_2 = solve_part_2(values)
  print("Solution to part 2:", solution_to_part_2)

if __name__ == '__main__':
  main()