import pandas as pd

# axulary method to read the excell files and returns a dataframe, up to desired rows
def food_intake(xls, row_end):

    data = pd.read_excel(xls)

    return data.iloc[0:row_end]
 

# Average daily intake of food by food source and demographic characteristics 2007 - 2010
daily_intake_2007_2010 = food_intake("archived_food_table1(2007-10).xls", 84)

# Food density by food source and demographic characteristics 2007 - 2010
food_density_2007_2010 = food_intake("archived_food_table2(2007-10).xls", 84)

# Benchmark food density recommended food intake per 1000 calorie intake 2007 - 2010
calory_intake_2007_2010 = food_intake("archived_food_table3(2007-10).xls", 11)

# Average daily intake of food by food source and demographic characteristics 2015 - 2016 & 2017 - 2018
daily_intake_2015_2018 = food_intake("food_table1.xlsx", 112)

# Food density by food source and demographic characteristics 2015 - 2016 & 2017 - 2018
food_density_2015_2018 = food_intake("food_table1.xlsx", 112)

# Benchmark food density recommended food intake per 1000 calorie intake 2015 - 2016 & 2017 - 2018
calory_intake_2015_2018 = food_intake("food_table3.xlsx", 10)

# since the dataframes daily intake 2015 2018, food density 2015 2018 have 2 different year values 
# (i.e 2015 - 2016 & 2017-2018), we will split them into 2 parts

# Split the DataFrame into two parts
def split(dataframe):

    # Calculate the index to split the columns
    split_index = (len(dataframe.columns) - 1) // 2  # Subtract 1 to exclude the first columns from splitting

    # Split the DataFrame into two parts
    df1 = dataframe[['Food group'] + list(dataframe.columns[1:split_index + 1])]
    df2 = dataframe[['Food group'] + list(dataframe.columns[split_index + 1:])]

    return df1,df2

# Average daily intake of food by food source and demographic characteristics 2015 - 2016 
daily_intake_2015_2016 = split(daily_intake_2015_2018)[0]
# Average daily intake of food by food source and demographic characteristics 2017 - 2018 
daily_intake_2017_2018 = split(daily_intake_2015_2018)[1]

# Food density by food source and demographic characteristics 2015 - 2016 
food_density_2015_2016 = split(food_density_2015_2018)[0]
# Food density by food source and demographic characteristics 2017 - 2018
food_density_2017_2018 = split(food_density_2015_2018)[1]

print(food_density_2015_2016, food_density_2017_2018)