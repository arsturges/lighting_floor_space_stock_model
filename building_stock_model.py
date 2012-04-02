'''
Written for Python 3.2.2
'''

from floor_space import *
from helper_functions import *
import pprint
import csv

#Create a building stock and move it forward through time
def create_building_stock(start_build_year, end_build_year, construction_data): #assumes construction_data spans start and end years
    # mass-create a building stock
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

def return_code_bins_in_current_year(building_stock_objects): #incorrectly assuming all objects will have same current year?
    #show a complete picture of all existing floor space bins
    #by state and by year, as it exists in the current_year
    #reference like this: code_bins_in_current_year["ID"][1992]
    code_bins_in_current_year = dict()
    for i in range(len(building_stock_objects)):
        state = building_stock_objects[i].region
        start_year = building_stock_objects[i].year_of_construction
        end_year = building_stock_objects[i].current_year
        for year in range(start_year,end_year+1):
            if state in code_bins_in_current_year:
                add_floor_space_to_bin(code_bins_in_current_year, state, year, building_stock_objects[i].remaining_floor_space_by_year[year])
            else:
                code_bins_in_current_year[state] = dict()
                code_bins_in_current_year[state] = add_floor_space_to_bin(code_bins_in_current_year, state, year, building_stock_objects[i].remaining_floor_space_by_year[year])
    return code_bins_in_current_year

def add_floor_space_to_bin(code_bins_in_current_year, state, year, floor_space):
    # += is forbidden in loops, so we use an if statement
    if year in code_bins_in_current_year[state]:
        code_bins_in_current_year[state][year] = code_bins_in_current_year[state][year] + floor_space
    else:
        code_bins_in_current_year[state][year] = floor_space
    return code_bins_in_current_year[state]

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
                format(int(code_bins_in_current_year[state][year]),',d'),
                "Building code:", code)
        
#set up some data objects:
code_compliance = convert_csv_to_dictionary_of_dictionaries('state_energy_code_compliance_no_increase.csv')
construction_history_by_state = convert_csv_to_dictionary_of_dictionaries('construction_history_by_state.csv')
code_key = dict(csv.reader(open('state_energy_code_key.csv')))#works because we know it has only two columns

#Run the model using the convenience methods above:
the_eighties = create_building_stock(1980, 1981, construction_history_by_state)
age_building_stock_to_year(the_eighties, 1982)
code_bins = return_code_bins_in_current_year(the_eighties)
show_building_codes_in_current_year(code_bins)
