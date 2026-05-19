# Nädal 8 grupitöö alaülesande roll A
# Ülesandeks on luua Python funktsioonid, mis pärivad UrbanStyle OÜ andmed Supabase API-st: müügi-, kliendi- ja tooteandmed.


# Impordin teegid
import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Loon Supabase client .env põhiselt (laen API tunnused .env failist)
load_dotenv()

supabase = create_client( 
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)


# Loon funktsiooni fetch_sales(), millega pärin müügiandmed ja loon DataFrame-i. Funktsioon võtab sisendiks valikulised algus- ja lõpukuupäevad
def fetch_sales(start_date: str = None, end_date: str = None):
    """
    Pärib kõik müügiandmed Supabase'st koos valikuliste kuupäevafiltritega.
    """
    all_data = []
    start_idx = 0
    batch_size = 1000       # Supabase'i maksimaalne ridade arv ühe päringuga

    try:
        while True:
            # Päring sales tabelisse
            query = supabase.table("sales").select("*")
            
            # Lisan filtrid, kui parameetrid on antud
            if start_date:
                query = query.gte("sale_date", start_date)      # greater than or equal
            if end_date:
                query = query.lte("sale_date", end_date)        # less than or equal

            # Määran andmevahemiku
            response = query.range(start_idx, start_idx + batch_size - 1).execute()    
            data = response.data

            # Kontrollin, kas andmed tulid
            if not data:
                break

            # Lisan saadud andmed üldnimekirja
            all_data.extend(data)

            # Kui sain vähem ridu kui batch_size, olen jõudnud lõpuni
            if len(data) < batch_size:
                break

            # Liigun järgmise lehekülje algusesse
            start_idx += batch_size
        
        # Teisendan koondnimekirja DataFrame'ks
        df = pd.DataFrame(all_data)
        
        # Veendun, et kuupäev on õiges formaadis (kui andmebaasist saadud tabel ei ole tühi, siis tuleb muuta sale_date veerg tekstist arvutatavaks kuupäevaks)
        if not df.empty:
            df['sale_date'] = pd.to_datetime(df['sale_date'])
            
        return df
    
    # Kui midagi läheb try plokis valesti, siis kuvab veateate
    except Exception as e:
        print(f"Viga müügiandmete pärimisel: {e}")
        return pd.DataFrame()


# Loon funktsiooni fetch_customers()
def fetch_customers():
    """
    Pärib kõik kliendiandmed Supabase'st.
    """
    all_data = []
    start_idx = 0
    batch_size = 1000

    try:
        while True:
            # 1. Teen päringu määratud vahemikuga (range)
            response = supabase.table("customers") \
                .select("*") \
                .range(start_idx, start_idx + batch_size - 1) \
                .execute()
            
            data = response.data
            
            if not data:
                break
                
            all_data.extend(data)
            
            if len(data) < batch_size:
                break
                
            start_idx += batch_size
            
        return pd.DataFrame(all_data)
        
    except Exception as e:
        print(f"Viga kliendiandmete pärimisel: {e}")
        return pd.DataFrame()       # annab tühja tabeli vastuseks, lubades ülejäänul koodil edasi töötada (nt raporti teistel osadel)


# Loon funktsiooni fetch_products()
def fetch_products():
    """
    Pärib kõik tooteandmed Supabase'st
    """
    try:
        response = supabase.table('products').select('*').execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        print(f'Viga tooteandmete pärimisel: {e}')
        return pd.DataFrame()


# Testin ja prindin tulemused kontrolliks
if __name__ == "__main__":
    print("--- UrbanStyle Andmete Pärimise Test ---")
    
    # Testin müügiandmeid näidisperioodiga
    df_sales = fetch_sales(start_date="2024-01-01", end_date="2024-03-31")
    print(f"Müüke leitud: {len(df_sales)}")
    print(df_sales.head())
    
    # Testin kliendiandmeid
    df_customers = fetch_customers()
    print(f'\nKliente leitud: {len(df_customers)}')
    print(df_customers.head())

    # Testin tooteandmeid
    df_products = fetch_products()
    print(f'\nTooteid leitud: {len(df_products)}')
    print(df_products.head())