import re
from datetime import datetime

def clean_price(price_text):
    """
    Extracts numeric price from strings like 'Â£51.77' or '$10.00'.
    Handles encoding artifacts and currency symbols.
    """
    if not price_text:
        return 0.0
    # Use RegEx to find only numbers and the decimal point
    match = re.search(r"(\d+\.\d+)", price_text)
    if match:
        return float(match.group(1))
    return 0.0

def get_timestamp():
    """Returns a standardized ISO 8601 timestamp for data freshness."""
    return datetime.now().isoformat()

def format_filename(base_name, extension="json"):
    """Creates a unique filename with a date to avoid overwriting data."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    return f"{base_name}_{date_str}.{extension}"

def validate_data(data_list, required_keys):
    """
    Checks if the scraped data is complete. 
    Crucial for 'Quality Control' requirements at Mindrift.
    """
    valid_data = []
    for item in data_list:
        if all(key in item and item[key] for key in required_keys):
            valid_data.append(item)
    return valid_data