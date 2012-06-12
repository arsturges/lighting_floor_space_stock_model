'''
main.py
Written for Python 3.2.2
'''
from datetime import datetime
start_time = datetime.now()

from csv_functions import *
from floor_space import FloorSpace
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
        code_bins_in_current_year,
        code_compliance,
        floor_space_coverage_by_code):
        for state in code_bins_in_current_year.keys():
                for year in code_bins_in_current_year[state].keys():
                    if year in code_compliance[state]:
                        code_number = code_compliance[state][year]
                        code_title = code_key[code_number]
                    else:
                        code_number = 0
                        code_title = "none specified"
                    covered_floor_space = 0
                    uncovered_floor_space = 0
                    for building_type in [1,2,3,4,5,6,9,10,11,78]:
                        if int(code_number) in floor_space_coverage_by_code[str(building_type)].keys():
                            coverage_multiplier = float(floor_space_coverage_by_code[str(building_type)][int(code_number)])
                        else:
                            coverage_multiplier = 0
                        covered_floor_space += code_bins_in_current_year[state][year][building_type] * coverage_multiplier
                        uncovered_floor_space += code_bins_in_current_year[state][year][building_type] * (1 - coverage_multiplier)
                    writer.writerow([current_year,state,year,building_type,code_number,code_title,'covered:',covered_floor_space])
                    writer.writerow([current_year,state,year,building_type,code_number,code_title,'uncovered:',uncovered_floor_space])


    # Define the inputs:
    starts = 'csv_inputs/construction_history_by_state.csv'
    state_cendiv_correspondance = 'csv_inputs/states_cendivs.csv'
    cendiv_NEMS_percentages = 'csv_inputs/cendivs_NEMS_percentages.csv'
    floor_space_coverage_by_code = 'csv_inputs/floor_space_under_building_lighting_automatic_shutoff.csv'

    # Intermediate steps to convert the inputs to usable arrays and dictionaries
    construction_history_by_state = convert_csv_to_dictionary_of_dictionaries(starts)
    states_cendivs = dict(csv.reader(open(state_cendiv_correspondance))) # states_cendivs['AZ'] == '8'.
    cendiv_NEMS = import_3_column_data(cendiv_NEMS_percentages)
    construction_history = add_NEMS_building_types_to_construction_history(
        construction_history_by_state,
        states_cendivs,
        cendiv_NEMS)
    floor_space_coverage_by_code = convert_csv_to_dictionary_of_dictionaries(floor_space_coverage_by_code)

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

        start_year = 1975
        end_year = 1985

##        print("start creating building stock objects")
##        _1900_to_2030 = create_building_stock(1900, 2030, construction_history)
##        print("finished creating stock objects")
##        print("start aging.")
##        age_building_stock_to_year(_1900_to_2030, 2030)
##        print("finished aging.")
##        print("assembling code bins.")
##        code_bins = return_code_bins_in_current_year(_1900_to_2030)
##        print("finished assembling code bins.")
##        print("start printing rows.")
##        print_csv_database_rows(2030, code_bins, code_compliance, floor_space_coverage_by_code)
##        print("finished printing rows. Done.")

        for snapshot_year in range(start_year, end_year + 1):
            print("snapshot_year is:", snapshot_year)
            start_time_stamp = datetime.now()
            snapshot = create_building_stock(start_year, snapshot_year, construction_history)
            age_building_stock_to_year(snapshot, snapshot_year)
            code_bins = return_code_bins_in_current_year(snapshot)
            print_csv_database_rows(snapshot_year, code_bins, code_compliance, floor_space_coverage_by_code)
            end_time_stamp = datetime.now()
            print("Duration between years:", end_time_stamp - start_time_stamp)


##        _1900 = FloorSpace(1900, construction_history['CA'][1900], 'CA')
##        pprint.pprint(_1900.remaining_floor_space_by_year)
##        _1900.age_n_years(78)
##        print_single_floor_space_object(_1900)

main()
#cProfile.run('main()')


end_time = datetime.now()
print("Duration:", end_time - start_time)
