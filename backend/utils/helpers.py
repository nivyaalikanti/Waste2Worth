import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_numeric_from_range(range_str):
    """
    Extract numeric value from range strings like '16 GB' or '130–150 g'
    Returns the lower bound or extracted number
    """
    if pd.isna(range_str):
        return None
    
    range_str = str(range_str).lower().strip()
    
    # Remove units
    range_str = re.sub(r'gb|g|mah|years?', '', range_str, flags=re.IGNORECASE)
    range_str = range_str.strip()
    
    # Handle ranges like "130–150" or "130-150"
    if '–' in range_str or '-' in range_str:
        match = re.search(r'(\d+(?:\.\d+)?)', range_str)
        if match:
            return float(match.group(1))
    
    # Handle "Less than" or "<"
    if '<' in range_str or 'less than' in range_str:
        match = re.search(r'(\d+(?:\.\d+)?)', range_str)
        if match:
            return float(match.group(1)) * 0.5
    
    # Handle "Greater than" or ">"
    if '>' in range_str or 'more than' in range_str or 'above' in range_str:
        match = re.search(r'(\d+(?:\.\d+)?)', range_str)
        if match:
            return float(match.group(1)) * 1.5
    
    # Simple number extraction
    match = re.search(r'(\d+(?:\.\d+)?)', range_str)
    if match:
        return float(match.group(1))
    
    return None

def safe_float_convert(value, default=0.0):
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int_convert(value, default=0):
    """Safely convert value to int"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default