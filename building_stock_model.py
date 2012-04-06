'''
Written for Python 3.2.2
'''

from floor_space import *
from helper_functions import *
import pprint
import csv

#Create a building stock and move it forward through time
def create_building_stock(start_build_year, end_build_year, construction_data):
    #assumes construction_data spans start and end years
    #mass-create a building stock
    building_stock_objects = list()
    for state in construction_data.keys():
        for i in range(start_build_year, end_build_year + 1):
            building_stock_objects.append(Floor_Space(i, construction_data[str(state)][i], str(state)))
    return building_stock_objects

def age_building_stock_to_year(building_stock_objects, year):
    #age a list of building_stock_objects to model_end_year
    for i in range(len(building_stock_objects)):
        start_year = building_stock_objects[i].current_year
        building_stock_objects[i].age_n_years(year - start_year)
    return building_stock_objects

def return_code_bins_in_current_year(stock_objects):
    #am I incorrectly assuming all objects will have same current year?
    #show a complete picture of all existing floor space bins
    #by state, year, and building type, as it exists in the current_year.
    #Reference it like this: code_bins_in_current_year["ID"][1992][5]
    code_bins_in_current_year = dict()
    for stock_object in stock_objects:
        state = stock_object.region
        start_year = stock_object.year_of_construction
        end_year = stock_object.current_year
        if not state in code_bins_in_current_year:
            code_bins_in_current_year[state] = dict()
        for year in range(start_year,end_year+1):
            if not year in code_bins_in_current_year[state]:
                code_bins_in_current_year[state][year] = dict()
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                if not building_type in code_bins_in_current_year[state][year]:
                    code_bins_in_current_year[state][year][building_type] = dict()
                    code_bins_in_current_year[state][year][building_type] = \
                        stock_object.remaining_floor_space_by_year[year][building_type]
                else:
                    existing = code_bins_in_current_year[state][year][building_type]
                    new_from_current_object = stock_object.remaining_floor_space_by_year[year][building_type]
                    code_bins_in_current_year[state][year][building_type] = existing + new_from_current_object
    return code_bins_in_current_year

def show_building_codes_in_current_year(code_bins_in_current_year):
    for state in code_bins_in_current_year.keys():
        for year in code_bins_in_current_year[state].keys():
            if year in code_compliance[state]:
                code = code_key[code_compliance[state][year]]
            else:
                code = "none specified"
            print(
                "State:", state,
                "Year:", year,
                "Square feet:",
                pprint.pprint(code_bins_in_current_year[state][year]),
                "Building code:", code)
        
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
#show_building_codes_in_current_year(code_bins)
