'''
main.py
Written for Python 3.2.2
'''
from datetime import datetime
start_time = datetime.now()

from csv_functions import *
from floor_space import *
from helper_functions import *
import pprint
import csv

#define the inputs:
starts = 'csv_inputs/construction_history_by_state.csv'
state_cendiv_correspondance = 'csv_inputs/states_cendivs.csv'
cendiv_NEMS_percentages = 'csv_inputs/cendivs_NEMS_percentages.csv'
floor_space_coverage_by_code = 'csv_inputs/floor_space_under_building_lighting_automatic_shutoff.csv'


construction_history_by_state = convert_csv_to_dictionary_of_dictionaries(starts)
states_cendivs = dict(csv.reader(open(state_cendiv_correspondance))) #states_cendivs['AZ'] == '8'.
cendiv_NEMS = import_3_column_data(cendiv_NEMS_percentages)
construction_history = add_NEMS_building_types_to_construction_history(
    construction_history_by_state,
    states_cendivs,
    cendiv_NEMS)
floor_space_coverage_by_code = convert_csv_to_dictionary_of_dictionaries(floor_space_coverage_by_code)

#Run the model using convenience methods from helper_functions.py:
the_eighties = create_building_stock(1975, 2015, construction_history)
age_building_stock_to_year(the_eighties, 2035)
code_bins = return_code_bins_in_current_year(the_eighties)
#show_building_codes_in_current_year(code_bins, code_compliance)

print_csv_database(code_bins, code_compliance, floor_space_coverage_by_code)



end_time = datetime.now()
print("Duration:", end_time - start_time)
