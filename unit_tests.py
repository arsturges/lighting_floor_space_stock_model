import unittest
from floor_space import FloorSpace
import pprint
##from load_inputs import LoadInputs
##from helper_functions import *
##import csv


class TestRateFunctions(unittest.TestCase):
    def test_renovation_chooser_should_return_correct_rate(self):
        # A 2-year old building has a 0% chance of renovation:
        self.rate = FloorSpace.choose_renovation_rate(self, 2)
        self.assertEqual(self.rate, 0, "2-year-old building should have a 0% renovation rate.")

        # A 13-year old building has a 1% chance of renovation:
        self.rate = FloorSpace.choose_renovation_rate(self, 13)
        self.assertEqual(self.rate, 0.01, "13-year-old building should have a 1% renovation rate.")

        # A 55-year old building has a 10% chance of renovation:
        self.rate = FloorSpace.choose_renovation_rate(self, 55)
        self.assertEqual(self.rate, 0.1, "55-year-old building should have a 10% renovation rate.")

    def test_renovation_chooser_should_return_percentage(self):
        # The function should always return a rate such that 0 <= rate <= 1
        for years_since_renovation in range(100):
            self.rate = FloorSpace.choose_renovation_rate(self, years_since_renovation)
            self.assertGreaterEqual(self.rate, 0, "renovation rate should be >= 0")
            self.assertLessEqual(self.rate, 1, "renovation rate should be <= 1")

class TestDistributeToNewBinYear(unittest.TestCase):
    # Receive the newly renovated floor space, the floor space object consisting
    # of the remaining floor space that wasn't renovated, and the year in which
    # the renovation happened, i.e. the new bin_year. Take the newly renovated
    # floor space and add it to a new bin on the original object.

    # bin_year should be +1 greater than largest bin-year of unrenovated floor space object
    def test_bin_year_is_next_greatest_year(self):
        self.test_object = FloorSpace(1900, 123456789, 'CA') # TODO: randomize this in a setUp method
        self.test_object.age_n_years(10) # now it has 10 bin_years
        pprint.pprint(self.test_object)

    # New object should have one more bin than old object


unittest.main(exit = False)
