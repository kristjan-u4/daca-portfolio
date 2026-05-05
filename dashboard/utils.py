from dateutil.relativedelta import relativedelta
import math

# Eesti formaat kuupäevadele.
def format_date(date):
    return date.strftime("%d.%m.%Y")

def format_date_as_text(date):
    return date.strftime("%b %Y")

# Arvutab sama pika võrdlusajavahemiku etteantud ajavahemikule.
def calculate_previous_open_date_range(open_date_range):
    start_date = open_date_range[0]
    end_date = open_date_range[1]

    delta = relativedelta(end_date, start_date)

    previous_end_date = start_date
    previous_start_date = previous_end_date - delta

    return(previous_start_date, previous_end_date)

# Vormindab muutuse KPI mõõdikul näitamiseks protsendina (None - ei näidata).
def format_metric_delta_as_percentage(metric_delta):
    if metric_delta:
        return f"{metric_delta:.0f} %"
    else:
        return None
    
def calculate_delta_in_percents(current_metric, previous_metric):
    try:
        delta = (current_metric - previous_metric) * 100 / previous_metric
        if math.isnan(delta) or math.isinf(delta):
            raise ZeroDivisionError
        return delta
    except ZeroDivisionError:
        return None

def format_eur_amount(value, precision=0):
    return f"€{format_number(value, precision)}"

def format_number(value, precision=0):
    return f"{value:,.{precision}f}".replace(",", " ").replace(".", ",")