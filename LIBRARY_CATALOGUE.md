# Data Cleaner Library Catalogue

A comprehensive reference guide to all functions and methods available in the Data Cleaner library, organized by category and use case.

## Table of Contents

1. [Core Class Overview](#core-class-overview)
2. [String Processing Functions](#string-processing-functions)
3. [Numeric Processing Functions](#numeric-processing-functions)
4. [Contact Information Functions](#contact-information-functions)
5. [Date and Time Functions](#date-and-time-functions)
6. [Data Structure Functions](#data-structure-functions)
7. [Advanced Text Processing](#advanced-text-processing)
8. [Statistical Functions](#statistical-functions)
9. [Convenience Functions](#convenience-functions)
10. [Use Case Matrix](#use-case-matrix)

---

## Core Class Overview

### `DataCleaner` Class

The main class that provides all cleaning functionality. All methods are static, so you can use them without instantiating the class.

```python
from data_cleaner import DataCleaner

# Option 1: Use class methods directly
clean_text = DataCleaner.clean_string("  messy text  ")

# Option 2: Create instance (optional, for convenience)
cleaner = DataCleaner()
clean_text = cleaner.clean_string("  messy text  ")
```

---

## String Processing Functions

### `clean_string()`
**Purpose**: Basic string cleaning and normalization

```python
DataCleaner.clean_string(
    text: str,
    strip: bool = True,                    # Remove leading/trailing whitespace
    lower: bool = False,                   # Convert to lowercase
    remove_extra_spaces: bool = True,      # Replace multiple spaces with single
    remove_special_chars: bool = False,     # Remove all special characters
    replace_special_with_space: bool = False  # Replace special chars with space
) -> str
```

**Use Cases**:
- Cleaning user input from forms
- Normalizing text data for analysis
- Preparing strings for database storage

**Examples**:
```python
# Basic cleaning
DataCleaner.clean_string("   Hello   World!   ")
# Result: "Hello World!"

# Remove special characters
DataCleaner.clean_string("Hello@World#123", remove_special_chars=True)
# Result: "HelloWorld123"

# Lowercase and clean
DataCleaner.clean_string("  MIXED CASE  ", strip=True, lower=True)
# Result: "mixed case"
```

### `clean_whitespace()`
**Purpose**: Advanced whitespace management

```python
DataCleaner.clean_whitespace(
    text: str,
    remove_leading_trailing: bool = True,   # Strip whitespace from ends
    collapse_spaces: bool = True,           # Convert multiple spaces to single
    remove_newlines: bool = True            # Remove newline characters
) -> str
```

**Use Cases**:
- Cleaning text from multiple sources
- Preparing text for NLP processing
- Normalizing multiline text

### `normalize_unicode()`
**Purpose**: Handle Unicode character normalization

```python
DataCleaner.normalize_unicode(
    text: str,
    form: str = 'NFKC'  # NFC, NFKC, NFD, NFKD
) -> str
```

**Use Cases**:
- Processing text from different languages
- Handling accented characters
- Standardizing Unicode input

### `decode_html_entities()`
**Purpose**: Convert HTML entities to readable text

```python
DataCleaner.decode_html_entities(text: str) -> str
```

**Use Cases**:
- Processing web-scraped content
- Cleaning HTML-encoded text
- Handling XML/HTML data

---

## Numeric Processing Functions

### `clean_numeric()`
**Purpose**: Parse and clean numeric values from text

```python
DataCleaner.clean_numeric(
    value: Union[int, float, str],
    default: float = 0.0,               # Default value if conversion fails
    remove_units: bool = True,          # Remove unit suffixes
    allow_negative: bool = True,        # Allow negative numbers
    max_value: Optional[float] = None,  # Maximum value constraint
    min_value: Optional[float] = None   # Minimum value constraint
) -> float
```

**Use Cases**:
- Extracting numbers from financial data
- Converting mixed-format numeric input
- Cleaning sensor data with units

**Examples**:
```python
# Currency cleaning
DataCleaner.clean_numeric("$75,000", remove_units=True)
# Result: 75000.0

# With units
DataCleaner.clean_numeric("25kg", remove_units=True)
# Result: 25.0

# With constraints
DataCleaner.clean_numeric("150", max_value=100)
# Result: 100.0
```

### `remove_outliers_iqr()`
**Purpose**: Remove statistical outliers using IQR method

```python
DataCleaner.remove_outliers_iqr(
    data: Union[List[float], pd.Series, np.ndarray],
    multiplier: float = 1.5  # IQR multiplier
) -> List[float]
```

**Use Cases**:
- Data quality assessment
- Preparing data for machine learning
- Statistical analysis preprocessing

---

## Contact Information Functions

### `clean_email()`
**Purpose**: Validate and standardize email addresses

```python
DataCleaner.clean_email(email: str) -> Optional[str]
```

**Use Cases**:
- User registration validation
- Email list cleaning
- Contact data standardization

**Examples**:
```python
DataCleaner.clean_email("  USER@EXAMPLE.COM  ")
# Result: "user@example.com"

DataCleaner.clean_email("invalid-email")
# Result: None
```

### `clean_phone()`
**Purpose**: Clean and format phone numbers

```python
DataCleaner.clean_phone(
    phone: str,
    format_as_international: bool = True,  # Format with country code
    remove_extension: bool = True          # Remove phone extensions
) -> Optional[str]
```

**Use Cases**:
- Standardizing phone numbers from forms
- Preparing contact data for CRM systems
- International phone number formatting

---

## Date and Time Functions

### `clean_date()`
**Purpose**: Parse and standardize date strings

```python
DataCleaner.clean_date(
    date_string: str,
    formats: List[str] = None,            # Custom date formats to try
    output_format: str = '%Y-%m-%d',      # Desired output format
    default: Any = None                   # Default value if parsing fails
) -> Optional[str]
```

**Use Cases**:
- Standardizing date input from various sources
- Converting international date formats
- Preparing dates for database storage

**Examples**:
```python
DataCleaner.clean_date("01/15/2023")
# Result: "2023-01-15"

DataCleaner.clean_date("15 Jan 2023", output_format="%d-%m-%Y")
# Result: "15-01-2023"
```

---

## Data Structure Functions

### `clean_list()`
**Purpose**: Clean and process list data

```python
DataCleaner.clean_list(
    data_list: List[Any],
    remove_duplicates: bool = True,       # Remove duplicate items
    remove_empty: bool = True,            # Remove empty strings
    remove_none: bool = True,             # Remove None values
    sort: bool = False,                   # Sort the list
    unique_only: bool = True              # Keep only unique values
) -> List[Any]
```

**Use Cases**:
- Cleaning user input arrays
- Processing tag lists
- Preparing data for analysis

### `clean_dict()`
**Purpose**: Clean dictionary keys and values

```python
DataCleaner.clean_dict(
    data_dict: Dict[str, Any],
    remove_empty_values: bool = True,     # Remove entries with empty values
    remove_none_values: bool = True,      # Remove entries with None values
    strip_keys: bool = True,               # Strip whitespace from keys
    convert_keys_to_lower: bool = False    # Convert keys to lowercase
) -> Dict[str, Any]
```

**Use Cases**:
- Cleaning JSON data
- Processing configuration dictionaries
- Standardizing API responses

### `clean_dataframe()`
**Purpose**: Comprehensive pandas DataFrame cleaning

```python
DataCleaner.clean_dataframe(
    df: pd.DataFrame,
    handle_missing: str = 'fill',         # 'fill', 'drop', 'interpolate'
    fill_value: Any = None,               # Custom fill value
    remove_duplicates: bool = True,       # Remove duplicate rows
    strip_strings: bool = True,           # Strip whitespace from strings
    convert_dates: bool = True             # Auto-convert date columns
) -> pd.DataFrame
```

**Use Cases**:
- ETL pipeline data cleaning
- Preparing data for analysis
- Data quality improvement

---

## Advanced Text Processing

### `standardize_text()`
**Purpose**: NLP preprocessing and text standardization

```python
DataCleaner.standardize_text(
    text: str,
    remove_stopwords: bool = False,       # Remove common stopwords
    stem: bool = False,                   # Apply basic stemming
    custom_stopwords: List[str] = None     # Additional stopwords to remove
) -> str
```

**Use Cases**:
- Preparing text for machine learning
- Text analysis preprocessing
- Search indexing preparation

---

## Statistical Functions

### Built-in Patterns
The library includes regex patterns for common data types:

```python
DataCleaner.PATTERNS = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}$',
    'url': r'^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$',
    'ssn': r'^\d{3}-\d{2}-\d{4}$',
    'credit_card': r'^\d{4}[-]?\d{4}[-]?\d{4}[-]?\d{4}$',
    'zipcode': r'^\d{5}(?:[-\s]\d{4})?$',
    'ip_address': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
}
```

---

## Convenience Functions

For quick access without class instantiation:

```python
from data_cleaner import clean_string, clean_numeric, clean_email, clean_phone, clean_date

# Direct function calls
clean_text = clean_string("  messy text  ")
clean_num = clean_numeric("$1,234.56", remove_units=True)
clean_email = clean_email("USER@DOMAIN.COM")
clean_phone = clean_phone("(555) 123-4567")
clean_date = clean_date("01/15/2023")
```

---

## Use Case Matrix

| Scenario | Primary Function(s) | Example |
|----------|-------------------|---------|
| **User Registration** | `clean_email()`, `clean_phone()`, `clean_string()` | Validate and standardize user input |
| **Financial Data** | `clean_numeric()`, `clean_dataframe()` | Process currency and amounts |
| **Text Analysis** | `standardize_text()`, `clean_string()` | NLP preprocessing |
| **Data Import/Export** | `clean_dataframe()`, `clean_date()` | ETL pipeline cleaning |
| **Contact Management** | `clean_email()`, `clean_phone()`, `clean_dict()` | CRM data standardization |
| **Web Scraping** | `decode_html_entities()`, `clean_string()` | Clean scraped content |
| **Survey Data** | `clean_list()`, `clean_numeric()`, `clean_dataframe()` | Process survey responses |
| **Sensor Data** | `clean_numeric()`, `remove_outliers_iqr()` | IoT data processing |
| **API Integration** | `clean_dict()`, `clean_date()` | Standardize API responses |
| **Data Migration** | `clean_dataframe()`, `clean_string()` | Legacy data cleanup |

---

## Performance Guidelines

### Best Practices

1. **Batch Processing**: Use DataFrame functions for large datasets
2. **Memory Efficiency**: Process data in chunks for very large files
3. **Error Handling**: Always check return values for None/defaults
4. **Type Safety**: Use type hints for better code documentation

### Performance Tips

```python
# Good: Vectorized operations with pandas
df['cleaned_column'] = df['messy_column'].apply(DataCleaner.clean_string)

# Avoid: Looping through DataFrames
for index, row in df.iterrows():
    df.loc[index, 'cleaned'] = DataCleaner.clean_string(row['messy'])

# Good: Batch processing
cleaned_list = DataCleaner.clean_list(large_list, remove_duplicates=True)

# Good: Handle missing values appropriately
cleaned_df = DataCleaner.clean_dataframe(df, handle_missing='fill')
```

---

## Error Handling Reference

### Common Return Values

| Function | Error Condition | Return Value |
|----------|----------------|--------------|
| `clean_email()` | Invalid email format | `None` |
| `clean_phone()` | Invalid phone format | `None` |
| `clean_numeric()` | Conversion fails | `default` parameter |
| `clean_date()` | Parsing fails | `default` parameter |
| `clean_list()` | Input not a list | `[]` (empty list) |
| `clean_dict()` | Input not a dict | `{}` (empty dict) |
| `clean_dataframe()` | Input is None | Empty DataFrame |

---

## Integration Examples

### With Pandas
```python
import pandas as pd
from data_cleaner import DataCleaner

# Apply cleaning to DataFrame columns
df['clean_email'] = df['email'].apply(DataCleaner.clean_email)
df['clean_phone'] = df['phone'].apply(DataCleaner.clean_phone)
df['clean_salary'] = df['salary'].apply(lambda x: DataCleaner.clean_numeric(x, remove_units=True))
```

### With NumPy
```python
import numpy as np
from data_cleaner import DataCleaner

# Clean numeric arrays
messy_numbers = np.array(['$1,000', '$2,500', '$3,750'])
clean_numbers = [DataCleaner.clean_numeric(x, remove_units=True) for x in messy_numbers]
```

### With JSON APIs
```python
import json
from data_cleaner import DataCleaner

# Clean API response
response = json.loads(api_data)
cleaned_data = DataCleaner.clean_dict(response, strip_keys=True, remove_empty_values=True)
```

This catalogue serves as a comprehensive reference for all available functions and their optimal use cases in data cleaning workflows.
