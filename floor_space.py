'''
floor_space.py
Written for Python 3.2.2.

This file includes the Floor_Space class which defines the building
stock object and its behavior.

The building stock of each individual year is represented as one distinct
object of the class "Floor_Space." The object keeps track of its own
state, such as year of construction, current year, region, age, building
type composition, as well as renovations for all years in its history.
In this way, we can establish objects for each year, and ask those objects
about their state at any point in time.'''

import pprint

#TODO: Make most of these methods private

class FloorSpace:
    def __init__(self, year_of_construction, total_initial_square_feet, region):
        # total_initial_square_feet is expected to be a dictionary of NEMS
        # building types, not just an integer.
        assert type(total_initial_square_feet) == dict, "Square footage must be dictionary"
        self.region = region
        self.year_of_construction = year_of_construction
        self.current_year = year_of_construction
        self.total_initial_square_feet = total_initial_square_feet
        self.remaining_floor_space_by_year = {} # dictionary of dictionaries;
        self.remaining_floor_space_by_year[self.year_of_construction] = (
            self.total_initial_square_feet) 
            # but this should be an array of building types, no?

    def choose_renovation_rate(self, years_since_last_renovation):
        if years_since_last_renovation < 7:
            rate = 0
        elif years_since_last_renovation < 15:
            rate = 0.01
        elif years_since_last_renovation < 25:
            rate = 0.05
        elif years_since_last_renovation < 50:
            rate = 0.07
        else:
            rate = 0.1
        return rate
    
    def age_n_years(self, n_years):
        '''
        During every year that a particular stock object gets older (e.g. the
        stock built in 1975), a fraction of every bin going back to the year
        of construction is demolished. A portion of what remains, from every 
        year_bin, is then renovated. That portion that was renovated is
        removed from the initial bin and moved to the current year's bin.
        '''
        assert type(n_years) == int
        if n_years < 1:
            message = "You tried to age it {} years. You must age it at \
                least one year.".format(n_years)
            raise RuntimeError(message)

        initial_year = self.current_year
        end_year = self.current_year + n_years
    
        while end_year > self.current_year:
            self.current_year += 1
            self.demolish()
            self.renovate()

    def renovate(self):
        bin_years = self.remaining_floor_space_by_year.keys()
        # Set up a new bin if needed:
        if not self.current_year in self.remaining_floor_space_by_year.keys():
            self.remaining_floor_space_by_year[self.current_year] = {}
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                self.remaining_floor_space_by_year[self.current_year][building_type] = 0

        for bin_year in bin_years:
            years_since_last_renovation = self.current_year - bin_year
            rate = self.choose_renovation_rate(years_since_last_renovation)
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                # Put a fraction of floor space into the new bin:
                self.remaining_floor_space_by_year[self.current_year][building_type] += rate * self.remaining_floor_space_by_year[bin_year][building_type] 
                # And reduce the old bin by the same amount:
                self.remaining_floor_space_by_year[bin_year][building_type] = (1-rate) * self.remaining_floor_space_by_year[bin_year][building_type]

    def demolish(self):
        '''
        We can define a demolition rate based on building stock age,
        current year, location, building type, etc. Assume "floor_space" is 
        a dictionary-of-dictionaries object.
        '''
        # If floor space exists up to year a, it must have a year 
        # bin from the previous year:
        assert self.current_year - 1 in self.remaining_floor_space_by_year # e.g. fstbd[1992]
        renovation_year = self.year_of_construction #start at first bin
        while renovation_year < self.current_year:
            """ Each renovation year has it's own age. If a 100-year-old building is
            renovated, it's chance of demolition goes down to that of a 1-
            year-old building. """
            floor_space_age = self.current_year - renovation_year 
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                survival_rate = self.surviving_proportion_wrapper(
                    building_type,
                    floor_space_age)
                surviving_floor_space = survival_rate * self.remaining_floor_space_by_year[renovation_year][building_type]
                self.remaining_floor_space_by_year[renovation_year][building_type] = surviving_floor_space
            renovation_year += 1

    def surviving_proportion_wrapper(self, building_type, building_age):
        """
        This wraps `surviving_proportion` so that it takes building type and 
        age instead of age, lifetime, and gamma. Gammas and median lifetimes 
        come from table 5.2, 'Assumptions to the aeo 2012'
        http://www.eia.gov/forecasts/aeo/assumptions/pdf/commercial.pdf
        """
        assert type(building_type)==int, "building_type must be an integer"
        gammas = {
            1:2.2, # assembly
            2:2.1, # education
            3:2.3, # food sales
            4:2.0, # food service
            5:2.5, # health care
            6:2.1, # lodging
            9:2.2, # merc/service
            10:2.0, # warehouse
            11:2.3, # other
            78:2.0 # large office and small ofice
            }
        gamma = gammas[building_type]

        median_lifetimes= {
            1:55, # assembly
            2:62, # education
            3:55, # food sales
            4:50, # food service
            5:55, # health care
            6:53, # lodging
            9:50, # merc/service
            10:58, # warehouse
            11:60, # other
            78:(65+58)/2 # large office and small ofice
            }
        median_lifetime = median_lifetimes[building_type]
        surviving_proportion = self.surviving_proportion(
            building_age,
            median_lifetime,
            gamma)
        return surviving_proportion

    def surviving_proportion(self, building_age, median_lifetime, gamma):
        """
        Source: http://www.eia.gov/forecasts/aeo/assumptions/pdf/commercial.pdf
        This is the survival function, taken from AEO 2012. Gamma values are given
        in table 5.2.
        """
        building_age = float(building_age)
        median_lifetime = float(median_lifetime)
        gamma = float(gamma)
        assert gamma>0, "Gamma must be greater than 0 for survival function."
            # See page 59 of NEMS Commercial Demand Module Documentation Report 2001
        surviving_proportion = 1/(1+(building_age/median_lifetime)**gamma)
        return surviving_proportion

if __name__ == "__main__":
    constructed_floor_space = {1:10, 2:10, 3:10, 4:10,5:10,6:10,9:10,10:10,11:10,78:10}
    obj = FloorSpace(1990, constructed_floor_space, 'CA')
    obj.current_year # 1990
    obj.age_n_years(2) 
    obj.current_year # 1990 + n
    obj.year_of_construction # 1990
    obj.region # 'CA'
    pprint.pprint(obj.remaining_floor_space_by_year)
