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
