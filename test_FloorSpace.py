import unittest
from floor_space import FloorSpace
import pprint
from helper_functions import sum_bin_years
import copy


class TestRateFunctions(unittest.TestCase):
    def setUp(self):
        self.square_footage = {
            1:100,
            2:100,
            3:100,
            4:100,
            5:100,
            6:100,
            9:100,
            10:100,
            11:100,
            78:100}

    def tearDown(self):
        pass

class TestAging(unittest.TestCase):
    def setUp(self):
        self.square_footage = {
            1:100,
            2:100,
            3:100,
            4:100,
            5:100,
            6:100,
            9:100,
            10:100,
            11:100,
            78:100}

    def test_aging(self):
        # Test that aging in separate consecutive periods
        # has same effect as one longer period:

        _1980a = FloorSpace(1980, self.square_footage, 'USA')
        _1980b = FloorSpace(1980, self.square_footage, 'USA')

        _1980a.age_n_years(15)
        _1980b.age_n_years(3)
        _1980b.age_n_years(2)
        _1980b.age_n_years(5)
        _1980b.age_n_years(5)
        
        self.assertEqual(_1980a.current_year, _1980b.current_year)
        for year in range(1980, 1986):
            self.assertEqual(_1980a.remaining_floor_space_by_year[year], _1980b.remaining_floor_space_by_year[year])

    def test_ageing_generates_correct_number_of_bins(self):
        fs_object = FloorSpace(1990, self.square_footage, 'CA')
        # Should have one year-bin upon instantiation:
        self.assertEqual(fs_object.remaining_floor_space_by_year.keys(), [1990])
        fs_object.age_n_years(3) # After this it should have 4:
        self.assertEqual(
            [1990,1991,1992,1993], 
            sorted(fs_object.remaining_floor_space_by_year.keys()))
        fs_object.age_n_years(3) # After this it should have 7:
        self.assertEqual(
            [1990,1991,1992,1993,1994,1995,1996], 
            sorted(fs_object.remaining_floor_space_by_year.keys()))
        self.assertEqual(fs_object.current_year, 1996)

    def test_renovation(self):
        _1990 = FloorSpace(1990, self.square_footage, 'USA')
        five_year_rate = _1990.choose_renovation_rate(5)
        # If the rate is zero, there should be nothing the five-year bin:
        _1990.age_n_years(5)
        if five_year_rate == 0:
            for b_type in [1,2,3,4,5,6,9,10,11,78]:
                self.assertEqual(_1990.remaining_floor_space_by_year[1995][b_type], 0)

    def test_ageing_demolishes_correct_floor_space(self):
        _1990 = FloorSpace(1990, self.square_footage, 'USA')
        education_surviving_after_1_year = _1990.surviving_proportion_wrapper(2,1)
        food_service_surviving_after_1_year = _1990.surviving_proportion_wrapper(4,1)

        _1990.age_n_years(1)
        self.assertEqual(
            _1990.remaining_floor_space_by_year[1990][2],
            self.square_footage[2] * education_surviving_after_1_year)
        self.assertEqual(
            _1990.remaining_floor_space_by_year[1990][4],
            self.square_footage[4] * food_service_surviving_after_1_year)

if __name__ == "__main__":
    unittest.main(exit = False)
