from floor_space import *
from load_inputs import LoadInputs

inputs = LoadInputs()
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

def print_single_floor_space_object(floor_space_object):
    current_year = floor_space_object.current_year
    state = floor_space_object.region
    for bin_year in floor_space_object.remaining_floor_space_by_year.keys():
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            total_floor_space = \
                floor_space_object.remaining_floor_space_by_year[bin_year][building_type]                
            writer.writerow([current_year,state,bin_year,building_type,"NA","NA","NA",total_floor_space])

def return_code_number_and_title(year, state):
    code_compliance = inputs.code_compliance
    code_key = inputs.code_key
    if year in code_compliance[state]:
        code_number = code_compliance[state][year] #these are strings; deal with it sometime
        code_title = code_key[int(code_number)]
    else:
        code_number = 99
        code_title = "Pre-2002 Building Code"
    return code_number, code_title

def return_coverage_multiplier(building_type, code_number):
    floor_space_coverage_by_code = inputs.floor_space_coverage_by_code
    if code_number in floor_space_coverage_by_code[building_type].keys():
        coverage_multiplier = float(floor_space_coverage_by_code[building_type][code_number])
    else:
        coverage_multiplier = 0
    return coverage_multiplier

def print_csv_database_rows(current_year, bin_years_sum, writer):
    for state in bin_years_sum.keys():
        for year in bin_years_sum[state].keys():
            code_number, code_title = return_code_number_and_title(year, state)
####                sum_across_all_building_types = 0
####                for building_type in [1,2,3,4,5,6,9,10,11,78]:
####                    sum_across_all_building_types += bin_years_sum[state][year][building_type]
####                writer.writerow([current_year,state,year,"All",code_number,code_title,"all floor space:", sum_across_all_building_types])
            covered_floor_space = 0
            uncovered_floor_space = 0
            compliance_rate = 0.25
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                coverage_multiplier = return_coverage_multiplier(
                    building_type,
                    code_number) * compliance_rate
                covered_floor_space += bin_years_sum[state][year][building_type] * coverage_multiplier
                uncovered_floor_space += bin_years_sum[state][year][building_type] * (1 - coverage_multiplier)
            writer.writerow([
                current_year,
                state,
                year,
                building_type,
                code_number,
                code_title,
                'covered:',
                covered_floor_space])
            writer.writerow([
                current_year,
                state,
                year,
                building_type,
                code_number,
                code_title,
                'uncovered:',
                uncovered_floor_space])

if __name__ == "__main__":
    print(return_coverage_multiplier(78,16))
