import logging
import pandas as pd

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_data(df_sales):
    """
    Clean and validate the sales DataFrame for downstream analysis.
    
    Performs the following cleaning operations:
    1. Converts "sale_date" to datetime and drops rows with invalid dates.
    2. Removes rows where "total_price" is zero or negative.
    3. Drops rows with duplicate "sale_id" values, keeping the first occurrence.
    4. Removes rows where "customer_id" is missing.
    5. Fills missing "store_location" values with "Online".
    6. Converts "customer_id" from float to integer after handling missing values.
    7. Resets the row index to ensure a continuous, sequential integer range.
    
    Args:
        df_sales (pd.DataFrame): The raw input sales DataFrame.
        
    Returns:
        pd.DataFrame: A cleaned and filtered copy of the input DataFrame.
    """
    # Create a copy to prevent modifying the original dataframe
    df_clean = df_sales.copy()
    
    # 1. Convert sale_date to datetime and drop invalid rows (NaT)
    df_clean["sale_date"] = pd.to_datetime(df_clean["sale_date"], errors="coerce")
    df_clean = df_clean.dropna(subset=["sale_date"])
    
    # 2. Keep only rows where total_price is strictly positive
    df_clean = df_clean[df_clean["total_price"] > 0]
    
    # 3. Remove duplicate sale_id rows (keeps the first instance)
    df_clean = df_clean.drop_duplicates(subset=["sale_id"])
    
    # 4. Remove rows where customer_id is missing
    df_clean = df_clean.dropna(subset=["customer_id"])
    
    # 5. Fill missing store_location values with "Online"
    df_clean["store_location"] = df_clean["store_location"].fillna("Online")
    
    # 6. Convert customer_id to integer (safe now that missing values are removed)
    df_clean["customer_id"] = df_clean["customer_id"].astype(int)
    
    # 7. Reset the index to be clean and sequential (0, 1, 2, 3...)
    df_clean = df_clean.reset_index(drop=True)
    
    return df_clean

# Audit log is not required in this particular role, but if it was, here would be an example
# of sales data cleaning with audit log.
def clean_data_with_full_audit(df_sales):
    """
    Cleans the sales DataFrame and generates a comprehensive audit report.
    The report contains full original rows that were either removed or modified,
    along with audit columns detailing the actions taken.
    
    Returns:
        tuple: (pd.DataFrame [cleaned_data], pd.DataFrame [audit_report])
    """
    # Create a copy of the original data that will be progressively filtered
    df_clean = df_sales.copy()
    
    # List to collect problematic rows in their full format along with audit info
    audit_rows = []

    # === 1. CHECK: Invalid or missing dates (REMOVAL) ===
    parsed_dates = pd.to_datetime(df_clean["sale_date"], errors="coerce")
    bad_date_mask = parsed_dates.isna()
    
    if bad_date_mask.any():
        # Extract those specific rows in their original format
        bad_dates = df_clean[bad_date_mask].copy()
        bad_dates["audit_action"] = "REMOVE_ROW"
        bad_dates["audit_reason"] = "Invalid or missing sale_date"
        audit_rows.append(bad_dates)
        
        # Remove from the clean dataframe
        df_clean = df_clean[~bad_date_mask]

    # === 2. CHECK: Negative or zero price (REMOVAL) ===
    bad_price_mask = df_clean["total_price"] <= 0
    if bad_price_mask.any():
        bad_prices = df_clean[bad_price_mask].copy()
        bad_prices["audit_action"] = "REMOVE_ROW"
        bad_prices["audit_reason"] = "Total price is zero or negative"
        audit_rows.append(bad_prices)
        
        df_clean = df_clean[~bad_price_mask]

    # === 3. CHECK: Missing customer ID (REMOVAL) ===
    missing_cust_mask = df_clean["customer_id"].isna()
    if missing_cust_mask.any():
        bad_customers = df_clean[missing_cust_mask].copy()
        bad_customers["audit_action"] = "REMOVE_ROW"
        bad_customers["audit_reason"] = "Missing customer_id"
        audit_rows.append(bad_customers)
        
        df_clean = df_clean[~missing_cust_mask]

    # === 4. CHECK: Missing store location (MODIFICATION / IMPUTATION) ===
    missing_store_mask = df_clean["store_location"].isna()
    if missing_store_mask.any():
        # Capture rows in their ORIGINAL state (where store_location is still NULL/NaN)
        modified_stores = df_clean[missing_store_mask].copy()
        modified_stores["audit_action"] = "MODIFY_VALUE"
        modified_stores["audit_reason"] = "Filled missing store_location with \"Online\""
        audit_rows.append(modified_stores)
        
        # Apply the modification to the clean dataframe
        df_clean["store_location"] = df_clean["store_location"].fillna("Online")

    # === 5. FINALIZATION (Type casting and index reset for the clean dataframe) ===
    df_clean["customer_id"] = df_clean["customer_id"].astype(int)
    df_clean = df_clean.reset_index(drop=True)

    # === 6. AUDIT REPORT CONCATENATION ===
    if audit_rows:
        # Concatenate all collected dataframes into a single audit report
        df_audit = pd.concat(audit_rows, ignore_index=True)
    else:
        # If no errors or modifications occurred, return an empty dataframe with correct columns
        audit_columns = list(df_sales.columns) + ["audit_action", "audit_reason"]
        df_audit = pd.DataFrame(columns=audit_columns)
    
    return df_clean, df_audit

