import pandas as pd
import matplotlib.pyplot as plt
import json

# Sinu JSON andmed
data = [
    {"turunduskanal": "facebook ads", "kuu": "2024-12", "klientide_arv": 169},
    {"turunduskanal": "facebook ads", "kuu": "2023-12", "klientide_arv": 147},
    {"turunduskanal": "facebook ads", "kuu": "2023-03", "klientide_arv": 123},
    {"turunduskanal": "facebook ads", "kuu": "2024-06", "klientide_arv": 172},
    {"turunduskanal": "facebook ads", "kuu": "2024-03", "klientide_arv": 126},
    {"turunduskanal": "facebook ads", "kuu": "2023-06", "klientide_arv": 129},
    {"turunduskanal": "facebook ads", "kuu": "2023-07", "klientide_arv": 143},
    {"turunduskanal": "facebook ads", "kuu": "2024-10", "klientide_arv": 138},
    {"turunduskanal": "facebook ads", "kuu": "2024-08", "klientide_arv": 170},
    {"turunduskanal": "facebook ads", "kuu": "2024-04", "klientide_arv": 136},
    {"turunduskanal": "facebook ads", "kuu": "2023-11", "klientide_arv": 104},
    {"turunduskanal": "facebook ads", "kuu": "2023-08", "klientide_arv": 151},
    {"turunduskanal": "facebook ads", "kuu": "2025-02", "klientide_arv": 104},
    {"turunduskanal": "facebook ads", "kuu": "2024-05", "klientide_arv": 138},
    {"turunduskanal": "facebook ads", "kuu": "2023-05", "klientide_arv": 115},
    {"turunduskanal": "facebook ads", "kuu": "2023-10", "klientide_arv": 94},
    {"turunduskanal": "facebook ads", "kuu": "2023-04", "klientide_arv": 116},
    {"turunduskanal": "facebook ads", "kuu": "2023-02", "klientide_arv": 86},
    {"turunduskanal": "facebook ads", "kuu": "2024-07", "klientide_arv": 158},
    {"turunduskanal": "facebook ads", "kuu": "2024-02", "klientide_arv": 95},
    {"turunduskanal": "facebook ads", "kuu": "2024-11", "klientide_arv": 113},
    {"turunduskanal": "facebook ads", "kuu": "2024-01", "klientide_arv": 115},
    {"turunduskanal": "facebook ads", "kuu": "2024-09", "klientide_arv": 126},
    {"turunduskanal": "facebook ads", "kuu": "2023-09", "klientide_arv": 100},
    {"turunduskanal": "facebook ads", "kuu": "2025-01", "klientide_arv": 101},
    {"turunduskanal": "facebook ads", "kuu": "2023-01", "klientide_arv": 97}
]

# 1. Teeme andmed DataFrame'iks
df = pd.DataFrame(data)

# 2. Muudame 'kuu' veeru kuupäeva tüübiks ja sorteerime
df['kuu'] = pd.to_datetime(df['kuu'])
df = df.sort_values('kuu')

# 3. Joonistame graafiku
plt.figure(figsize=(12, 6))
plt.plot(df['kuu'], df['klientide_arv'], marker='o', linestyle='-', color='#1877F2', linewidth=2)

# 4. Kujundus
plt.title('Facebook Ads: Klientide arv kuude lõikes', fontsize=14, pad=20)
plt.xlabel('Kuu', fontsize=12)
plt.ylabel('Klientide arv', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(df['kuu'], df['kuu'].dt.strftime('%Y-%m'), rotation=45)

# Hoiame ära siltide lõikumise
plt.tight_layout()

# 5. Näitame graafikut
plt.show()