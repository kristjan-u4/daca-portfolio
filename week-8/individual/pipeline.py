import logging
import time
import argparse
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

import data_fetcher
import transform
import visualize_export

def main():
    """Main entry point to be used in __main__ block"""
    try:
        logger.info("Parsing command line arguments")
        args = _parse_command_line_arguments()
        logger.info(f"Arguments parsed: {args}")

        start_time = time.time()
        logger.info("Launching pipeline process from main block")
        run_pipeline(args.start_date, args.end_date)
        end_time = time.time()
        elapsed_seconds = round(end_time - start_time, 2)
        logger.info(f"Pipeline process finished. Elapsed time: {elapsed_seconds} seconds.")
    except Exception as e:
        logger.exception(f"Exception caught in the main block: {e}")


def run_pipeline(start_date, end_date):
    try:
        logger.info("Starting: fetch")
        df_sales = data_fetcher.fetch_sales(start_date, end_date)
        df_customers = data_fetcher.fetch_customers()
        df_products = data_fetcher.fetch_products()
        logger.info("Finished: fetch")

        logger.info("Starting: clean")
        logger.info("Finished: clean")

        logger.info("Starting: aggregate")
        logger.info("Finished: aggregate")

        logger.info("Starting: visualize")
        logger.info("Finished: visualize")

        logger.info("Starting: export")
        logger.info("Finished: export")
    except Exception as e:
        logger.exception(f"Pipeline failed with exception: {e}")


def _parse_command_line_arguments():
    """
    Parse and validate command-line arguments for the pipeline.
    
    Returns:
        argparse.Namespace: Parsed arguments containing start_date and end_date.
    """
    parser = argparse.ArgumentParser(description="UrbanStyle sales data pipeline")
    
    today = datetime.now().date()
    default_start = today - timedelta(days=1)
    default_end = default_start
    
    parser.add_argument(
        "--start-date", 
        type=_normalize_date, 
        default=default_start,
        help="Start date (YYYY-MM-DD). Defaults to the start of the previous period."
    )
    
    parser.add_argument(
        "--end-date", 
        type=_normalize_date, 
        default=default_end,
        help="End date (YYYY-MM-DD). Defaults to the end of the previous period."
    )

    return parser.parse_args()

def _normalize_date(date_str):
    """Convert string to datetime.date object for argparse."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{date_str}'. Use YYYY-MM-DD.")


if __name__ == "__main__":
    main()
