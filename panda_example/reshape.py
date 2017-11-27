import pandas as pd

# Read the CSV
df = pd.read_csv('ACS_15_5YR_S2101/ACS_15_5YR_S2101_with_ann.csv')

# Drop two of the "ID" columns (could keep these if you want them)
df.drop(['GEO.id', 'GEO.display-label'], axis = 1, inplace = True)

# Rename the GEO.id2 to fips
df.rename(columns = {'GEO.id2': 'fips'}, inplace = True)

# Reshape the table, make it long
df = df.melt(id_vars = ['fips'])

# Do analysis, remove rows, make table wide again, etc...

# Write to CSV
df.to_csv('reshaped.csv', index = False)
