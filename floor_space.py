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

class FloorSpace:
    verbose = False
    def __init__(self, year_of_construction, total_initial_square_feet, region):
        # total_initial_square_feet is expected to be a dictionary of NEMS
        # building types, not just an integer.
        self.region = region
        self.year_of_construction = year_of_construction
        self.current_year = year_of_construction
        self.total_initial_square_feet = total_initial_square_feet
        #self.stock_age = 0
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

    def choose_renovation_rate(self, years_since_last_renovation):
        if years_since_last_renovation < 7:
            rate = 0.01
        elif years_since_last_renovation < 15:
            rate = 0.01
        elif years_since_last_renovation < 25:
            rate = 0.05
        elif years_since_last_renovation < 50:
            rate = 0.07
        else:
            rate = 0.1
        return rate

    def choose_demolition_rate(self, years_since_construction):
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
        rate = 0 ############################
        return rate

    def distribute_to_new_bin_year(self, renovated_floor_space, unrenovated_floor_space, bin_year):
        unrenovated_floor_space[bin_year] = dict() #create the new bin_year
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            if not building_type in unrenovated_floor_space[bin_year]:
                unrenovated_floor_space[bin_year][building_type] = renovated_floor_space[building_type]
            else:
                unrenovated_floor_space[bin_year][building_type] += renovated_floor_space[building_type]
        floor_space_after_renovation = unrenovated_floor_space
        return floor_space_after_renovation

    def scrape_off_renovated_floor_space(self, floor_space, temp_floor_space_holder, bin_year, rate):
        if FloorSpace.verbose:
            print("\t\t\t Inside the scrape function, dealing with bin_year", bin_year)
            print("\t\t\t I, the scrape function, have already been handed this much already scraped from prior years:")
            pprint.pprint(temp_floor_space_holder)
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            not_renovated = floor_space[bin_year][building_type] * (1 - rate)
            renovated =     floor_space[bin_year][building_type] * rate

            # (1 - rate) stays in the current bins:
            floor_space[bin_year][building_type] = not_renovated

            # The rest goes into a temporary object
            if not building_type in temp_floor_space_holder:
                temp_floor_space_holder[building_type] = renovated
            else:
                temp_floor_space_holder[building_type] += renovated
        if FloorSpace.verbose:
            print("\t\t\t Here's what's now in the scraped bin", bin_year, ":", sum(temp_floor_space_holder.values()))
            print("\t\t\t Here's what I didn't scrape from this bin_year:", sum(floor_space[bin_year].values()))
            print("\t\t\t Exiting scrape function.")
        return (floor_space, temp_floor_space_holder)

    def age_n_years(self, n_years):
        '''
        During every year that a particular stock object gets
        older (e.g. the stock built in 1975), a fraction of every
        bin going back to the year of construction is demolished.
        A portion of what remains, from every year_bin, is then
        renovated. That portion that was renovated is removed from
        the initial bin and moved to the current year's bin.'''
        if FloorSpace.verbose: print("Started age_n_years function. Current year:", self.current_year, "aging to",self.current_year + n_years)
        initial_year = self.current_year
        end_year = self.current_year + n_years
        
        while end_year > self.current_year:
            # January 1 of current_year

            if FloorSpace.verbose:
                print("Inside the age_n_years loop. See what you have:")
            # See what you have:
            # pprint.pprint(self.remaining_floor_space_by_year)
                print("All of that sums to:")
                for year in self.remaining_floor_space_by_year.keys():
                    print(year,":", sum(self.remaining_floor_space_by_year[year].values()))

            # Increment (at which point it's December 31,
            # the date on which all demoltion and renovation occurs:
            self.current_year += 1

            # Demolish some portion of it (from each year):
            self.remaining_floor_space_by_year = self.demolish(self.remaining_floor_space_by_year)
            
            # Renovate some portion of what's left:
            self.remaining_floor_space_by_year = self.renovate(self.remaining_floor_space_by_year)

        if FloorSpace.verbose:
            print("Finished with age_n_years function.")
            print("Now the floor space object looks like this:")
            final_sum = 0
            for year in self.remaining_floor_space_by_year.keys():
                final_sum += sum(self.remaining_floor_space_by_year[year].values())
                print(year,":", sum(self.remaining_floor_space_by_year[year].values()))
            print("And the final sum is:", final_sum)

    def renovate(self, floor_space_eligible_for_renovation):
        '''We can define a renovation rate based on building stock age,
        current year, location, building type, etc. Assume "floor_space"
        is a dictionary object.'''
        if FloorSpace.verbose: print("\t Entering renovate function.")
        bin_year = self.year_of_construction # Start with the first bin
        floor_space_renovated_into_new_bin_year = dict() # Temporary deposit for renovated floor space (by building type)
        if FloorSpace.verbose: print("\t Current_year:", self.current_year)
        while bin_year < self.current_year:
            if FloorSpace.verbose: print("\t\t ########In the renovate loop, bin_year", bin_year)
            years_since_last_renovation = self.current_year - bin_year
            rate = self.choose_renovation_rate(years_since_last_renovation)
            # Scrape function returns two values:
            floor_space_eligible_for_renovation, floor_space_renovated_into_new_bin_year = \
                self.scrape_off_renovated_floor_space(floor_space_eligible_for_renovation,
                                                      floor_space_renovated_into_new_bin_year,
                                                      bin_year, rate)
            if FloorSpace.verbose:
                print("\t\t Just exited the scrape function, and here's the total scraped:",
                  sum(floor_space_renovated_into_new_bin_year.values()),"as follows:")
                pprint.pprint(floor_space_renovated_into_new_bin_year)
            bin_year += 1

        if FloorSpace.verbose:
            print("\t Finished scraping all available bin years, last bin_year scraped was",bin_year-1)
            print("\t That's how much will be added to the new bin_year, which is", bin_year)

        # Move renovated floor space from new object into new bin in old object:
        floor_space_after_renovation = self.distribute_to_new_bin_year(
            floor_space_renovated_into_new_bin_year,
            floor_space_eligible_for_renovation,
            bin_year)

        return floor_space_after_renovation

    def demolish(self, floor_space_to_be_demolished):
        '''we can define a demolition rate based on building stock age,
        current year, location, building tpye, etc. For now, just use
        a static rate. Assume "floor_space" is a dictionary-of-dictionaries object.'''
        bin_year = self.year_of_construction #start at first bin
        while bin_year < self.current_year:
            years_since_construction = self.current_year - self.year_of_construction
            rate = self.choose_demolition_rate(years_since_construction)

            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                floor_space_to_be_demolished[bin_year][building_type] = (
                    (1 - rate) * floor_space_to_be_demolished[bin_year][building_type])
            bin_year += 1 #go to the next bin
        return floor_space_to_be_demolished
