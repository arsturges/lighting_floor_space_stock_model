import csv
class LoadInputs():
    def __init__(self):
        # Define to paths to inputs:
        starts = 'csv_inputs/construction_history_by_state.csv'
        state_cendiv_correspondance = 'csv_inputs/states_cendivs.csv'
        cendiv_NEMS_percentages = 'csv_inputs/cendivs_NEMS_percentages.csv'
        floor_space_coverage_by_code = 'csv_inputs/floor_space_under_building_lighting_automatic_shutoff.csv'
        scenario = 'csv_inputs/state_energy_code_compliance_no_increase.csv'
        #scenario = 'csv_inputs/state_energy_code_compliance_federal_standard_2007_by_2015.csv'
        state_energy_code_key = 'csv_inputs/state_energy_code_key_SIMPLIFIED.csv'

        # Create some csv.reader objects:
        code_key_reader = csv.reader(open(state_energy_code_key))
        states_cendivs_reader = csv.reader(open(state_cendiv_correspondance))

        # Parse paths and reader objects into usable dictionaries:
        self.code_key = self.convert_csv_to_dictionary_without_header(code_key_reader)
        self.states_cendivs = self.convert_csv_to_dictionary_without_header(states_cendivs_reader)
        self.construction_history_by_state = self.convert_csv_to_dictionary_of_dictionaries(starts)
        self.code_compliance = self.convert_csv_to_dictionary_of_dictionaries(scenario)
        self.floor_space_coverage_by_code = self.convert_csv_to_dictionary_of_dictionaries(floor_space_coverage_by_code)
        self.cendiv_NEMS = self.import_3_column_data(cendiv_NEMS_percentages)
        self.construction_history= self.add_NEMS_building_types_to_construction_history(
            self.construction_history_by_state,
            self.states_cendivs,
            self.cendiv_NEMS)

    def convert_csv_to_dictionary_without_header(self, reader_object):
        dictionary = dict()
        for row_number, row in enumerate(reader_object):
            if row_number == 0: continue # Skip header
            key = self.return_in_native_format(row[0])
            value = row[1]
            dictionary[key] = value
        return dictionary

    def convert_csv_to_dictionary_of_dictionaries(self, csv_file):
        '''We want a function that will import a csv file that is known to be
        in the following format: column 1 is a list of "primary keys" (e.g.
        state), and row 1 is a list of "secondary keys" (e.g. year), and their
        intersection is the value we want to reference. Basically, a common data
        table. There should be nothing (of value) in cell(0,0). The function
        will import this file, and create a dictionary that can be accessed as
        follows: new_dictionary['primary_key']['secondary_key'] = value.

        In other words, we want a dictionary of dictionaries; access it like
        this: dictionary_namy['MA'][1986]
        It returns the value of what was in the csv file for that year/state.
        '''

        reader = csv.reader(open(csv_file))#, newline='')) # A 'reader' object
        reader_rows = list(reader)
        # A list object; the number of rows is the same as rows in the csv file.
        
        secondary_keys = list()
        # We assume secondary_keys (e.g. years) in the header; we skip 0, which is cell(0,0)
        for secondary_key in range(1, len(reader_rows[0])):
            secondary_keys.append(int(reader_rows[0][secondary_key])) # Get rid of this int call

        primary_keys = list()
        primary_key_dictionaries = list() # A list of primary key dictionaries (one level deep only)
        for primary_key in range(1, len(reader_rows)): # Skip the header
            key_name = self.return_in_native_format(reader_rows[primary_key][0])
            primary_keys.append(key_name)
            primary_key_values = [] # A list of values corresponding to available years
            for secondary_key in range(1, len(reader_rows[0])): # Skip the header
                value_to_store = self.return_in_native_format(reader_rows[primary_key][secondary_key])
                primary_key_values.append(value_to_store)
            primary_key_dictionary = dict(zip(secondary_keys, primary_key_values))
            primary_key_dictionaries.append(primary_key_dictionary)
        dictionary_of_dictionaries = dict(zip(primary_keys, primary_key_dictionaries))
        return dictionary_of_dictionaries

    def return_in_native_format(self, string_object):
        '''This is a result of my csv inputs all coming in as strings. Maybe
        there's a way to parse them in their native formats to begin with,
        instead of dealing with it here.

        We want to get integers back to being integers, floats back to floats,
        leave strings as strings, etc. And be careful not to convert floats to
        integers. Right now this does little of that, but remains as a framework
        for future implementation.'''

        try:
            string_object_as_new_type = int(string_object) #Try for integer...
        except:
            string_object_as_new_type = string_object # ...otherwise take it as-is.
        return string_object_as_new_type

    def import_3_column_data(self, csv_file):
        ''' Import the NEMS floor space percentages. Will be a dict object like
        this: cendiv_NEMS[cendiv][NEMS_building_type]. This will return the
        percentage of all floor space in that cendiv that is comprised of that
        building type.'''
        cendiv_NEMS_csv = list(csv.reader(open(csv_file))) # A list of rows
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
        self,
        construction_history_by_state,
        states_cendivs,
        cendiv_NEMS):
        ''' The following code takes construction_history_by_state and breaks
        each state's floor space into its constituent NEMS building types as
        defined in cendiv_NEMS.
        Original: construction_history_by_state['CA'] = total for all of CA
        Modified: construction_history['CA'][78] = total for just office space in CA.'''
        construction_history = dict()
        for state in construction_history_by_state:
            construction_history[state] = dict()
            for year in construction_history_by_state[state]:
                total_state_year_floor_space = float(construction_history_by_state[state][year])
                construction_history[state][year] = dict()
                cendiv = int(states_cendivs[state])
                for NEMS_building_type in [1,2,3,4,5,6,9,10,11,78]: 
                    #better to pull this from the csv
                    percentage = cendiv_NEMS[cendiv][NEMS_building_type]
                    floor_space = total_state_year_floor_space * percentage
                    construction_history[state][year][NEMS_building_type] = floor_space
        return construction_history
##inputs = LoadInputs()
##import pprint
##pprint.pprint(inputs.code_compliance['CA'])
##print("###########\n\n\n########")
##print(inputs.code_key)
##print("###########\n\n\n########")
##pprint.pprint(inputs.floor_space_coverage_by_code)
