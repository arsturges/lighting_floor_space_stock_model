'''
main.py
Written for Python 3.2.2
'''
from datetime import datetime
start_time = datetime.now()

from floor_space import FloorSpace
from load_inputs import LoadInputs
import helper_functions
import copy
import pprint
import csv

def print_csv_database_rows(
    current_year,
    bin_years_sum):
    for state in bin_years_sum.keys():
        for year in bin_years_sum[state].keys():
            code_number, code_title = helper_functions.return_code_number_and_title(year, state)
####                sum_across_all_building_types = 0
####                for building_type in [1,2,3,4,5,6,9,10,11,78]:
####                    sum_across_all_building_types += bin_years_sum[state][year][building_type]
####                writer.writerow([current_year,state,year,"All",code_number,code_title,"all floor space:", sum_across_all_building_types])
            covered_floor_space = 0
            uncovered_floor_space = 0
            compliance_rate = 0.25
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                coverage_multiplier = helper_functions.return_coverage_multiplier(
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

# Load the inputs:
inputs = LoadInputs()

# Run the model using convenience methods from helper_functions.py:

with open('results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['snapshot_year',
                     'state',
                     'floor_space_vintage',
                     'building_type',
                     'code_number',
                     'code_title',
                     'subspace',
                     'floor_space'])

# Create a single, complete building stock, age it one year at a time, 
# then sum and print those years.
    start_year = 1900
    end_year = 2030
    _1900_to_2030 = helper_functions.create_building_stock(
        1900, 
        2030, 
        copy.deepcopy(inputs.construction_history))
    for snapshot_year in range(start_year, end_year + 1):
        print("Aging to year", snapshot_year)
        helper_functions.age_building_stock_to_year(_1900_to_2030, snapshot_year)
        code_bins = helper_functions.sum_bin_years(_1900_to_2030, snapshot_year)
        print_csv_database_rows(snapshot_year, code_bins)

end_time = datetime.now()
print("Duration:", end_time - start_time)
