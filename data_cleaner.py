"""
data_cleaner.py - A comprehensive data cleaning utility library
"""

import re
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Union, List, Dict, Any, Optional
import unicodedata
import html

class DataCleaner:
    """
    A versatile data cleaning utility for various data types and formats
    """
    
    # Common patterns for different data types
    PATTERNS = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'phone': r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}$',
        'url': r'^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$',
        'ssn': r'^\d{3}-\d{2}-\d{4}$',
        'credit_card': r'^\d{4}[-]?\d{4}[-]?\d{4}[-]?\d{4}$',
        'zipcode': r'^\d{5}(?:[-\s]\d{4})?$',
        'ip_address': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    }
    
    @staticmethod
    def clean_string(text: str, 
                    strip: bool = True, 
                    lower: bool = False,
                    remove_extra_spaces: bool = True,
                    remove_special_chars: bool = False,
                    replace_special_with_space: bool = False) -> str:
        """
        Clean string data by applying various transformations
        
        Args:
            text: Input string to clean
            strip: Remove leading/trailing whitespace
            lower: Convert to lowercase
            remove_extra_spaces: Replace multiple spaces with single space
            remove_special_chars: Remove all special characters
            replace_special_with_space: Replace special characters with space
        
        Returns:
            Cleaned string
        """
        if not isinstance(text, str):
            text = str(text) if text is not None else ''
        
        if strip:
            text = text.strip()
        
        if lower:
            text = text.lower()
        
        if remove_extra_spaces:
            text = re.sub(r'\s+', ' ', text)
        
        if remove_special_chars:
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        if replace_special_with_space:
            text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
        
        return text
    
    @staticmethod
    def clean_numeric(value: Union[int, float, str],
                     default: float = 0.0,
                     remove_units: bool = True,
                     allow_negative: bool = True,
                     max_value: Optional[float] = None,
                     min_value: Optional[float] = None) -> float:
        """
        Clean and convert numeric data
        
        Args:
            value: Input value to clean
            default: Default value if conversion fails
            remove_units: Remove common unit suffixes
            allow_negative: Whether to allow negative numbers
            max_value: Maximum allowed value
            min_value: Minimum allowed value
        
        Returns:
            Cleaned numeric value
        """
        try:
            if isinstance(value, str):
                if remove_units:
                    # Remove common unit patterns
                    value = re.sub(r'[$€£]', '', value)
                    value = re.sub(r'(kg|km|m|cm|mm|l|ml|gb|mb|kb|%)', '', value, flags=re.IGNORECASE)
                    # Remove common text units and descriptors
                    value = re.sub(r'(per year|per annum|annually|yearly|k|thousand)', '', value, flags=re.IGNORECASE)
                # Remove commas from numbers
                value = value.replace(',', '')
                # Clean up any remaining non-numeric characters (except decimal point and minus)
                value = re.sub(r'[^\d.\-]', '', value)
                
            numeric_value = float(value)
            
            if not allow_negative and numeric_value < 0:
                numeric_value = abs(numeric_value)
            
            if max_value is not None and numeric_value > max_value:
                numeric_value = max_value
            
            if min_value is not None and numeric_value < min_value:
                numeric_value = min_value
                
            return numeric_value
            
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def clean_date(date_string: str,
                  formats: List[str] = None,
                  output_format: str = '%Y-%m-%d',
                  default: Any = None) -> Optional[str]:
        """
        Parse and format date strings
        
        Args:
            date_string: Input date string
            formats: List of possible date formats to try
            output_format: Desired output date format
            default: Default value if parsing fails
        
        Returns:
            Formatted date string
        """
        if not date_string:
            return default
            
        if formats is None:
            formats = [
                '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d',
                '%d-%m-%Y', '%m-%d-%Y', '%b %d, %Y', '%B %d, %Y',
                '%Y%m%d', '%d.%m.%Y', '%m.%d.%Y'
            ]
        
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_string.strip(), fmt)
                return date_obj.strftime(output_format)
            except ValueError:
                continue
        
        return default
    
    @staticmethod
    def clean_email(email: str) -> Optional[str]:
        """
        Validate and clean email address
        
        Args:
            email: Email address to clean
        
        Returns:
            Cleaned email or None if invalid
        """
        if not email:
            return None
        
        email = DataCleaner.clean_string(email, strip=True, lower=True)
        
        if re.match(DataCleaner.PATTERNS['email'], email):
            return email
        return None
    
    @staticmethod
    def clean_phone(phone: str,
                   format_as_international: bool = True,
                   remove_extension: bool = True) -> Optional[str]:
        """
        Clean and format phone numbers
        
        Args:
            phone: Phone number to clean
            format_as_international: Format with country code
            remove_extension: Remove phone extensions
        
        Returns:
            Cleaned phone number or None if invalid
        """
        if not phone:
            return None
        
        # Extract only digits and plus sign
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        if remove_extension:
            cleaned = re.sub(r'x\d+', '', cleaned, flags=re.IGNORECASE)
        
        # Basic validation
        if len(cleaned) < 10:
            return None
        
        if format_as_international:
            if cleaned.startswith('+'):
                return cleaned
            elif cleaned.startswith('00'):
                cleaned = '+' + cleaned[2:]
            elif len(cleaned) == 10:
                cleaned = '+1' + cleaned  # Default to US/Canada
            else:
                cleaned = '+' + cleaned
        
        return cleaned
    
    @staticmethod
    def clean_whitespace(text: str,
                        remove_leading_trailing: bool = True,
                        collapse_spaces: bool = True,
                        remove_newlines: bool = True) -> str:
        """
        Advanced whitespace cleaning
        
        Args:
            text: Input text
            remove_leading_trailing: Strip whitespace from ends
            collapse_spaces: Convert multiple spaces to single
            remove_newlines: Remove newline characters
        
        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            text = str(text) if text is not None else ''
        
        if remove_leading_trailing:
            text = text.strip()
        
        if collapse_spaces:
            text = re.sub(r' +', ' ', text)
        
        if remove_newlines:
            text = re.sub(r'[\n\r\t]+', ' ', text)
            text = re.sub(r' +', ' ', text)
        
        return text
    
    @staticmethod
    def normalize_unicode(text: str, form: str = 'NFKC') -> str:
        """
        Normalize Unicode characters
        
        Args:
            text: Input text
            form: Unicode normalization form (NFC, NFKC, NFD, NFKD)
        
        Returns:
            Normalized text
        """
        if not isinstance(text, str):
            text = str(text) if text is not None else ''
        
        return unicodedata.normalize(form, text)
    
    @staticmethod
    def decode_html_entities(text: str) -> str:
        """
        Decode HTML entities
        
        Args:
            text: Text containing HTML entities
        
        Returns:
            Text with decoded HTML entities
        """
        if not isinstance(text, str):
            text = str(text) if text is not None else ''
        
        return html.unescape(text)
    
    @staticmethod
    def clean_list(data_list: List[Any],
                  remove_duplicates: bool = True,
                  remove_empty: bool = True,
                  remove_none: bool = True,
                  sort: bool = False,
                  unique_only: bool = True) -> List[Any]:
        """
        Clean list data
        
        Args:
            data_list: Input list
            remove_duplicates: Remove duplicate items
            remove_empty: Remove empty strings
            remove_none: Remove None values
            sort: Sort the list
            unique_only: Keep only unique values (if remove_duplicates=False)
        
        Returns:
            Cleaned list
        """
        if not isinstance(data_list, list):
            return []
        
        cleaned = data_list.copy()
        
        if remove_empty:
            cleaned = [x for x in cleaned if str(x).strip() != '']
        
        if remove_none:
            cleaned = [x for x in cleaned if x is not None]
        
        # Strip whitespace from remaining items if they're strings
        cleaned = [x.strip() if isinstance(x, str) else x for x in cleaned]
        
        if remove_duplicates or unique_only:
            # Preserve order while removing duplicates
            seen = set()
            cleaned = [x for x in cleaned if not (x in seen or seen.add(x))]
        
        if sort:
            try:
                cleaned.sort()
            except TypeError:
                # Handle mixed types by converting to string for sorting
                cleaned.sort(key=str)
        
        return cleaned
    
    @staticmethod
    def clean_dict(data_dict: Dict[str, Any],
                  remove_empty_values: bool = True,
                  remove_none_values: bool = True,
                  strip_keys: bool = True,
                  convert_keys_to_lower: bool = False) -> Dict[str, Any]:
        """
        Clean dictionary data
        
        Args:
            data_dict: Input dictionary
            remove_empty_values: Remove entries with empty string values
            remove_none_values: Remove entries with None values
            strip_keys: Strip whitespace from keys
            convert_keys_to_lower: Convert keys to lowercase
        
        Returns:
            Cleaned dictionary
        """
        if not isinstance(data_dict, dict):
            return {}
        
        cleaned = {}
        
        for key, value in data_dict.items():
            # Clean key
            if strip_keys and isinstance(key, str):
                key = key.strip()
            
            if convert_keys_to_lower and isinstance(key, str):
                key = key.lower()
            
            # Skip unwanted values
            if remove_empty_values and value == '':
                continue
            if remove_none_values and value is None:
                continue
            
            cleaned[key] = value
        
        return cleaned
    
    @staticmethod
    def clean_dataframe(df: pd.DataFrame,
                        handle_missing: str = 'fill',  # 'fill', 'drop', 'interpolate'
                        fill_value: Any = None,
                        remove_duplicates: bool = True,
                        strip_strings: bool = True,
                        convert_dates: bool = True) -> pd.DataFrame:
        """
        Clean pandas DataFrame
        
        Args:
            df: Input DataFrame
            handle_missing: Strategy for missing values
            fill_value: Value to fill missing values with
            remove_duplicates: Remove duplicate rows
            strip_strings: Strip whitespace from string columns
            convert_dates: Attempt to convert date columns
        
        Returns:
            Cleaned DataFrame
        """
        if df is None:
            return pd.DataFrame()
        
        cleaned_df = df.copy()
        
        # Handle missing values
        if handle_missing == 'fill':
            if fill_value is not None:
                cleaned_df = cleaned_df.fillna(fill_value)
            else:
                # Fill numeric with mean, categorical with mode
                for col in cleaned_df.columns:
                    if cleaned_df[col].dtype in ['int64', 'float64']:
                        cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mean())
                    else:
                        cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mode()[0] if not cleaned_df[col].mode().empty else '')
        elif handle_missing == 'drop':
            cleaned_df = cleaned_df.dropna()
        elif handle_missing == 'interpolate':
            cleaned_df = cleaned_df.interpolate()
        
        # Remove duplicates
        if remove_duplicates:
            cleaned_df = cleaned_df.drop_duplicates()
        
        # Clean string columns
        if strip_strings:
            string_columns = cleaned_df.select_dtypes(include=['object']).columns
            for col in string_columns:
                cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
                # Try to clean numeric strings that contain currency symbols
                if cleaned_df[col].str.contains(r'[$€£]', na=False).any():
                    try:
                        cleaned_df[col] = cleaned_df[col].apply(
                            lambda x: DataCleaner.clean_numeric(x, remove_units=True) 
                            if pd.notna(x) and isinstance(x, str) and x.strip() else x
                        )
                    except:
                        pass  # If conversion fails, keep original values
        
        # Convert date columns
        if convert_dates:
            for col in cleaned_df.columns:
                try:
                    cleaned_df[col] = pd.to_datetime(cleaned_df[col])
                except (ValueError, TypeError):
                    pass
        
        return cleaned_df
    
    @staticmethod
    def remove_outliers_iqr(data: Union[List[float], pd.Series, np.ndarray],
                           multiplier: float = 1.5) -> List[float]:
        """
        Remove outliers using IQR method
        
        Args:
            data: Input data
            multiplier: IQR multiplier (default: 1.5)
        
        Returns:
            Data without outliers
        """
        if isinstance(data, list):
            data = np.array(data)
        elif isinstance(data, pd.Series):
            data = data.values
        
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr
        
        return [x for x in data if lower_bound <= x <= upper_bound]
    
    @staticmethod
    def standardize_text(text: str,
                        remove_stopwords: bool = False,
                        stem: bool = False,
                        custom_stopwords: List[str] = None) -> str:
        """
        Advanced text standardization for NLP preprocessing
        
        Args:
            text: Input text
            remove_stopwords: Whether to remove stopwords
            stem: Whether to perform basic stemming
            custom_stopwords: Additional stopwords to remove
        
        Returns:
            Standardized text
        """
        # Common stopwords
        stopwords = {'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
                     'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
                     'to', 'was', 'were', 'will', 'with'}
        
        if custom_stopwords:
            stopwords.update(custom_stopwords)
        
        # Clean and tokenize
        text = DataCleaner.clean_string(text, lower=True, remove_special_chars=True)
        words = text.split()
        
        if remove_stopwords:
            words = [w for w in words if w not in stopwords]
        
        if stem:
            # Basic stemming (remove common suffixes)
            words = [re.sub(r'(ing|ed|es|s)$', '', w) for w in words]
        
        return ' '.join(words)


# Convenience functions for quick access
def clean_string(*args, **kwargs):
    return DataCleaner.clean_string(*args, **kwargs)

def clean_numeric(*args, **kwargs):
    return DataCleaner.clean_numeric(*args, **kwargs)

def clean_email(*args, **kwargs):
    return DataCleaner.clean_email(*args, **kwargs)

def clean_phone(*args, **kwargs):
    return DataCleaner.clean_phone(*args, **kwargs)

def clean_date(*args, **kwargs):
    return DataCleaner.clean_date(*args, **kwargs)

    
    