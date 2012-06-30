import csv
class LoadInputs():
    def __init__(self):
        # Get raw CSV data:
        starts = 'csv_inputs/construction_history_by_state_CA_ONLY.csv'
        state_cendiv_correspondance = 'csv_inputs/states_cendivs.csv'
        cendiv_NEMS_percentages = 'csv_inputs/cendivs_NEMS_fake_percentages.csv'
        floor_space_coverage_by_code = 'csv_inputs/floor_space_under_building_lighting_automatic_shutoff.csv'
        scenario = 'csv_inputs/state_energy_code_compliance_no_increase.csv'
        #scenario = 'csv_inputs/state_energy_code_compliance_federal_standard_2007_by_2015.csv'
        state_energy_code_key = 'csv_inputs/state_energy_code_key.csv'

        # Intermediate steps to convert the inputs to usable arrays and dictionaries
        # TODO: make this output int and float instead of str
        self.states_cendivs  = dict(csv.reader(open(state_cendiv_correspondance))) # states_cendivs['AZ'] == '8'.
        code_key        = dict(csv.reader(open(state_energy_code_key))) #code_key['13'] == "ASHRAE 2004"
        self.construction_history_by_state  = self.convert_csv_to_dictionary_of_dictionaries(starts)
        self.code_compliance                = self.convert_csv_to_dictionary_of_dictionaries(scenario)
        self.floor_space_coverage_by_code   = self.convert_csv_to_dictionary_of_dictionaries(floor_space_coverage_by_code)
        self.cendiv_NEMS                    = self.import_3_column_data(cendiv_NEMS_percentages)
        self.construction_history           = self.add_NEMS_building_types_to_construction_history(
            self.construction_history_by_state,
            self.states_cendivs,
            self.cendiv_NEMS)

    def convert_csv_to_dictionary_of_dictionaries(self, csv_file):
        '''We want a function that will import a csv file that
        is known to be in the following format: column 1 is a
        list of states, and row 1 is a list of years. There should
        be nothing (of value) in cell(0,0). The function will import this
        file, and create a dictionary that can be accessed as
        follows: new_dictionary['state'][year]

        In other words, we want a dictionary of dictionaries; the first key
        will be the state abbreviation, and the second key
        will be the year, so we can access it like this:
        dictionary_namy['MA'][1986]
        It will return the value of whatever was in the
        csv file for that year/state.
        '''

        reader = csv.reader(open(csv_file, newline='')) # A 'reader' object
        rows = list(reader)
        # A 'list' object; the number of rows is the same as rows in the csv file,
        # probably the 51 states (incl. DC) and a header.
        
        years=list()
        for year in range(1, len(rows[0])): # We assume years in the header; we skip 0, which is cell(0,0)
            years.append(int(rows[0][year]))

        states=list()
        state_dictionaries = list() # A list of state dictionaries
        for state in range(1, len(rows)): # Skip the header
            states.append(rows[state][0])
            state_values = [] # A list of values corresponding to available years
            for year in range(1, len(rows[0])): # Skip the header
                state_values.append(rows[state][year]) # TODO: put in some int/float/str logic
            state_dictionary = dict(zip(years, state_values))
            state_dictionaries.append(state_dictionary)
        final_product = dict(zip(states, state_dictionaries))
        return final_product

    def import_3_column_data(self, csv_file):
        # Import the NEMS floor space percentages.
        # Will be a dict object like this: cendiv_NEMS[cendiv][NEMS_building_type]
        # This will return the percentage of all floor space in that cendiv
        # that is comprised of that building type.
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
        # The following code takes construction_history_by_state
        # and breaks each state's floor space into its constituent
        # NEMS building types as defined in cendiv_NEMS.
        # Original: construction_history_by_state['CA'] = total for all of CA
        # Modified: construction_history['CA'][78] = total for just office space in CA
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
