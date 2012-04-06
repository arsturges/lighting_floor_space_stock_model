import csv
from floor_space import *

def convert_csv_to_dictionary_of_dictionaries(csv_file):
    '''We want a function that will import a csv file that
    is known to be in the following format: column 1 is a
    list of states, and row 1 is a list of years. There should
    be nothing (of value) in cell(0,0). The function will import this
    file, and create a dictionary that can be accessed as
    follows: new_dictionary['state'][year]

    We want a dictionary of dictionaries; the first key
    will be the state abbreviation, and the second key
    will be the year, so we can access it like this:
    dictionary_namy['MA'][1986]
    It will return the value of whatever was in the
    csv file for that year/state.
    '''

    reader = csv.reader(open(csv_file, newline='')) # a 'reader' object
    rows = list(reader)
    #a 'list' object;
    #the number of rows is the same as rows in the csv file, 
    #probably the 51 states (incl. DC) and a header.
    
    years=list()
    for year in range(1, len(rows[0])): #we assume years in the header; we skip 0, which is cell(0,0
        years.append(int(rows[0][year]))

    states=list()
    state_dictionaries = list() #a list of state dictionaries
    for state in range(1, len(rows)): #skip the header
        states.append(rows[state][0])
        state_values = [] # a list of values corresponding to available years
        for year in range(1, len(rows[0])): #skip the header
            state_values.append(rows[state][year]) #put in some int/float/str logic
        state_dictionary = dict(zip(years, state_values))
        state_dictionaries.append(state_dictionary)
    final_product = dict(zip(states, state_dictionaries))
    return final_product

def import_3_column_data(csv_file):
    #import the NEMS floor space percentages.
    #Will be a dict object like this: cendiv_NEMS[cendiv][NEMS_building_type]
    #this will return the percentage of all floor space in that cendiv
    #that is comprised of that building type.
    cendiv_NEMS_csv = list(csv.reader(open(csv_file))) #a list of rows
    cendiv_NEMS = dict()
    for row_number in range(1, len(cendiv_NEMS_csv)):
        cendiv = int(cendiv_NEMS_csv[row_number][0])
        NEMS_building_type = int(cendiv_NEMS_csv[row_number][1])
        percentage = float(cendiv_NEMS_csv[row_number][2])
        if cendiv in cendiv_NEMS:
            cendiv_NEMS[cendiv][NEMS_building_type] = percentage
        else:
            cendiv_NEMS[cendiv] = dict()
            cendiv_NEMS[cendiv][NEMS_building_type] = percentage
    return cendiv_NEMS

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

def test_the_model():
    #test that aging in separate consecutive periods
    #has same effect as one longer period:
    construction_history = dict(csv.reader(open('construction_history.csv')))

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

def animate_1975():
    #animate the year 1975:
    _1975 = create_building_stock(1975,1975, construction_history)
    animation_data_by_year = dict()
    for year in range(1975, 2011):
        animation_data_by_year[year] = return_code_bins_in_current_year(age_building_stock_to_year(_1975, year))

    #create a csv file to graph this in Excel
    #want a row of 1975 values from each stock object,
    #so loop through all the stock objects and grab 1975:

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

def show_existing_stock():
    '''Create a dictionary of total existing floor space by year,
    without respect to renovations or building codes. Just show
    how much existed during each year from each stock object.
    This will basically show demolition rate only; renovation
    will have no effect. This is an old method that doesn't
    use the new convenience methods 'create_building_stock(); etc.'''

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
    pprint.pprint(histories) # graph this output in Excel

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

def show_building_codes_in_current_year(code_bins_in_current_year, code_compliance):
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


