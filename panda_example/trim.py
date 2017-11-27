import pandas as pd

# Read the CSV
df = pd.read_csv('ACS_15_5YR_S2101/ACS_15_5YR_S2101_with_ann.csv')

# Drop two of the "ID" columns (could keep these if you want them)
df.drop(['GEO.id', 'GEO.display-label'], axis = 1, inplace = True)

# Rename the columns we want to keep
renamed_columns = {
    'GEO.id2': 'fips',
    'HC01_EST_VC01': 'total',
    'HC03_EST_VC01': 'veterans',
    'HC04_EST_VC01': 'pct_veterans',
}
df.rename(columns = renamed_columns, inplace = True)

df = df.loc[:, ('fips', 'total', 'veterans', 'pct_veterans')]

# # Write to CSV
df.to_csv('trimmed.csv', index = False)
