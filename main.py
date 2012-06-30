'''
main.py
Written for Python 3.2.2
'''
from datetime import datetime
start_time = datetime.now()

from floor_space import FloorSpace
from load_inputs import LoadInputs
from helper_functions import *
import pprint
import csv
import cProfile

def main():

    def print_single_floor_space_object(floor_space_object):
        current_year = floor_space_object.current_year
        state = floor_space_object.region
        for bin_year in floor_space_object.remaining_floor_space_by_year.keys():
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                total_floor_space = \
                    floor_space_object.remaining_floor_space_by_year[bin_year][building_type]                
                writer.writerow([current_year,state,bin_year,building_type,"NA","NA","NA",total_floor_space])

    def print_csv_database_rows(
        current_year,
        bin_years_sum,
        code_compliance,
        floor_space_coverage_by_code):
        for state in bin_years_sum.keys():
            for year in bin_years_sum[state].keys():
                if year in code_compliance[state]:
                    code_number = int(code_compliance[state][year])
                    code_title = code_key[code_number]
                else:
                    code_number = 0
                    code_title = "none specified"
                covered_floor_space = 0
                uncovered_floor_space = 0
                for building_type in [1,2,3,4,5,6,9,10,11,78]:
                    if code_number in floor_space_coverage_by_code[str(building_type)].keys():
                        coverage_multiplier = float(floor_space_coverage_by_code[str(building_type)][code_number])
                    else:
                        coverage_multiplier = 0
                    covered_floor_space += bin_years_sum[state][year][building_type] * coverage_multiplier
                    uncovered_floor_space += bin_years_sum[state][year][building_type] * (1 - coverage_multiplier)
                writer.writerow([current_year,state,year,building_type,code_number,code_title,'covered:',covered_floor_space])
                writer.writerow([current_year,state,year,building_type,code_number,code_title,'uncovered:',uncovered_floor_space])

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

    # Create a single FloorSpace object, age it, and print it out:
##        _1900 = FloorSpace(1900, inputs.construction_history['CA'][1900], 'CA')
##        _1900.age_n_years(10)
##        print_single_floor_space_object(_1900)

    # Create a single snapshot consisting of a list of FloorSpace objects,
    # each aged to the same point in time:
        _1900_to_1903 = create_building_stock(1900, 1903, copy.deepcopy(inputs.construction_history))
        age_building_stock_to_year(_1900_to_1903, 1903, inputs)
        code_bins = sum_bin_years(_1900_to_1903)
        print_csv_database_rows(1903, code_bins, inputs.code_compliance, inputs.floor_space_coverage_by_code)

        _1900_to_1904 = create_building_stock(1900, 1904, copy.deepcopy(inputs.construction_history))
        age_building_stock_to_year(_1900_to_1904, 1904, inputs)
        code_bins = sum_bin_years(_1900_to_1904)
        print_csv_database_rows(1904, code_bins, inputs.code_compliance, inputs.floor_space_coverage_by_code)

    # Create a range of snapshots
##        start_year = 1900
##        end_year = 1910
##        for snapshot_year in range(start_year, end_year + 1):
##            start_time_stamp = datetime.now()
##            print("Creating a snapshot object spanning", start_year,"--",snapshot_year)
##            snapshot = create_building_stock(start_year, snapshot_year, copy.deepcopy(inputs.construction_history))
##            print("Now aging it to", snapshot_year)
##            age_building_stock_to_year(snapshot, snapshot_year)
##            code_bins = sum_bin_years(snapshot)
##            print_csv_database_rows(snapshot_year, code_bins, inputs.code_compliance, inputs.floor_space_coverage_by_code)
##            end_time_stamp = datetime.now()
##            print("Duration between years:", end_time_stamp - start_time_stamp)

main()
#cProfile.run('main()')


end_time = datetime.now()
print("Duration:", end_time - start_time)

