# Data Cleaner Library

A comprehensive Python library for cleaning and preprocessing various data types and formats. Perfect for data science projects, ETL pipelines, and data wrangling tasks.

## Features

### Core Data Cleaning Functions
- **String Cleaning**: Remove whitespace, normalize case, handle special characters
- **Numeric Cleaning**: Parse numbers from text, remove currency symbols, handle units
- **Email Validation**: Validate and standardize email addresses
- **Phone Number Formatting**: Clean and format phone numbers internationally
- **Date Parsing**: Parse dates from multiple formats and standardize output
- **List Processing**: Remove duplicates, empty values, and sort lists
- **Dictionary Cleaning**: Clean keys and values in dictionaries
- **DataFrame Cleaning**: Comprehensive pandas DataFrame cleaning pipeline

### Advanced Features
- **Unicode Normalization**: Handle different Unicode character encodings
- **HTML Entity Decoding**: Convert HTML entities back to readable text
- **Outlier Detection**: Remove statistical outliers using IQR method
- **Text Standardization**: NLP preprocessing with stopword removal and stemming
- **Whitespace Management**: Advanced whitespace cleaning options

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd "Data Science/Data Cleaner"

# Install required dependencies
pip install pandas numpy
```

## Quick Start

```python
from data_cleaner import DataCleaner

# Initialize the cleaner
cleaner = DataCleaner()

# Clean a string
messy_text = "   Hello   World!   @#$   "
clean_text = cleaner.clean_string(messy_text, strip=True, remove_special_chars=True)
# Result: "Hello World"

# Clean numeric data with currency
salary = "$75,000 per year"
clean_salary = cleaner.clean_numeric(salary, remove_units=True)
# Result: 75000.0

# Clean and validate email
email = "  USER@EXAMPLE.COM  "
clean_email = cleaner.clean_email(email)
# Result: "user@example.com"

# Clean a DataFrame
import pandas as pd
df = pd.DataFrame({
    'name': ['Alice', '  Bob  ', 'Charlie'],
    'salary': ['$50,000', '$60,000', None],
    'email': ['alice@test.com', 'invalid-email', 'charlie@test.com']
})

cleaned_df = cleaner.clean_dataframe(
    df,
    handle_missing='fill',
    remove_duplicates=True,
    strip_strings=True
)
```

## Function Catalog

### String Operations
```python
# Basic string cleaning
cleaner.clean_string(text, strip=True, lower=False, remove_extra_spaces=True, 
                    remove_special_chars=False, replace_special_with_space=False)

# Advanced whitespace cleaning
cleaner.clean_whitespace(text, remove_leading_trailing=True, 
                        collapse_spaces=True, remove_newlines=True)

# Unicode normalization
cleaner.normalize_unicode(text, form='NFKC')

# HTML entity decoding
cleaner.decode_html_entities(text)

# Text standardization for NLP
cleaner.standardize_text(text, remove_stopwords=False, stem=False, 
                        custom_stopwords=None)
```

### Numeric Operations
```python
# Clean and convert numeric data
cleaner.clean_numeric(value, default=0.0, remove_units=True, 
                     allow_negative=True, max_value=None, min_value=None)

# Remove outliers using IQR method
cleaner.remove_outliers_iqr(data, multiplier=1.5)
```

### Contact Information
```python
# Email validation and cleaning
cleaner.clean_email(email)

# Phone number cleaning and formatting
cleaner.clean_phone(phone, format_as_international=True, remove_extension=True)
```

### Date Operations
```python
# Parse and format dates
cleaner.clean_date(date_string, formats=None, output_format='%Y-%m-%d', 
                  default=None)
```

### Data Structure Operations
```python
# Clean lists
cleaner.clean_list(data_list, remove_duplicates=True, remove_empty=True, 
                  remove_none=True, sort=False, unique_only=True, to_lowercase=False)

# Clean dictionaries
cleaner.clean_dict(data_dict, remove_empty_values=True, remove_none_values=True, 
                  strip_keys=True, convert_keys_to_lower=False)

