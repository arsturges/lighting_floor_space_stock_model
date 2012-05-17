from floor_space import *
from csv_functions import *

#TODO: put all the inputs in main.py

#set up some data objects:
scenario = 'csv_inputs/state_energy_code_compliance_no_increase.csv'
#scenario = 'csv_inputs/state_energy_code_compliance_federal_standard_2007_by_2015.csv'
code_compliance = convert_csv_to_dictionary_of_dictionaries(scenario)

#this form works because we know it has only 2 columns
#code_key['13'] == "ASHRAE 2004"
state_energy_code_key = 'csv_inputs/state_energy_code_key.csv'
code_key = dict(csv.reader(open(state_energy_code_key))) #TODO: make this output int and float instead of str

def add_NEMS_building_types_to_construction_history(
    construction_history_by_state,
    states_cendivs,
    cendiv_NEMS):
    #the following code takes construction_history_by_state
    # and adds the NEMS building types to it.
    construction_history = dict()
    for state in construction_history_by_state:
        construction_history[state] = dict()
        for year in construction_history_by_state[state]:
            total_state_year_floor_space = float(construction_history_by_state[state][year])
            construction_history[state][year] = dict()
            cendiv = int(states_cendivs[state])
            for NEMS_building_type in [1,2,3,4,5,6,9,10,11,78]: #better to pull this from the csv
                percentage = cendiv_NEMS[cendiv][NEMS_building_type]
                floor_space = total_state_year_floor_space * percentage
                construction_history[state][year][NEMS_building_type] = floor_space
    return construction_history

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

