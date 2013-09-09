'''
main.py
Written for Python 3.2.2
'''
from datetime import datetime
start_time = datetime.now()

from floor_space import FloorSpace
from load_inputs import LoadInputs
import helper_functions
import copy
import pprint
import csv


# Load the inputs:
inputs = LoadInputs()

# Create a single, complete building stock, age it one year at a time, 
# then sum and print those years.
start_year = 1900
end_year = 2030 
_1900_to_2030 = helper_functions.create_building_stock(
    start_year, 
    end_year, 
    copy.deepcopy(inputs.construction_history))

with open('2013-09-09_results_from_branch.csv', 'w') as f:#, newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['snapshot_year',
                     'state',
                     'floor_space_vintage',
                     'building_type',
                     'code_number',
                     'code_title',
                     'subspace',
                     'floor_space'])

    for snapshot_year in range(start_year, end_year + 1):
        if snapshot_year > start_year:
            print("Aging to year {}".format(snapshot_year))
            helper_functions.age_building_stock_to_year(_1900_to_2030, snapshot_year)
        code_bins = helper_functions.sum_bin_years(_1900_to_2030)
        helper_functions.print_csv_database_rows(snapshot_year, start_year, code_bins, writer)


end_time = datetime.now()
duration = end_time - start_time
print("Duration: {}".format(duration))