def calculate_weekly_aggregates(df_sales_clean):
    """
    Aggregates sales data by week, calculating total revenue, number of transactions,
    and average transaction value for each week.

    Args:
        df_sales_clean (pd.DataFrame): A DataFrame containing cleaned sales data,
                                       with "sale_date" (datetime) and "total_price" columns.

    Returns:
        pd.DataFrame: A new DataFrame with weekly aggregates, indexed by the start of the week.
    """
    if df_sales_clean.empty:
        return pd.DataFrame(columns=["total_revenue", "number_of_orders", "avg_order_value"])

    # Group by week and calculate aggregates
    # Create a copy to avoid modifying the original df_sales_clean
    df_temp = df_sales_clean.copy()
    
    # Calculate the week period for each sale date
    df_temp["week"] = df_temp["sale_date"].dt.to_period("W")

    # Group by week and calculate aggregates
    weekly_aggregates = df_temp.groupby("week").agg(
        total_revenue=("total_price", "sum"),
        number_of_orders=("sale_id", "count"), # Assuming sale_id is unique per order
        avg_order_value=("total_price", "mean")
    ).reset_index() # Reset index to make "week" a column

    logger.info(f"Weekly aggregates dimensions: {weekly_aggregates.shape}")
    logger.info(f"First 5 rows of weekly aggregates:\n{weekly_aggregates.head().to_string()}")

    return weekly_aggregates


def calculate_kpis(df_sales_clean):
    """
    Calculates key performance indicators (KPIs) from the cleaned sales data.

    Args:
        df_sales_clean (pd.DataFrame): A DataFrame containing cleaned sales data,
                                       with "total_price" and "customer_id" columns.

    Returns:
        dict: A dictionary containing the calculated KPIs:
              - total_revenue (float): Sum of all total_price values.
              - unique_customers (int): Count of unique customer_id values.
              - avg_order_value (float): Average of all total_price values.
    """
    if df_sales_clean.empty:
        return {
            "total_revenue": 0.0,
            "unique_customers": 0,
            "avg_order_value": 0.0
        }

    total_revenue = df_sales_clean["total_price"].sum()
    unique_customers = df_sales_clean["customer_id"].nunique()
    avg_order_value = df_sales_clean["total_price"].mean()

    kpis = {
        "total_revenue": total_revenue,
        "unique_customers": unique_customers,
        "avg_order_value": avg_order_value
    }
    logger.info(f"Calculated KPIs: {kpis}")
    return kpis


def merge_datasets(df_sales_clean, df_customers):
    """
    Merges cleaned sales data with customer data using a left join on "customer_id".

    Args:
        df_sales_clean (pd.DataFrame): Cleaned sales DataFrame with "customer_id".
        df_customers (pd.DataFrame): Customer DataFrame with "customer_id".

    Returns:
        pd.DataFrame: Merged DataFrame containing sales and customer information.
    """
    if df_sales_clean.empty:
        logger.warning("df_sales_clean is empty, returning empty DataFrame from merge_datasets.")
        return pd.DataFrame(columns=list(df_sales_clean.columns) + [col for col in df_customers.columns if col != "customer_id"])

    if df_customers.empty:
        logger.warning("df_customers is empty, returning df_sales_clean as no customer data to merge.")
        return df_sales_clean

    merged_df = pd.merge(df_sales_clean, df_customers, on="customer_id", how="left")
    logger.info(f"Merged dataset dimensions: {merged_df.shape}")
    return merged_df
