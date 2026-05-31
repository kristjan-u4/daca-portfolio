import plotly.express as px
import pandas as pd

# 1. Valmistame andmed ette
data = {
    "Kuu": ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun"],
    "Müük (€)": [18500, 17200, 20100, 22300, 21800, 24500]
}

df = pd.DataFrame(data)

# 2. Loome tulpdiagrammi (Bar chart)
fig = px.bar(
    df, 
    x="Kuu", 
    y="Müük (€)", 
    title="Müügitulu kuude lõikes (esimene poolaasta)",
    text_auto='.s', # Lisab tulpadel olevad väärtused automaatselt
    color="Müük (€)", # Muudab tulba värvi vastavalt summale
    color_continuous_scale="Viridis" # Valib ilusa värvigamma
)

# 3. Kuvame diagrammi
fig.show()