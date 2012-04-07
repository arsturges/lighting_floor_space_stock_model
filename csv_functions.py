import csv

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
