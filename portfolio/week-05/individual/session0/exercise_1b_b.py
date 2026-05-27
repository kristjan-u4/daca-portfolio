import plotly.express as px
import pandas as pd

# 1. Valmistame andmed ette
data = {
    "Toode": [
        "Denim Jacket", 
        "Urban Sneakers", 
        "Hoodie Classic", 
        "Street Tee", 
        "Canvas Bag"
    ],
    "Käive (€)": [45000, 35000, 28000, 21000, 16000]
}

df = pd.DataFrame(data)

# 2. Loome tulpdiagrammi (Bar chart)
fig = px.bar(
    df, 
    x="Toode",
    y="Käive (€)",
    title="TOP 5 toodet käibe järgi",
    text_auto='.s', # Lisab tulpadel olevad väärtused automaatselt
    color="Käive (€)", # Muudab tulba värvi vastavalt summale
    color_continuous_scale="Viridis" # Valib ilusa värvigamma
)

# 3. Kuvame diagrammi
fig.show()