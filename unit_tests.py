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

class Renovation(unittest.TestCase):
    """
    Check that the correct amount of floor space from each renovation bin is
    getting moved into the current_year bin.
    """
    def setUp(self):
        self.square_footage = {1:100, 2:100, 3:100, 4:100, 5:100, 6:100, 9:100, 10:100, 11:100, 78:100}
        self.fs = FloorSpace(1990, self.square_footage, 'CA')

    def test_renovation_shifts_bins_correctly(self):
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            self.assertEqual(self.fs.remaining_floor_space_by_year[1990][building_type], 100)
        for year in range(1990, 1996):
            self.fs.current_year +=1
            self.fs.renovate()
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                self.assertEqual(self.fs.remaining_floor_space_by_year[1990][building_type], 100)
        # All floor space should have remained in the 1990 bin, because renovation_rate was 0:
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1990].values()), 10*100)
        self.assertEqual(self.fs.total_remaining_floor_space(), 10*100)

        # now advance it one year, and there should be a positive renovation rate.
        # current year is 1996 until we advance, so it'll renovate 1990 bins and put them into 1997
        self.fs.current_year += 1 # so now it's 1997
        self.fs.renovate() # renovate 1% of 1990 bin, put it into 1997:
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1990].values()), 99*10)
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1997].values()), 1*10)
        # in-between bins should have nothing:
        for year_bin in range(1991,1997):
            self.assertEqual(sum(self.fs.remaining_floor_space_by_year[year_bin].values()), 0)

        # Advance another year, 1% of all bins get moved to 1998, total sum should still be 10*100 (self.square_footage)
        self.fs.current_year += 1 # so now it's 1998
        self.fs.renovate() # renovate 1% of 1990 bin and 0% of 1997 bin, put it into 1998:
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1990].values()), 10*100*.99*.99)
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1997].values()), 1*10)
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1998].values()), 10*100*.01*.99)
        self.assertEqual(self.fs.total_remaining_floor_space(), 10*100)

        # One more year, and I think we can say it's working:
        self.fs.current_year += 1 # so now it's 1999
        self.fs.renovate() # renovate 1% of 1990 bin and 0% of 1997 bin and 0% of 1998 bin, put it into 1999:
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1990].values()), 10*100*.99*.99*.99)
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1997].values()), 1*10)
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1998].values()), 10*100*.01*.99)
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1998].values()), 10*100*.01*.99)
        self.assertEqual(sum(self.fs.remaining_floor_space_by_year[1999].values()), 10*100*.99*.99*.01)
        self.assertEqual(self.fs.total_remaining_floor_space(), 10*100)


