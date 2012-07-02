from floor_space import *

def create_building_stock(start_build_year, end_build_year, construction_data):
    # Assumes construction_data spans start and end years.
    # Mass-create a building stock.
    building_stock_objects = list()
    for state in construction_data.keys():
        for i in range(start_build_year, end_build_year + 1):
            building_stock_objects.append(FloorSpace(i, construction_data[str(state)][i], str(state)))
    return building_stock_objects

def age_building_stock_to_year(building_stock_objects, year):
    # Age a list of building_stock_objects to year.
    for i in range(len(building_stock_objects)):
        start_year = building_stock_objects[i].current_year
        building_stock_objects[i].age_n_years(year - start_year)
    return building_stock_objects

def sum_bin_years(stock_objects, sum_to_year):
    # Combine all individual FloorSpace objects into one.
    # Show a complete picture of all existing floor space bins by state, year,
    # and building type, as it exists in the 'sum-to year'.
    # bin_years_sum['CA'][1950][78] = 2467.937 (floor space from all years having a 1950 bin)
    bin_years_sum = dict()
    for stock_object in stock_objects:
        end_year = stock_object.current_year
        if sum_to_year >= end_year:
            state = stock_object.region
            start_year = stock_object.year_of_construction
            end_year = stock_object.current_year
            if not state in bin_years_sum:
                bin_years_sum[state] = dict()
            for year in range(start_year, end_year + 1):
                if not year in bin_years_sum[state]:
                    bin_years_sum[state][year] = dict()
                for building_type in [1,2,3,4,5,6,9,10,11,78]:
                    if not building_type in bin_years_sum[state][year]:
                        bin_years_sum[state][year][building_type] = 0
                    bin_years_sum[state][year][building_type] += stock_object.remaining_floor_space_by_year[year][building_type]
    return bin_years_sum
