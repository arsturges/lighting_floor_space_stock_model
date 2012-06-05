'''
floor_space.py
Written for Python 3.2.2.

This file includes the Floor_Space class which defines the building
stock objects and their behaviors.

The building stock of each individual year is represented as one distinct
object of the class "Floor_Space." The object keeps track of its own
state, such as year of construction, current year, region, age, building
type composition, as well as renovations for all years in its history.
In this way, we can establish objects for each year, and ask those objects
about their state at any point in time.'''

import pprint
import copy

class Floor_Space:
    def __init__(self, year_of_construction, total_initial_square_feet, region):
        # total_initial_square_feet is expected to be a dictionary of NEMS
        # building types, not just an integer.
        self.region = region
        self.year_of_construction = year_of_construction
        self.current_year = year_of_construction
        self.total_initial_square_feet = total_initial_square_feet
        self.stock_age = 0
        self.remaining_floor_space_by_year = {} # dictionary of dictionaries;
        self.remaining_floor_space_by_year[self.year_of_construction] = (
            self.total_initial_square_feet)

    def identify(self):
        print("---------------------------------------")
        print("The current year is now", self.year_of_construction + self.stock_age)
        print('My year of construction is', self.year_of_construction)
        print('My initial total square feet was')
        pprint.pprint(self.total_initial_square_feet)
        print('The age of this building stock is', self.stock_age, "years.")
        print(
            "The building code year of the floor space originally constructed \n in",
            self.year_of_construction,
            "has been shifted, according to the following schedule:")
        pprint.pprint(self.remaining_floor_space_by_year)

    def age_n_years(self, n_years):
        '''
        During every year that a particular stock object gets
        older (e.g. the stock built in 1975), a fraction of every
        bin going back to the year of construction is demolished.
        A portion of what remains, from every bin, is then
        renovated. That portion that was renovated is removed from
        the initial bin and moved to the current year's bin.'''
        
        initial_year = self.current_year
        end_year = self.current_year + n_years
        
        while end_year > self.current_year:
            self.current_year += 1
            self.stock_age += 1

            #see what you have:
            self.remaining_floor_space_by_year
            
            #demolish some portion of it (from each year)
            floor_space_to_be_demolished = copy.deepcopy(self.remaining_floor_space_by_year)
            demolished = self.demolish(floor_space_to_be_demolished) #dict
            
            #subtract the demolished portion from the
            #remaining_floor_space_by_year dictionary (year by year)
            #TODO: break this "subtraction" logic into a method
            year = self.year_of_construction
            while year < self.current_year:
                for building_type in [1,2,3,4,5,6,9,10,11,78]:
                    self.remaining_floor_space_by_year[year][building_type] = (
                        self.remaining_floor_space_by_year[year][building_type] -
                        demolished[year][building_type])
                year += 1
            
            #renovate some portion of what's left
            floor_space_to_be_renovated = copy.deepcopy(self.remaining_floor_space_by_year)
            stock_renovated_in_current_year = self.renovate(floor_space_to_be_renovated) #dict
            
            #subtract the renovated portion from the
            #remaining_floor_space_by_year dictionary
            year = self.year_of_construction
            while year < self.current_year:
                for building_type in [1,2,3,4,5,6,9,10,11,78]:
                    existing = self.remaining_floor_space_by_year[year][building_type]
                    renovated = stock_renovated_in_current_year[year][building_type]
                    self.remaining_floor_space_by_year[year][building_type] = existing - renovated
                year += 1

            #get the sum of all renovated space from all years
            total_space_renovated_from_all_bins_in_the_current_year = dict()
            year = self.year_of_construction
            while year < self.current_year:
                for building_type in [1,2,3,4,5,6,9,10,11,78]:
                    if building_type in total_space_renovated_from_all_bins_in_the_current_year:
                        existing = total_space_renovated_from_all_bins_in_the_current_year[building_type]
                        new_from_current_year = stock_renovated_in_current_year[year][building_type]
                        total_space_renovated_from_all_bins_in_the_current_year[building_type] = (
                            existing + new_from_current_year)
                    else:
                        existing = stock_renovated_in_current_year[year][building_type]
                        total_space_renovated_from_all_bins_in_the_current_year[building_type] = existing
                year += 1
            
            #and add the total renovated space to the current year
            self.remaining_floor_space_by_year[self.current_year] = (
                total_space_renovated_from_all_bins_in_the_current_year)

        #print("The", self.year_of_construction, "building stock has been aged by",
              #n_years, "years; the current year is now", self.current_year)

    def renovate(self, floor_space_to_be_renovated):
        '''We can define a renovation rate based on building stock age,
        current year, location, building type, etc. Assume "floor_space"
        is a dictionary object.'''
        year = self.year_of_construction
        while year < self.current_year:
            years_since_last_renovation = self.current_year - year
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
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                floor_space_to_be_renovated[year][building_type] = (
                    rate * floor_space_to_be_renovated[year][building_type])
            year += 1
        return floor_space_to_be_renovated

    def demolish(self, floor_space_to_be_demolished):
        '''we can define a demolition rate based on building stock age,
        current year, location, building tpye, etc. For now, just use
        a static rate. Assume "floor_space" is a dictionary-of-dictionaries object.'''
        year = self.year_of_construction
        while year < self.current_year:
            years_since_construction = self.current_year - self.year_of_construction
            if (years_since_construction < 10) or (self.current_year < 1979):
                rate = 0
            elif years_since_construction < 30:
                rate = 0.005
            elif years_since_construction < 50:
                rate = 0.01
            elif years_since_construction < 70:
                rate = 0.03
            else: # after 1979 and buildings are older than 70, maybe historical
                rate = 0.04
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                floor_space_to_be_demolished[year][building_type] = (
                    rate * floor_space_to_be_demolished[year][building_type])
            year += 1
        return floor_space_to_be_demolished
