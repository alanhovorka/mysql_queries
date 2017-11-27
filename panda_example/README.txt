Reshaping tables

Reshaping a table from wide to long means converting a bunch of columns into two columns,
called key-value pairs. The "key" column is the name of the former columns and the 
"value" column has the values that were under each column.

You can do the opposite too, convert a long table to a wide table. Basically you're
converting two key-value columns into multiple columns.

Here are some examples of reshaping tables using Python and R.
- Python + Pandas: https://pandas.pydata.org/pandas-docs/stable/reshaping.html
- R + tidyverse: http://tidyr.tidyverse.org/articles/tidy-data.html
    - this article does a good job explaining data cleaning more generally

Files and folders...

simplified-example.xlsx
- Toy example of what I mean by "reshaping" a table wide-to-long

ACS_15_5YR_S2101/
- Demographics of veteran population by state
- Downloaded from American Factfinder
- Deleted the second header row

reshape.py
- Python script that reshapes the ACS table. Creates reshaped.csv

trim.py
- Python script that trims away some columns, renames things. Creates trimmed.csv