# Clean DataFrames
cleaner.clean_dataframe(df, handle_missing='fill', fill_value=None, 
                       remove_duplicates=True, strip_strings=True, 
                       convert_dates=True)
```

## Data Type Patterns

The library includes built-in regex patterns for common data types:

- **Email**: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- **Phone**: `^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-1-9]{1,9}$`
- **URL**: `^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$`
- **SSN**: `^\d{3}-\d{2}-\d{4}$`
- **Credit Card**: `^\d{4}[-]?\d{4}[-]?\d{4}[-]?\d{4}$`
- **ZIP Code**: `^\d{5}(?:[-\s]\d{4})?$`
- **IP Address**: `^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$`

## Usage Examples

### Example 1: User Data Cleaning
```python
user_data = {
    'name': '  John DOE  ',
    'email': 'JOHN@EXAMPLE.COM',
    'age': '25 years',
    'phone': '(555) 123-4567 ext. 123',
    'salary': '$75,000',
    'join_date': '01/15/2023'
}

cleaned_data = {
    'name': cleaner.clean_string(user_data['name'], strip=True),
    'email': cleaner.clean_email(user_data['email']),
    'age': cleaner.clean_numeric(user_data['age']),
    'phone': cleaner.clean_phone(user_data['phone']),
    'salary': cleaner.clean_numeric(user_data['salary'], remove_units=True),
    'join_date': cleaner.clean_date(user_data['join_date'])
}
```

### Example 2: List Processing
```python
raw_list = ['apple', '  BANANA  ', '', 'CHERRY', 'apple', None, '  date  ']
cleaned_list = cleaner.clean_list(
    raw_list, 
    remove_duplicates=True, 
    remove_empty=True,
    remove_none=True,
    sort=True
)
# Result: ['BANANA', 'CHERRY', 'apple', 'date']

# With lowercase conversion
lowercase_list = cleaner.clean_list(
    raw_list, 
    remove_duplicates=True, 
    remove_empty=True,
    remove_none=True,
    sort=True,
    to_lowercase=True
)
# Result: ['apple', 'banana', 'cherry', 'date']
```

### Example 3: DataFrame Pipeline
```python
# Load messy data
df = pd.read_csv('messy_data.csv')

# Apply comprehensive cleaning
cleaned_df = cleaner.clean_dataframe(
    df,
    handle_missing='fill',      # Fill missing values
    remove_duplicates=True,     # Remove duplicate rows
    strip_strings=True,         # Strip whitespace from strings
    convert_dates=True          # Auto-convert date columns
)

# Additional custom cleaning
cleaned_df['email'] = cleaned_df['email'].apply(cleaner.clean_email)
cleaned_df['phone'] = cleaned_df['phone'].apply(cleaner.clean_phone)
```

## Convenience Functions

For quick access, the library provides standalone functions:

```python
from data_cleaner import clean_string, clean_numeric, clean_email, clean_phone, clean_date

# Direct usage without instantiating DataCleaner
clean_text = clean_string("  messy text  ", strip=True)
clean_num = clean_numeric("$1,234.56", remove_units=True)
clean_email = clean_email("USER@DOMAIN.COM")
```

## Dependencies

- **pandas**: For DataFrame operations
- **numpy**: For numerical operations
- **Python Standard Library**: 
  - `re` (regular expressions)
  - `datetime` (date handling)
  - `typing` (type hints)
  - `unicodedata` (Unicode normalization)
  - `html` (HTML entity decoding)

## Error Handling

The library is designed to be robust and handles errors gracefully:

- Invalid inputs return default values or `None`
- Type conversion errors are caught and handled
- Missing values are processed according to specified strategies
- All functions include comprehensive error handling

## Performance Considerations

- Functions are optimized for performance with large datasets
- Vectorized operations used where possible (especially with pandas)
- Memory-efficient implementations for list and dictionary operations
- Regex patterns are compiled and reused

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Include tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Examples and Notebooks

See the included Jupyter notebooks for detailed examples:
- `example.ipynb` - Basic usage examples
- `example_2.ipynb` - Advanced data cleaning scenarios

## Support

For issues, questions, or contributions, please use the project's issue tracker or contact the maintainers.
