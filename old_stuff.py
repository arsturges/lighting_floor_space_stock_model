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
