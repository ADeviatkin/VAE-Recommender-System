import pandas as pd
import plotly.graph_objects as go
from glob import glob
import os
import json

# Предположим, что у вас уже есть словарь для преобразования названий штатов в коды
state_name_to_code = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia' : 'DC'
}

# Path do source data
folder_path = './filtered_meta_data/*'
files = glob(folder_path)

data = []

for file in files:
    state_name = os.path.basename(file).split('-')[1].split('.')[0].replace("_", " ")
    state_code = state_name_to_code.get(state_name, state_name)
    
    with open(file, 'r') as f:
        for line in f:
            if line.strip():
                entry = json.loads(line)
                category = entry.get('category')
                if category:
                    first_category = category[0] if category else None
                    data.append({'state': state_code, 'category': first_category})

df = pd.DataFrame(data)
df['category'] = df['category'].replace({'bar': 'Bar', 'pub': 'Pub', 'restaurant': 'Restauracja'})
pivot_df = df.pivot_table(index='state', columns='category', aggfunc='size', fill_value=0)
pivot_df['Total'] = pivot_df.sum(axis=1)
pivot_df_sorted = pivot_df.sort_values(by='Total', ascending=False)
middle_index = len(pivot_df_sorted) // 2
first_half = pivot_df_sorted[:middle_index]
second_half = pivot_df_sorted[middle_index:]
def create_fig(data, title=""):
    fig = go.Figure()
    for category in data.columns[:-1]: 
        fig.add_trace(go.Bar(x=data.index, y=data[category], name=category))
    
    fig.update_layout(
        barmode='stack',
        xaxis_title="Stan",
        yaxis_title="",
        title=title,
        legend_title="Kategoria",
        width=800,
        height=400
    )
    return fig

fig1 = create_fig(first_half)
fig2 = create_fig(second_half)

fig1.write_image("top_half_states.png")
fig2.write_image("bottom_half_states.png")