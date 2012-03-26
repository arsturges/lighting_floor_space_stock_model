'''
The building stock of each individual year is represented as
one distinct object of the class "Floor_Space." The object
keeps track of its own state, such as year of construction,
current year, region, age, as well as renovations for all years in
its history. In this way, we can establish objects for each year,
and ask those objects about their state at any point in time.
'''
import pprint

class Floor_Space:
    verbose = False
    def __init__(self, year_of_construction, total_initial_square_feet, region):
        self.region = region
        self.year_of_construction = year_of_construction
        self.current_year = year_of_construction
        self.total_initial_square_feet = int(float(total_initial_square_feet))
        self.stock_age = 0
        self.initial_code_year = self.year_of_construction
        self.remaining_floor_space_by_year = {} # dictionary; (key=year, value=square feet)
        self.remaining_floor_space_by_year[self.year_of_construction] = self.total_initial_square_feet

    def identify(self):
        print("---------------------------------------")
        print("The current year is now", self.year_of_construction + self.stock_age)
        print('My year of construction is', self.year_of_construction)
        print('My initial total square feet was', format(self.total_initial_square_feet, ',d'))
        print('The age of this building stock is', self.stock_age, "years.")
        print(
            "The building code year of the floor space originally constructed \n in",
            self.year_of_construction,
            "has been shifted, according to the following schedule:")
        pprint.pprint(self.remaining_floor_space_by_year)

    def age_n_years(self, n_years):
        '''
        During every year that a particular stock object gets
        older (e.g. the stock built in 1975, a fraction of every
        bin going back to the year of construction is demolished.
        A portion of what remains, from every bin, is then
        renovated. That portion that was renovated is removed from
        the initial bin and moved to the current year's bin.'''
        
        initial_year = self.current_year
        end_year = self.current_year + n_years
        
        if Floor_Space.verbose: print("Okay I'm going to age the", self.year_of_construction,
              "building stock by", n_years, " years.")
        if Floor_Space.verbose: print("The current year is now", self.current_year,".")
        if Floor_Space.verbose: print("For each of the next",n_years,
              "years, we're going to age the stock, \n demolish some from each year, and renovate some.")
        while end_year > self.current_year:
            self.current_year += 1
            self.stock_age += 1

            #see what you have:
            self.remaining_floor_space_by_year
            if Floor_Space.verbose: print("It's now the start of", self.current_year, "; here's the stock we have:")
            if Floor_Space.verbose: pprint.pprint(self.remaining_floor_space_by_year)

            #demolish some portion of it (from each year)
            if Floor_Space.verbose: print("Now we'll demolish 1% from each year:")
            floor_space_to_be_demolished = self.remaining_floor_space_by_year.copy() #make a shallow copy
            demolished = self.demolish(floor_space_to_be_demolished) #dict
            if Floor_Space.verbose: pprint.pprint(demolished)

            #subtract the demolished portion from the
            #remaining_floor_space_by_year dictionary (year by year)
            if Floor_Space.verbose: print("Now we'll subtract that amount from what we started with:")
            year = self.year_of_construction
            while year < self.current_year:                
                self.remaining_floor_space_by_year[year] = (
                    self.remaining_floor_space_by_year[year] - demolished[year])
                year += 1
            if Floor_Space.verbose: print("That leaves us with:")
            if Floor_Space.verbose: pprint.pprint(self.remaining_floor_space_by_year)

            #renovate some portion of what's left
            if Floor_Space.verbose: print("Of that amount, we'll renovate 1%, which means moving that floor space \n out of its original year and into the current year, whcih is", self.current_year)
            floor_space_to_be_renovated = self.remaining_floor_space_by_year.copy() #make a shallow copy
            stock_renovated_in_current_year = self.renovate(floor_space_to_be_renovated) #dict
            if Floor_Space.verbose: print("what's being renovated:", stock_renovated_in_current_year)

            #subtract the renovated portion from the remaining_floor_space_by_year dictionary
            if Floor_Space.verbose: print("Now we'll move that renovated portion out of its original year bins \n and into", self.current_year)
            year = self.year_of_construction
            while year < self.current_year:
                self.remaining_floor_space_by_year[year] = (
                    self.remaining_floor_space_by_year[year] - stock_renovated_in_current_year[year])
                year += 1

            #get the sum of all renovated space from all years
            total_space_renovated_from_all_bins_in_the_current_year = 0
            if Floor_Space.verbose: print("Here's the total space that was renovated from all the year bins:")
            if Floor_Space.verbose: pprint.pprint(stock_renovated_in_current_year)
            year = self.year_of_construction
            while year < self.current_year:
                total_space_renovated_from_all_bins_in_the_current_year += stock_renovated_in_current_year[year]
                year += 1
            if Floor_Space.verbose: print("The total of all those years is", total_space_renovated_from_all_bins_in_the_current_year,". \n That's the amount we'll add to the", self.current_year, "bin.")

            #and add the total renovated space to the current year
            self.remaining_floor_space_by_year[self.current_year] = total_space_renovated_from_all_bins_in_the_current_year

            if Floor_Space.verbose: print("With that addition, the new totals are:")
            if Floor_Space.verbose: pprint.pprint(self.remaining_floor_space_by_year)

        print("The", self.year_of_construction, "building stock has been aged by", n_years, "years; the current year is now", self.current_year)

    def renovate(self, floor_space_to_be_renovated):
        '''we can define a renovation rate based on
        building stock age, current year, location, etc.
        For now, just use a static rate.
        Assume "floor_space" is a dictionary object.'''
        year = self.year_of_construction
        while year < self.current_year:
            floor_space_to_be_renovated[year] = 0.01 * floor_space_to_be_renovated[year]
            year += 1
        return floor_space_to_be_renovated

    def demolish(self, floor_space_to_be_demolished):
        '''we can define a demolition rate based on
        building stock age, current year, location, etc.
        For now, just use a static rate.
        Assume "floor_space" is a dictionary object.'''
        year = self.year_of_construction
        while year < self.current_year:
            floor_space_to_be_demolished[year] = 0.06 * floor_space_to_be_demolished[year]
            year += 1
        return floor_space_to_be_demolished