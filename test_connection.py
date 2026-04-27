"""Testi Supabase ühendust."""
import sys
sys.path.insert(0, "dashboard")
 
from data_loader import load_sales, load_customers, load_products
 
print("=== Supabase ühenduse test ===\n")
 
# Test 1: Müügiandmed
df_sales = load_sales()
print(f"Müügitabel (sales): {len(df_sales)} rida, {len(df_sales.columns)} veergu")
print(f"Veerud: {list(df_sales.columns)}")
print(f"\nEsimesed 3 rida:")
print(df_sales.head(3))
print()
 
# Test 2: Kliendiandmed
df_customers = load_customers()
print(f"Klienditabel (customers): {len(df_customers)} rida")
print()
 
# Test 3: Tooteandmed
df_products = load_products()
print(f"Tootetabel (products): {len(df_products)} rida")
print()
 
print("=== Kõik testid edukad! ===")