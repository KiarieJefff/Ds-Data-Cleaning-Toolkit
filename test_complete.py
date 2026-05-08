import pandas as pd
from data_cleaner import DataCleaner

# Test the complete workflow again
cleaner = DataCleaner()

# Clean mixed data types
user_data = {
    'name': '  John DOE  ',
    'email': 'JOHN@EXAMPLE.COM',
    'age': '25 years',
    'phone': '(555) 123-4567 ext. 123',
    'salary': '$75,000',
    'join_date': '01/15/2023'
}

# Clean each field
cleaned_data = {
    'name': cleaner.clean_string(user_data['name'], strip=True, lower=False),
    'email': cleaner.clean_email(user_data['email']),
    'age': cleaner.clean_numeric(user_data['age']),
    'phone': cleaner.clean_phone(user_data['phone']),
    'salary': cleaner.clean_numeric(user_data['salary'], remove_units=True),
    'join_date': cleaner.clean_date(user_data['join_date'])
}

print('Cleaned user data:', cleaned_data)

# Working with DataFrames
df = pd.DataFrame({
    'name': ['Alice', '  Bob  ', 'Charlie', 'Alice', ''],
    'age': [25, None, '30 years', 25, 'unknown'],
    'salary': ['$50,000', '$60,000', None, '$50,000', '$0']
})

cleaned_df = cleaner.clean_dataframe(
    df,
    handle_missing='fill',
    remove_duplicates=True,
    strip_strings=True,
    convert_dates=False
)
print('\nCleaned DataFrame:')
print(cleaned_df)

# Test list cleaning
raw_list = ['apple', '  BANANA  ', '', 'CHERRY', 'apple', None, '  date  ']
cleaned_list = cleaner.clean_list(
    raw_list, 
    remove_duplicates=True, 
    remove_empty=True,
    remove_none=True,
    sort=True
)
print('\nCleaned list:', cleaned_list)
