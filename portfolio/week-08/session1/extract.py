import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

supabase = create_client( 
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

def get_data(table_name):
    try:
      data = []
      page_size = 1000
      page = 0
      while True:
          response = supabase.table(table_name).select('*').range(page * page_size, (page + 1) * page_size - 1).execute()
          data.extend(response.data)
          if len(response.data) < page_size:
              break
          page += 1
      return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error fetching data from {table_name}: {e}")
        return pd.read_csv(f'datasets/{table_name}.csv')