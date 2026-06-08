from dateutil.relativedelta import relativedelta
import math

def format_date(date):
    """
    Format a date object into Estonian date format string (DD.MM.YYYY).

    Args:
        date (datetime.date): The date to format.

    Returns:
        str: The formatted date string.
    """
    return date.strftime("%d.%m.%Y")

def format_date_as_text(date):
    """
    Format a date object into a text representation (Month Year).

    Args:
        date (datetime.date): The date to format.

    Returns:
        str: The formatted date string.
    """
    return date.strftime("%b %Y")

def calculate_previous_open_date_range(open_date_range):
    """
    Calculate a previous date range of the same duration as the given range.

    Args:
        open_date_range (tuple): A tuple containing (start_date, end_date).

    Returns:
        tuple: A tuple containing (previous_start_date, previous_end_date).
    """
    start_date = open_date_range[0]
    end_date = open_date_range[1]

    delta = relativedelta(end_date, start_date)

    previous_end_date = start_date
    previous_start_date = previous_end_date - delta

    return (previous_start_date, previous_end_date)

def format_metric_delta_as_percentage(metric_delta):
    """
    Format a metric delta value as a percentage string for KPI display.

    Args:
        metric_delta (float or None): The delta value to format.

    Returns:
        str or None: The formatted percentage string, or None if metric_delta is None.
    """
    if metric_delta:
        return f"{metric_delta:.0f} %"
    else:
        return None
    
def calculate_delta_in_percents(current_metric, previous_metric):
    """
    Calculate the percentage delta between current and previous metrics.

    Args:
        current_metric (float): The current metric value.
        previous_metric (float): The previous metric value.

    Returns:
        float or None: The percentage delta, or None if division by zero occurs.
    """
    try:
        delta = (current_metric - previous_metric) * 100 / previous_metric
        if math.isnan(delta) or math.isinf(delta):
            raise ZeroDivisionError
        return delta
    except ZeroDivisionError:
        return None

def format_eur_amount(value, precision=0):
    """
    Format a numeric value as a EUR currency string.

    Args:
        value (float): The numeric value to format.
        precision (int, optional): Decimal precision. Defaults to 0.

    Returns:
        str: The formatted currency string.
    """
    return f"€{format_number(value, precision)}"

def format_as_percentage(value, precision=0):
    """
    Format a decimal fraction value as a percentage string.

    Args:
        value (float): The decimal fraction (e.g., 0.15 for 15%).
        precision (int, optional): Decimal precision. Defaults to 0.

    Returns:
        str: The formatted percentage string.
    """
    perc = value * 100.0
    return f"{format_number(perc, precision)}%"

def format_number(value, precision=0):
    """
    Format a number with thousands separators as spaces and decimal separator as comma.

    Args:
        value (float): The number to format.
        precision (int, optional): Decimal precision. Defaults to 0.

    Returns:
        str: The formatted number string.
    """
    return f"{value:,.{precision}f}".replace(",", " ").replace(".", ",")
