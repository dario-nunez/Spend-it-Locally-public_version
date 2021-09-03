"""CACI datasets.

Performs all necessary computations to transform the raw CACI dataset files (currently
in xlsx format) to a more workable csv file. Currently these steps are done manually.

Input datasets:
- WCC - CACI Paycheck Disposable Income - Feb2020.xlsx
- WCC - Population by Age and Gender - Feb2020.xlsx
- Westminster City Council - Westminster Acorn directory - February 2020.xlsx
- Westminster City Council - Westminster COICOP directory - February 2020.xlsx
- Westminster City Council - Westminster Paycheck directory - February 2020.xlsx
- Westminster City Council - Westminster PTAL directory - February 2020.xlsx
- Westminster City Council - Westminster StreetValue directory - February 2020.xlsx
- Westminster City Council - Westminster Wellbeing Acorn directory - February 2020.xlsx

Output datasets:
- WCC_Acorn_directory_Feb2020.csv
- WCC_CACI_Paycheck_Disposable_Income_Feb2020.csv
- WCC_COICOP_directory_Feb2020.csv
- WCC_Paycheck_directory_Feb2020.csv
- WCC_Population_by_Age_and_Gender_Feb2020.csv
- WCC_PTAL_directory_Feb2020.csv
- WCC_StreetValue_directory_Feb2020.csv
- WCC_Wellbeing_Acorn_directory_Feb2020.csv
"""

#-------------------------------------------------------------------------------
# Manual data conversion from xlsx to csv using LibreOffice:
# 1. Open the data file in.
# 2. Go to the data sheet to export.
# 3. Export it as:
#   character set: Unicode (UTF-8).
#   field delimeter: ,.
#   string delimeter: ".
#   Save cell context as shown.
#   Quote all the text cells.
# 4. Open the exported file in a text editor.
# 5. Delete all the data that is not data or data table headers.
#
# * In the WCC_CACI_Paycheck_Disposable_Income_Feb2020 dataset, append parent headers 
# to child column names.
#-------------------------------------------------------------------------------
