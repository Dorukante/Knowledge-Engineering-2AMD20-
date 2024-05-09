import pandas as pd

def read_excell(file, sheet, row_end):
    # Read the Excel file
    df = pd.read_excel(file, sheet_name=sheet)

    # Limit the DataFrame to the specified number of rows
    df = df.iloc[:row_end]

    return df

def group_foods(df):
    food_groups = {}
    current_group = None
    for index, row in df.iterrows():
        if (isinstance(row['Food group'], str) and 
            any(char in row['Food group'] for char in ['(', ')'])):
            current_group = row['Food group']
            food_groups[current_group] = {}
        elif current_group:
            if isinstance(row['Food group'], str) and row['Food group'] not in ['Total population', 'Children', 'Adults']:
                food_groups[current_group][row['Food group']] = row.drop('Food group').to_dict()
    return food_groups

def group_nutrients(df):
    nutrient_groups = {}
    current_group = None
    for index, row in df.iterrows():
        if (isinstance(row['Nutrient group'], str) and 
            any(char in row['Nutrient group'] for char in ['(', ')'])):
            current_group = row['Nutrient group']
            nutrient_groups[current_group] = {}
        elif current_group:
            if isinstance(row['Nutrient group'], str) and row['Nutrient group'] not in ['Total population', 'Children', 'Adults']:
                nutrient_groups[current_group][row['Nutrient group']] = row.drop('Nutrient group').to_dict()
    return nutrient_groups

# Average daily intake of food by food source and demographic characteristics 2007 - 2010
daily_intake_2007_2010 = group_foods(read_excell("archived_food_table1(2007-10).xls", "Daily intake by food source", 56))

# Food density by food source and demographic characteristics 2007 - 2010
food_density_2007_2010 = group_foods(read_excell("archived_food_table2(2007-10).xls", "Food density", 56))

def benchmark_calory_group(df):
    # Convert DataFrame to dictionary
    food_groups = {}
    for index, row in df.iterrows():
        food_group = row["Food group"]
        food_groups[food_group] = dict(row.iloc[1:])

    return food_groups

# Benchmark food density recommended food intake per 1000 calorie intake 2007 - 2010
calory_intake_2007_2010 = benchmark_calory_group(read_excell("archived_food_table3(2007-10).xls", "Benchmark food density", 11))

# Average daily intake of nutrients by food source and demographic characteristics, 2007-10
daily_nutrient_intake_2007_2010 = group_nutrients(read_excell("archived_nutrient_table1(2007-10).xls", "Daily intake", 32))

# Nutrient density by food source and demographic characteristics, 2007-10
nutrient_density_2007_2010 = group_nutrients(read_excell("archived_nutrient_table2(2007-10).xls", "Nutrient density", 28))

# Average daily intake of food by food source and demographic characteristics 2015 - 2016
daily_intake_2015_2016 = group_foods(read_excell("food_table1.xlsx", "2015 2016", 56))

# Average daily intake of food by food source and demographic characteristics 2017 - 2018
daily_intake_2017_2018 = group_foods(read_excell("food_table1.xlsx", "2017 2018", 56))

# Food density by food source and demographic characteristics 2015 - 2016
food_density_2015_2016 = group_foods(read_excell("food_table1.xlsx", "2015 2016", 56))

# Food density by food source and demographic characteristics 2017 - 2018
food_density_2017_2018 = group_foods(read_excell("food_table2.xlsx", "2017 2018", 56))

# Benchmark food density recommended food intake per 1000 calorie intake 2015 - 2016 & 2017-2018
calory_intake_2015_2018 = benchmark_calory_group(read_excell("food_table3.xlsx", "benchmark out", 10))

# Average daily intake of nutrients by food source and demographic characteristics, 2015-2016
daily_nutrient_intake_2015_2016 = group_nutrients(read_excell("nutrient_table1.xlsx", "2015 2016", 32))

# Average daily intake of nutrients by food source and demographic characteristics, 2017-2018
daily_nutrient_intake_2017_2018 = group_nutrients(read_excell("nutrient_table1.xlsx", "2017 2018", 32))

# Nutrient density by food source and demographic characteristics, 2015-2016
nutrient_density_2015_2016 = group_nutrients(read_excell("nutrient_table2.xlsx", "2015 2016", 28))

# Nutrient density by food source and demographic characteristics, 2017-2018
nutrient_density_2017_2018 = group_nutrients(read_excell("nutrient_table2.xlsx", "2017 2018", 28))
