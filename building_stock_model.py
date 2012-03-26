'''
Written for Python 3.2.2
By Andrew Sturges; LBNL
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


#Duplicative sample code to show the steps of the more compact version below
'''
#Start in 1975, establish a five-year building stock,
#and then age everything up to the year 2010: 

_1975 = Floor_Space(1975, construction_history['1975'], 'USA')
_1976 = Floor_Space(1976, construction_history['1976'], 'USA')
_1977 = Floor_Space(1977, construction_history['1977'], 'USA')
_1978 = Floor_Space(1978, construction_history['1978'], 'USA')
_1979 = Floor_Space(1979, construction_history['1979'], 'USA')
_1980 = Floor_Space(1980, construction_history['1980'], 'USA')

_1975.age_n_years(35)
_1976.age_n_years(34)
_1977.age_n_years(33)
_1978.age_n_years(32)
_1979.age_n_years(31)
_1980.age_n_years(30)

code_year = 2010
#Now get the total square footage of buildings under, e.g., the 1997 building codes:
print("1975 stock renovated under",code_year,"code:", format(int(_1975.remaining_floor_space_by_year[code_year]), ',d'), "square feet.")
print("1976 stock renovated under",code_year,"code:", format(int(_1976.remaining_floor_space_by_year[code_year]), ',d'), "square feet.")
print("1977 stock renovated under",code_year,"code:", format(int(_1977.remaining_floor_space_by_year[code_year]), ',d'), "square feet.")
print("1978 stock renovated under",code_year,"code:", format(int(_1978.remaining_floor_space_by_year[code_year]), ',d'), "square feet.")
print("1979 stock renovated under",code_year,"code:", format(int(_1979.remaining_floor_space_by_year[code_year]), ',d'), "square feet.")
print("1980 stock renovated under",code_year,"code:", format(int(_1980.remaining_floor_space_by_year[code_year]), ',d'), "square feet.")
total = (_1975.remaining_floor_space_by_year[code_year]
    +_1976.remaining_floor_space_by_year[code_year]
    +_1977.remaining_floor_space_by_year[code_year]
    +_1978.remaining_floor_space_by_year[code_year]
    +_1979.remaining_floor_space_by_year[code_year]
    +_1980.remaining_floor_space_by_year[code_year])
total = format(int(total), ',d')
print("Total stock from 1975--1980 renovated under", code_year,"buidling codes:", total, "square feet.")

#now what's the applicable building code from that year?
building_code = code_compliance['USA'][code_year]
print(total, "square feet are under the",code_year,"building code which is", building_code)
'''

#Create a building stock and move it forward through time
'''This code is a more flexible and concise version
of what is layed out above.'''

def create_building_stock(start_build_year, end_build_year, construction_data): #assumes construction_data spans start and end years
    # mass create a building stock
    building_stock_objects = list()
    #todo: gotta loop through regions here too, given by construction_data
    for i in range(start_build_year, end_build_year + 1):
        building_stock_objects.append(Floor_Space(i, construction_data[str(i)], 'USA'))
    return building_stock_objects

def age_building_stock_to_year(building_stock_objects, model_end_year):
    #age a list of building_stock_objects to model_end_year
    for i in range(len(building_stock_objects)):
        start_year = building_stock_objects[i].current_year
        building_stock_objects[i].age_n_years(model_end_year - start_year)
    return building_stock_objects

def return_code_bins_in_current_year(building_stock_objects): #incorrectly assuming all objects will have same current year?
    #show a complete picture of all existing floor space bins
    #by year, as it exists in the current_year
    code_bins_in_current_year = dict()
    for i in range(len(building_stock_objects)):
        start_year = building_stock_objects[i].year_of_construction
        end_year = building_stock_objects[i].current_year
        for j in range(start_year,end_year+1):
            # += is forbidden in loops, so we use an if statement
            if j in code_bins_in_current_year:
                code_bins_in_current_year[j] = code_bins_in_current_year[j] + building_stock_objects[i].remaining_floor_space_by_year[j]
            else:
                code_bins_in_current_year[j] = building_stock_objects[i].remaining_floor_space_by_year[j]
    return code_bins_in_current_year

def show_building_codes_in_current_year(code_bins_in_current_year):
    for year in code_bins_in_current_year.keys():
        if year in code_compliance['USA']:
            code = code_key[code_compliance['USA'][year]]
        else:
            code = "none specified"
        print(
            "Year:",
            year,
            "Square feet:",
            format(int(code_bins_in_current_year[year]),',d'),
            "Building code:",
            code)

the_eighties = create_building_stock(1980, 1980, construction_history)
age_building_stock_to_year(the_eighties, 2010)
code_bins = return_code_bins_in_current_year(the_eighties) #fun future project: animate this through time
show_building_codes_in_current_year(code_bins)

#animate the year 1975:
_1975 = create_building_stock(1975,1975, construction_history)
animation_data_by_year = dict()
for year in range(1975, 2011):
    animation_data_by_year[year] = return_code_bins_in_current_year(age_building_stock_to_year(_1975, year))

#pprint.pprint(animation_data_by_year)
#create a csv file to graph this in Excel
#want a row of 1975 values from each stock object, so loop through all the stock objects and grab 1975:

with open('animation.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row_year in range(1975,2011):
        row = list()
        for object_year in range(1975,2011):
            if row_year in animation_data_by_year[object_year]:
                row.append(animation_data_by_year[object_year][row_year])
            else:
                row.append(0) #this is so ugly please fix this later
        writer.writerow(row)


'''Create a dictionary of total existing floor space by year,
without respect to renovations or building codes. Just show
how much existed during each year from each stock object.'''

'''
#Create a list of new stock objects:
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



#test that aging in separate consecutive periods
#has same effect as one longer period:
'''

_1980a = Floor_Space(1980, construction_history['1980'], 'USA')
_1980b = Floor_Space(1980, construction_history['1980'], 'USA')

_1980a.age_n_years(10)
_1980b.age_n_years(3)
_1980b.age_n_years(1)
_1980b.age_n_years(6)
_1980a.identify()
_1980b.identify()

print(_1980a.current_year == _1980b.current_year)
print(_1980a.remaining_floor_space_by_year[1987] == _1980b.remaining_floor_space_by_year[1987])
print(_1980a.stock_age == _1980b.stock_age)
'''
