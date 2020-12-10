#!/usr/bin/env python3

import argparse
import re

"""
Part 1:
Implement a parser for 'passports' which determines the count of valid passwords.

The expected fields are:
  byr (Birth Year)
  iyr (Issue Year)
  eyr (Expiration Year)
  hgt (Height)
  hcl (Hair Color)
  ecl (Eye Color)
  pid (Passport ID)
  cid (Country ID) (Optional)

Part 2:
Implement field validation:
  byr (Birth Year) - four digits; at least 1920 and at most 2002.
  iyr (Issue Year) - four digits; at least 2010 and at most 2020.
  eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
  hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
  hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
  ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
  pid (Passport ID) - a nine-digit number, including leading zeroes.
  cid (Country ID) - ignored, missing or not.

Assumption: well-formed input
"""

REQUIRED_PASSPORT_FIELDS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

VALID_EYE_COLOURS = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

MIN_BIRTH_YEAR, MAX_BIRTH_YEAR           = 1920, 2002
MIN_ISSUE_YEAR, MAX_ISSUE_YEAR           = 2010, 2020
MIN_EXPIRATION_YEAR, MAX_EXPIRATION_YEAR = 2020, 2030

MIN_HEIGHT_CM, MAX_HEIGHT_CM = 150, 193
MIN_HEIGHT_IN, MAX_HEIGHT_IN = 59, 76

def are_required_fields_present(passport):
  for field in REQUIRED_PASSPORT_FIELDS:
    if field not in passport: return False
  return True

def is_passport_valid(passport):
  if not are_required_fields_present(passport):     return False
  if not is_birth_year_valid(passport['byr']):      return False
  if not is_issue_year_valid(passport['iyr']):      return False
  if not is_expiration_year_valid(passport['eyr']): return False
  if not is_height_valid(passport['hgt']):          return False
  if not is_hair_colour_valid(passport['hcl']):     return False
  if not is_eye_colour_valid(passport['ecl']):      return False
  if not is_passport_id_valid(passport['pid']):     return False
  return True

def is_year_valid(year, minimum, maximum):
  is_four_digits = re.match(r"^\d{4}$", year)
  if not is_four_digits: return False
  return minimum <= int(year) <= maximum

def is_birth_year_valid(byr):
  return is_year_valid(byr, MIN_BIRTH_YEAR, MAX_BIRTH_YEAR)

def is_issue_year_valid(iyr):
  return is_year_valid(iyr, MIN_ISSUE_YEAR, MAX_ISSUE_YEAR)

def is_expiration_year_valid(eyr):
  return is_year_valid(eyr, MIN_EXPIRATION_YEAR, MAX_EXPIRATION_YEAR)

def is_height_valid(hgt):
  is_valid_format = re.match(r"^(\d{2,3})(cm|in)$", hgt)
  if not is_valid_format: return False
  height, unit = is_valid_format.group(1, 2)
  if unit == "cm": return MIN_HEIGHT_CM <= int(height) <= MAX_HEIGHT_CM
  else: return MIN_HEIGHT_IN <= int(height) <= MAX_HEIGHT_IN

def is_hair_colour_valid(hcl):
  return re.match(r"^#[0-9a-f]{6}$", hcl)

def is_eye_colour_valid(ecl):
  return ecl in VALID_EYE_COLOURS

def is_passport_id_valid(pid):
  return re.match(r"^\d{9}$", pid)

def count_valid_passwords(passports, validation_function):
  valid_passports = [passport for passport in passports if validation_function(passport)]
  return len(valid_passports)

def parse_file(input_file_name):
  passports = []
  with open(input_file_name) as input_file:
    current_passport = {}
    for line in input_file:
      stripped_line = line.strip()
      if stripped_line != "":
        for line_split in stripped_line.split():
          entry = line_split.split(":")
          current_passport[entry[0]] = entry[1]
      else:
        passports.append(current_passport)
        current_passport = {}
    # If input doesn't end with a newline, handle this
    if current_passport != {}:
      passports.append(current_passport)
  return passports

def test_validation():
  invalid_years = ["abcd", "-1234", "50000", "?!@£", "202020", "0", "560_"]

  # byr
  assert not is_birth_year_valid("1919")
  for year in range(1920, 2002 + 1):
    assert is_birth_year_valid(str(year))
  assert not is_birth_year_valid("2003")
  for invalid_year in invalid_years:
    assert not is_birth_year_valid(invalid_year)

  # iyr
  assert not is_birth_year_valid("2009")
  for year in range(2010, 2020 + 1):
    assert is_issue_year_valid(str(year))
  assert not is_birth_year_valid("2021")
  for invalid_year in invalid_years:
    assert not is_issue_year_valid(invalid_year)

  # eyr
  assert not is_birth_year_valid("2019")
  for year in range(2020, 2030 + 1):
    assert is_expiration_year_valid(str(year))
  assert not is_birth_year_valid("2031")
  for invalid_year in invalid_years:
    assert not is_expiration_year_valid(invalid_year)

  # hgt
  assert not is_height_valid("123ab")
  assert not is_height_valid("hello")
  assert not is_height_valid("!@%&")
  assert not is_height_valid("149cm")
  assert not is_height_valid("194cm")
  assert not is_height_valid("58in")
  assert not is_height_valid("77in")
  assert not is_height_valid("190")
  for height_cm in range(150, 193 + 1):
    assert is_height_valid(str(height_cm) + "cm")
  for height_in in range(59, 76 + 1):
    assert is_height_valid(str(height_in) + "in")

  # hcl
  assert is_hair_colour_valid("#123abc")
  assert not is_hair_colour_valid("#1111111")
  assert not is_hair_colour_valid("#123abz")
  assert not is_hair_colour_valid("123abz")

  # ecl
  for eye_colour in VALID_EYE_COLOURS:
    assert is_eye_colour_valid(eye_colour)
  assert not is_eye_colour_valid("abc")
  assert not is_eye_colour_valid("123")
  assert not is_eye_colour_valid("am")

  # pid
  assert is_passport_id_valid("000000001")
  assert not is_passport_id_valid("0123456789")
  assert not is_passport_id_valid("abcdefghi")

  print("All tests passed.")

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='a text file containing the Advent of Code problem input')
  args = parser.parse_args()

  passports = parse_file(args.input)

  test_validation()

  # Solve problems
  print("Solution to part 1:", count_valid_passwords(passports, are_required_fields_present))
  print("Solution to part 2:", count_valid_passwords(passports, is_passport_valid))

if __name__ == '__main__':
  main()