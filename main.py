'''
Written for Python 3.2.2
'''

from floor_space import *
from helper_functions import *
import pprint
import csv

#set up some data objects:
code_compliance = convert_csv_to_dictionary_of_dictionaries('state_energy_code_compliance_no_increase.csv')
construction_history_by_state = convert_csv_to_dictionary_of_dictionaries('construction_history_by_state.csv')
code_key = dict(csv.reader(open('state_energy_code_key.csv')))#works because we know it has only two columns
states_cendivs = dict(csv.reader(open('states_cendivs.csv'))) #states_cendivs['AZ'] returns '8'.
cendiv_NEMS = import_3_column_data('cendivs_NEMS_percentages.csv')
construction_history = add_NEMS_building_types_to_construction_history(
    construction_history_by_state,
    states_cendivs,
    cendiv_NEMS)

##_1980 = Floor_Space(1980, construction_history['AZ'][1980], 'AZ')
##_1980.age_n_years(10)
##_1980.identify()
#Run the model using the convenience methods above:
the_eighties = create_building_stock(1980, 1980, construction_history)
age_building_stock_to_year(the_eighties, 1981)
code_bins = return_code_bins_in_current_year(the_eighties)
show_building_codes_in_current_year(code_bins, code_compliance)