class Demolition(unittest.TestCase):
    """
    Check that the correct amount of floor space is being removed/demolished
    from each bin.
    """

    def setUp(self):
        self.square_footage = {1:100, 2:100, 3:100, 4:100, 5:100, 6:100, 9:100, 10:100, 11:100, 78:100}
        self.fs = FloorSpace(1990, self.square_footage.copy(), 'CA')

    def test_demolition(self):
        self.assertEqual(self.fs.total_remaining_floor_space(), 10*100)
        self.fs.current_year += 1 # now it's 1991
        self.fs.demolish()

        building_age = self.fs.current_year - self.fs.year_of_construction
        self.assertEqual(building_age, 1)
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            surviving_proportion = self.fs.surviving_proportion_wrapper(building_type, building_age)
            self.assertEqual(self.fs.remaining_floor_space_by_year[1990][building_type], 100*surviving_proportion)

    def test_demolish_consecutive_years(self):
        # Further years require renovate() to create later years' year_bins. Instead we create a simple fixture:
        fs_later = FloorSpace(1990, self.square_footage.copy(), 'CA')
        self.assertEqual(fs_later.total_remaining_floor_space(), 10*100)
        fs_later.current_year += 1 #1991
        fs_later.remaining_floor_space_by_year[1991]={1:0,2:0,3:0,4:0,5:0,6:0,9:0,10:0,11:0,78:0}
        self.assertEqual(fs_later.total_remaining_floor_space(), 10*100)
        fs_later.current_year += 1 #1992
        fs_later.remaining_floor_space_by_year[1992]={1:5,2:5,3:5,4:5,5:5,6:5,9:5,10:5,11:5,78:5}
        # So now each bin in 1990 has 100, 1991 has 0, and 1992 has 5. Total sum should 10*100+10*5
        self.assertEqual(fs_later.current_year, 1992)
        self.assertEqual(fs_later.total_remaining_floor_space(), 10*100 + 10*0 + 10*5)

        """ Now we have a FloorSpace object with 1990 (100 each), 1991 (0 each), and 1992 (5 each) bins. 
        Advance one more year into 1993, and demolish the 1990, 1991, and 1992 bins:"""

        fs_later.current_year +=1 # now 1993
        self.assertEqual(fs_later.current_year, 1993)
        fs_later.demolish()
    
        # Now check that each bin has exactly what it should:
    
        #1990 bin is 3 years old
        building_age = fs_later.current_year - 1990
        surviving_proportion90={}
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            surviving_proportion90[building_type] =fs_later.surviving_proportion_wrapper(building_type, building_age)
            self.assertEqual(fs_later.remaining_floor_space_by_year[1990][building_type], 100*surviving_proportion90[building_type])

        #1991 bin is 2 years old
        building_age = fs_later.current_year - 1991
        surviving_proportion91={}
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            surviving_proportion91[building_type] =fs_later.surviving_proportion_wrapper(building_type, building_age)
            self.assertEqual(fs_later.remaining_floor_space_by_year[1991][building_type], 0*surviving_proportion91[building_type])

        #1992 bin is 1 years old
        building_age = fs_later.current_year - 1992
        surviving_proportion92={}
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            surviving_proportion92[building_type] =fs_later.surviving_proportion_wrapper(building_type, building_age)
            self.assertEqual(fs_later.remaining_floor_space_by_year[1992][building_type], 5*surviving_proportion92[building_type])

        # Now go one more year, and demo it again:
        # First create a new 1994 renovation bin:
        fs_later.remaining_floor_space_by_year[1993]={1:5,2:5,3:5,4:5,5:5,6:5,9:5,10:5,11:5,78:5}
        fs_later.current_year +=1 # 1994
        fs_later.demolish()

        #1990 bin is 4 years old
        self.assertEqual(fs_later.current_year, 1994)
        building_age = fs_later.current_year - 1990
        surviving_proportion90b={}
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            surviving_proportion90b[building_type] =fs_later.surviving_proportion_wrapper(building_type, building_age)
            self.assertEqual(fs_later.remaining_floor_space_by_year[1990][building_type], 100*surviving_proportion90[building_type]*surviving_proportion90b[building_type])

        #1991 bin is 3 years old
        building_age = fs_later.current_year - 1991
        surviving_proportion91b={}
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            surviving_proportion91b[building_type] =fs_later.surviving_proportion_wrapper(building_type, building_age)
            self.assertEqual(fs_later.remaining_floor_space_by_year[1991][building_type], 0)

        #1992 bin is 2 years old
        building_age = fs_later.current_year - 1992
        surviving_proportion92b={}
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            surviving_proportion92b[building_type] =fs_later.surviving_proportion_wrapper(building_type, building_age)
            self.assertEqual(fs_later.remaining_floor_space_by_year[1992][building_type], 5*surviving_proportion92[building_type]*surviving_proportion92b[building_type])

        #1993 bin is 1 years old
        building_age = fs_later.current_year - 1993
        surviving_proportion93b={}
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            surviving_proportion93b[building_type] =fs_later.surviving_proportion_wrapper(building_type, building_age)
            self.assertEqual(fs_later.remaining_floor_space_by_year[1993][building_type], 5*surviving_proportion93b[building_type])

        print "90"
        pprint.pprint(surviving_proportion90)
        print "90b"
        pprint.pprint(surviving_proportion90b)
        print "91"
        pprint.pprint(surviving_proportion91)
        print "91b"
        pprint.pprint(surviving_proportion91b)
        print "92"
        pprint.pprint(surviving_proportion92)
        print "92b"
        pprint.pprint(surviving_proportion92b)
        print "93b"
        pprint.pprint(surviving_proportion93b)

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

    # New object should have one more bin than old object

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
