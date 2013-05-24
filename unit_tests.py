import unittest
from floor_space import FloorSpace
import pprint
##from load_inputs import LoadInputs
from helper_functions import sum_bin_years
##import csv


class TestRateFunctions(unittest.TestCase):
    def setUp(self):
        self.square_footage = {1:100, 2:100, 3:100, 4:100, 5:100, 6:100, 9:100, 10:100, 11:100, 78:100}
        self.fs = FloorSpace(1990, self.square_footage, 'CA')
        
    def test_renovation_chooser_should_return_correct_rate(self):
        # A 2-year old building has a 0% chance of renovation:
        rate = self.fs.choose_renovation_rate(2)
        self.assertEqual(rate, 0, "2-year-old building should have a 0% renovation rate.")

        # A 13-year old building has a 1% chance of renovation:
        rate = self.fs.choose_renovation_rate(13)
        self.assertEqual(rate, 0.01, "13-year-old building should have a 1% renovation rate.")

        # A 55-year old building has a 10% chance of renovation:
        rate = self.fs.choose_renovation_rate(55)
        self.assertEqual(rate, 0.1, "55-year-old building should have a 10% renovation rate.")

    def test_renovation_chooser_should_return_percentage(self):
        # The function should always return a rate such that 0 <= rate <= 1
        for years_since_renovation in range(100):
            rate = self.fs.choose_renovation_rate(years_since_renovation)
            self.assertGreaterEqual(rate, 0, "renovation rate should be >= 0")
            self.assertLessEqual(rate, 1, "renovation rate should be <= 1")

"""
class TestDistributeToNewBinYear(unittest.TestCase):
    # Receive the newly renovated floor space, the floor space object consisting
    # of the remaining floor space that wasn't renovated, and the year in which
    # the renovation happened, i.e. the new bin_year. Take the newly renovated
    # floor space and add it to a new bin on the original object.

    # bin_year should be +1 greater than largest bin-year of unrenovated floor space object
    def setUp(self):
        self.square_footage = {1:100, 2:100, 3:100, 4:100, 5:100, 6:100, 9:100, 10:100, 11:100, 78:100}
        self.fs = FloorSpace(1990, self.square_footage, 'CA')
        
    def test_bin_year_is_next_greatest_year(self):
        self.fs.age_n_years(10) # now it has 10 bin_years
        pprint.pprint(self.test_object)

    # New object should have one more bin than old object
"""

class TestCombiningBinYears(unittest.TestCase):
    def setUp(self):
        square_footage = {1:100, 2:100, 3:100, 4:100, 5:100, 6:100, 9:100, 10:100, 11:100, 78:100}
        fs1990 = FloorSpace(1990, square_footage, 'CA')
        fs1991 = FloorSpace(1991, square_footage, 'CA')
        self.stock_objects = [fs1990, fs1991]
    def test_function_properly_combines_objects_in_single_region(self):
        pprint.pprint(self.stock_objects[0].remaining_floor_space_by_year)
        self.stock_objects[0].age_n_years(2)
        pprint.pprint(self.stock_objects[0].remaining_floor_space_by_year)
        code_bins = sum_bin_years(self.stock_objects)
        pprint.pprint(code_bins)
        self.assertEqual(code_bins['CA'][1990][1], 100)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main(exit = False)
