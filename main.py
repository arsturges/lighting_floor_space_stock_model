'''
main.py
Written for Python 3.2.2
'''

from csv_functions import *
from floor_space import *
from helper_functions import *
import pprint
import csv

#set up some data objects:
scenario = 'state_energy_code_compliance_no_increase.csv'
code_compliance = convert_csv_to_dictionary_of_dictionaries(scenario)

#this form works because we know it has only 2 columns
#code_key['13'] == "ASHRAE 2004"
code_key = dict(csv.reader(open('state_energy_code_key.csv')))

starts = 'construction_history_by_state.csv'
construction_history_by_state = convert_csv_to_dictionary_of_dictionaries(starts)

#states_cendivs['AZ'] == '8'.
states_cendivs = dict(csv.reader(open('states_cendivs.csv'))) 

cendiv_NEMS = import_3_column_data('cendivs_NEMS_percentages.csv')

construction_history = add_NEMS_building_types_to_construction_history(
    construction_history_by_state,
    states_cendivs,
    cendiv_NEMS)

#Run the model using convenience methods from helper_functions.py:
the_eighties = create_building_stock(1980, 1980, construction_history)
age_building_stock_to_year(the_eighties, 1981)
code_bins = return_code_bins_in_current_year(the_eighties)
show_building_codes_in_current_year(code_bins, code_compliance)
