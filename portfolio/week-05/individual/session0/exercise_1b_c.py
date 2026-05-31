import pandas as pd
import plotly.express as px

# 1. Andmete ettevalmistamine
data = {
    "Asukoht": ["Tallinn", "Online", "Tartu", "Pärnu"],
    "Osakaal (%)": [42, 28, 18, 12]
}

df = pd.DataFrame(data)

# 2. Sektordiagrammi loomine
fig = px.pie(
    df, 
    values="Osakaal (%)", 
    names="Asukoht", 
    title="Müük linnade lõikes",
    color_discrete_sequence=px.colors.sequential.RdBu, # Kasutame kena värvipaletti
    hole=0.3 # Teeb sellest "Donut chart-i", mis on sageli loetavam
)

# 3. Seadistame sildid, et näha nii nime kui protsenti korraga
fig.update_traces(textinfo='percent+label')

# 4. Näitame diagrammi
fig.show()