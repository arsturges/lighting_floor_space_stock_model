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
construction_history = dict(csv.reader(open('construction_history.csv')))#TODO: make it read in integers as integers so int() isn't required

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

the_eighties = create_building_stock(1980, 1981, construction_history_by_state)
age_building_stock_to_year(the_eighties, 1982)
code_bins = return_code_bins_in_current_year(the_eighties)
show_building_codes_in_current_year(code_bins)

##_1980 = Floor_Space(1980, 100000000, "CA")
##_1980.age_n_years(30)
##_1980.identify()

###animate the year 1975:
##_1975 = create_building_stock(1975,1975, construction_history)
##animation_data_by_year = dict()
##for year in range(1975, 2011):
##    animation_data_by_year[year] = return_code_bins_in_current_year(age_building_stock_to_year(_1975, year))
##
###create a csv file to graph this in Excel
###want a row of 1975 values from each stock object, so loop through all the stock objects and grab 1975:
##
##with open('animation.csv', 'w', newline='') as f:
##    writer = csv.writer(f)
##    for row_year in range(1975,2011):
##        row = list()
##        for object_year in range(1975,2011):
##            if row_year in animation_data_by_year[object_year]:
##                row.append(animation_data_by_year[object_year][row_year])
##            else:
##                row.append(0) #this is so ugly please fix this later
##        writer.writerow(row)


'''Create a dictionary of total existing floor space by year,
without respect to renovations or building codes. Just show
how much existed during each year from each stock object.
This will basically show demolition rate only; renovation
will have no effect.'''

#Create a list of new stock objects:
'''
building_stock_objects = list()
for i in range(1975, 1981): #(1975 through 1980)
    building_stock_objects.append(Floor_Space(i, construction_history[str(i)], 'USA'))

#create a list of dictionaries to hold each stock object's history
histories = list()
for i in range(len(building_stock_objects)):
    histories.append(dict())

#age each one some number of years, and record total existing floor space at each year:
for i in range(len(building_stock_objects)):
    for j in range(25):
        start_year = building_stock_objects[i].year_of_construction
        end_year = building_stock_objects[i].current_year
        total_space_in_loop_year = 0
        for k in range(start_year, end_year+1):
            total_space_in_loop_year += building_stock_objects[i].remaining_floor_space_by_year[k]
        histories[i][j+start_year] = total_space_in_loop_year
        building_stock_objects[i].age_n_years(1)
pprint.pprint(histories) # graph this output in Excel'''


