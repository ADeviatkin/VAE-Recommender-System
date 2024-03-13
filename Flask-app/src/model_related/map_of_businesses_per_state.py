import pandas as pd
import plotly.express as px
from glob import glob
import os

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

# Directories to data
folder_path = './filtered_meta_data/*'
files = glob(folder_path)

data = []

for file in files:
    print(file)
    state_name = os.path.basename(file).split('-')[1].split('.')[0].replace("_", " ")
    state_code = state_name_to_code.get(state_name, state_name)  
    with open(file, 'r') as f:
        non_empty_lines = sum(1 for line in f if line.strip())
    data.append({'state': state_code, 'count': non_empty_lines})

state_counts = pd.DataFrame(data)

fig = px.choropleth(state_counts,
                    locations='state',
                    locationmode="USA-states",
                    color='count',
                    scope="usa",
                    color_continuous_scale="algae",
                    labels={'count': 'Liczba lokali'})

fig.update_layout(
    geo=dict(showlakes=True, lakecolor="LightBlue"),
    margin={"r":0, "t":0, "l":0, "b":0},
    width=800,
    height=400
)

fig.write_image("./map_of_business_by_state.png")