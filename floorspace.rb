start_year = 1980

@floor_space = Hash.new
@floor_space[start_year] = 100000

def new_floor_space(year, new_construction_rate = 0.05 )
  @floor_space[year] * new_construction_rate 
end

def renovated_floor_space(year, renovation_rate=0.002)
  @floor_space[year] * renovation_rate
end

def retired_floor_space(year, retirement_rate = 0.03)
  @floor_space[year] * retirement_rate
end

def existing_floor_space(year)
  @floor_space[year-1] + new_floor_space(year-1) + renovated_floor_space(year-1) - retired_floor_space(year-1)
end


(start_year..1990).each do |year|
  if year == start_year
    @floor_space[year] = @floor_space[start_year]
  else
    @floor_space[year] = existing_floor_space(year)
  end
  puts year.to_s + " -- " + @floor_space[year].to_s
end


