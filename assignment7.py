import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import webbrowser
import threading


# Creating dataset
data = {"Year": [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],
    "Winner": ["Uruguay", "Italy", "Italy", "Uruguay", "West Germany", "Brazil", "Brazil", "England", "Brazil", "West Germany", "Argentina", "Italy", "Argentina", "West Germany", "Brazil", "France", "Brazil", "Italy", "Spain", "Germany", "France", "Argentina"],
    "Runner-Up": ["Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary", "Sweden", "Czechoslovakia", "West Germany", "Italy", "Netherlands", "Netherlands", "West Germany", "West Germany", "Argentina", "Italy", "Brazil", "Germany", "France", "Netherlands", "Argentina", "Croatia", "France"]
}

# use pandas df for purpose of convience
df = pd.DataFrame(data)

# germany and west germany should be the same
df.replace({"West Germany": "Germany"}, inplace=True)

# get number of wins for each country
wins = df["Winner"].value_counts().reset_index()
wins.columns = ["Country", "Wins"]



# Define dashboard application
app = Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA Soccer World Cup Dashboard", style={"textAlign": "center", "color": "blue"}),

    # choropleth map to visualize countries
    dcc.Graph(id= "choropleth"),

    # dropdown to select specific country
    html.Label("Select a country:", style= {"color": "blue"}),
    dcc.Dropdown(
        id="dropdown",
        options =[{"label": country, "value": country} for country in wins["Country"].unique()],
        value=wins["Country"].unique()[0],
        clearable= False),
    
    html.Div(id="country-wins",style={"marginTop": 20, "color":"blue"}),

    # Dropdown to select year
    html.Label("Select a Year to view winner and runner up:", style = {"color": "blue"}),
    
    dcc.Dropdown(
        id = "year-dropdown",
        options = [{"label": year, "value": year} for year in df["Year"].unique()],
        value = df["Year"].unique()[0],
        clearable = False
    ),
    html.Div(id="year-result-output", style = {"marginTop": 20, "color":"blue"})
])

# Callback to update the Choropleth map
@app.callback(
    Output("choropleth","figure"),
    Input("dropdown", "value")
)
# updaet chloropleth when needed
def update_choropleth(selected_country):
    fig = px.choropleth(
        wins,
        locations="Country",
        locationmode="country names",
        color="Wins",
        hover_name="Country",
        title="World Cup Winners by Country"
    )
    return fig

# Callback for country dropdown
@app.callback(
    Output("country-wins", "children"),
    Input("dropdown", "value"))

def display_wins(selected_country):
    temp = wins.loc[wins["Country"] == selected_country, "Wins"].values[0]
    return f"{selected_country} has won the FIFA World Cup {temp} times"

# Callback for year dropdown
@app.callback(
    Output("year-result-output","children"),
    Input("year-dropdown", "value"))

def display_year(selected_year):
    row = df[df["Year"] == selected_year].iloc[0]
    return f"In {selected_year} the winner was {row['Winner']} and the runner-up was {row['Runner-Up']}"

if __name__ == "__main__":
    threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:8050")).start()  #Open browser
    app.run_server(debug=True, use_reloader=False)
