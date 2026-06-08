from dateutil.relativedelta import relativedelta
import math

def format_date(date):
    """
    Formats a date object into a string using the "DD Mon YYYY" format.

    Args:
        date (datetime.date): The date object to format.

    Returns:
        str: The formatted date string (e.g., "05 Jun 2024").
    """
    return date.strftime("%d %b %Y")

def format_date_month_precision(date):
    """
    Formats a date object into a string using the "Mon YYYY" format.

    Args:
        date (datetime.date): The date object to format.

    Returns:
        str: The formatted date string (e.g., "Jun 2024").
    """
    return date.strftime("%b %Y")

def calculate_previous_open_date_range(open_date_range):
    """
    Calculates a comparison date range of the same length preceding the given date range.

    Args:
        open_date_range (tuple): A tuple containing the start and end dates
                                 (datetime.date) of the current period.

    Returns:
        tuple: A tuple containing the start and end dates (datetime.date)
               of the previous comparison period.
    """
    start_date = open_date_range[0]
    end_date = open_date_range[1]

    delta = relativedelta(end_date, start_date)

    previous_end_date = start_date
    previous_start_date = previous_end_date - delta

    return (previous_start_date, previous_end_date)

def format_metric_delta_as_percentage(metric_delta):
    """
    Formats a metric delta as a percentage string for display, or None if no delta.

    Args:
        metric_delta (float or None): The percentage change as a float, or None.

    Returns:
        str or None: The formatted percentage string (e.g., "10 %") or None.
    """
    if metric_delta:
        return f"{metric_delta:.0f} %"
    else:
        return None

def format_eur_amount(value, precision=0):
    """
    Formats a numeric value as a Euro amount string, using comma as thousands
    separator and dot as decimal separator, with an Euro symbol prefix.

    Args:
        value (float or int): The numeric value to format.
        precision (int): The number of decimal places.

    Returns:
        str: The formatted Euro amount string (e.g., "€1,234.00").
    """
    return f"€{value:,.{precision}f}"

def format_as_percentage(value, precision=0):
    """
    Formats a numeric value as a percentage string, using comma as thousands
    separator and dot as decimal separator, with a percentage symbol suffix.

    Args:
        value (float or int): The numeric value to format.
        precision (int): The number of decimal places.

    Returns:
        str: The formatted percentage string (e.g., "10.00 %").
    """
    return f"{value:,.{precision}f} %"

def format_number(value, precision=0):
    """
    Formats a numeric value as a string, using comma as thousands separator
    and dot as decimal separator.

    Args:
        value (float or int): The numeric value to format.
        precision (int): The number of decimal places.

    Returns:
        str: The formatted number string (e.g., "1,234").
    """
    return f"{value:,.{precision}f}"

def calculate_delta_in_percents(current_metric, previous_metric):
    """
    Calculates the percentage change between a current and a previous metric.

    Args:
        current_metric (float or int): The current value of the metric.
        previous_metric (float or int): The previous value of the metric.

    Returns:
        float or None: The percentage change, or None if the previous metric is zero
                       or results in NaN/infinity.
    """
    try:
        delta = (current_metric - previous_metric) * 100 / previous_metric
        if math.isnan(delta) or math.isinf(delta):
            raise ZeroDivisionError
        return delta
    except ZeroDivisionError:
        return None
