from floor_space import *
from load_inputs import LoadInputs

inputs = LoadInputs()
def create_building_stock(start_build_year, end_build_year, construction_data):
    # Assumes construction_data spans start and end years.
    # Mass-create a building stock.
    building_stock_objects = list()
    for state in construction_data.keys():
        for year in range(start_build_year, end_build_year + 1):
            building_stock_objects.append(FloorSpace(
                year, 
                construction_data[str(state)][year], 
                str(state)))
    return building_stock_objects

def age_building_stock_to_year(building_stock_objects, year):
    # Age a list of building_stock_objects to year.
    for stock_object in building_stock_objects:
        start_year = stock_object.current_year
        years_to_age = year - start_year
        if years_to_age > 0:
            stock_object.age_n_years(years_to_age)
    return building_stock_objects

def sum_bin_years(stock_objects):
    """
    Combine all individual FloorSpace objects into one.
    Show a complete picture of all existing floor space bins by state, year,
    and building type, as it exists in the 'current_year'.
    bin_years_sum['CA'][1950][78] = 2467.937 (floor space from all years having a 1950 bin)
    """
    bin_years_sum = dict()
    for stock_object in stock_objects:
        state = stock_object.region
        bin_years = stock_object.remaining_floor_space_by_year.keys()
        if not state in bin_years_sum:
            bin_years_sum[state] = dict()
        for bin_year in bin_years:
            if not bin_year in bin_years_sum[state]:
                bin_years_sum[state][bin_year] = dict()
            for building_type in [1,2,3,4,5,6,9,10,11,78]:
                if not building_type in bin_years_sum[state][bin_year]:
                    bin_years_sum[state][bin_year][building_type] = 0
                bin_years_sum[state][bin_year][building_type] += \
                    stock_object.remaining_floor_space_by_year[bin_year][building_type]
    return bin_years_sum

def print_single_floor_space_object(floor_space_object):
    current_year = floor_space_object.current_year
    state = floor_space_object.region
    for bin_year in floor_space_object.remaining_floor_space_by_year.keys():
        for building_type in [1,2,3,4,5,6,9,10,11,78]:
            total_floor_space = \
                floor_space_object.remaining_floor_space_by_year[bin_year][building_type]                
            writer.writerow([current_year,state,bin_year,building_type,"NA","NA","NA",total_floor_space])

def return_code_number_and_title(year, state):
    code_compliance = inputs.code_compliance
    code_key = inputs.code_key
    if year in code_compliance[state]:
        code_number = code_compliance[state][year] #these are strings; deal with it sometime
        code_title = code_key[int(code_number)]
    else:
        code_number = 99
        code_title = "Pre-2002 Building Code"
    return code_number, code_title

def return_coverage_multiplier(building_type, code_number):
    floor_space_coverage_by_code = inputs.floor_space_coverage_by_code
    if code_number in floor_space_coverage_by_code[building_type].keys():
        coverage_multiplier = float(floor_space_coverage_by_code[building_type][code_number])
    else:
        coverage_multiplier = 0
    return coverage_multiplier

def print_csv_database_rows(snapshot_year, start_year, bin_years_sum, writer):
    compliance_rate = 0.8
    for state in bin_years_sum.keys():
        for renovation_year in range(start_year, snapshot_year + 1):#bin_years_sum[state].keys():
            code_number, code_title = return_code_number_and_title(renovation_year, state)
            sum_across_all_b_types = 0 # b_types is building_types
            sum_covered = 0
            sum_uncovered = 0
            for b_type in [1,2,3,4,5,6,9,10,11,78]:
                floor_space = bin_years_sum[state][renovation_year][b_type] # 100 ft2
                coverage_multiplier = return_coverage_multiplier(b_type, code_number) # 0.75
                compliant_fs = floor_space * compliance_rate # 100 * 0.8 = 80 fts2
                non_compliant_fs = floor_space * (1-compliance_rate) # 100 * 0.2 = 20 ft2
                covered_compliant_fs = compliant_fs * coverage_multiplier # 80 * .75 = 60 ft2
                uncovered_compliant_fs = compliant_fs * (1-coverage_multiplier) # 80 * .25 = 20 ft2

                covered_floor_space = covered_compliant_fs # 60 ft2
                uncovered_floor_space = non_compliant_fs + uncovered_compliant_fs # 20 + 20 = 40 ft2

                sum_across_all_b_types += floor_space
                sum_covered += covered_floor_space
                sum_uncovered += uncovered_floor_space

            # Write out sum all of covered/uncovered fs across all building_types
            writer.writerow([
                snapshot_year,
                state,
                renovation_year,
                "Sum over all",
                code_number,
                code_title,
                "Covered",
                sum_covered])
            writer.writerow([
                snapshot_year,
                state,
                renovation_year,
                "Sum over all",
                code_number,
                code_title,
                "Uncovered",
                sum_uncovered])

if __name__ == "__main__":
    print(return_coverage_multiplier(78,16))
