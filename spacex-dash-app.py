# spacex_dash_app.py
# IBM Data Science Capstone — Plotly Dash Lab
# COMPLETE, RUNNABLE SCRIPT WITH TASK COMMENTS

# -----------------------------
# Import required libraries
# -----------------------------
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# -----------------------------
# Read the SpaceX data
# -----------------------------
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# -----------------------------
# Create a Dash application
# -----------------------------
app = dash.Dash(__name__)

# -----------------------------
# App layout
# -----------------------------
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # ------------------------------------------------------------
    # TASK 1: Add a Launch Site Drop-down Input Component
    # - id = 'site-dropdown'
    # - options include 'All Sites' (value='ALL') + each launch site
    # - default value='ALL'
    # - placeholder and searchable=True
    # ------------------------------------------------------------
    dcc.Dropdown(
        id='site-dropdown',
        options=(
            [{'label': 'All Sites', 'value': 'ALL'}] +
            [{'label': s, 'value': s} for s in sorted(spacex_df['Launch Site'].unique())]
        ),
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # ------------------------------------------------------------
    # TASK 2: Pie chart for success counts
    # - If ALL sites: show total successful launches per site
    # - If a specific site: show Success vs Failure counts for that site
    # ------------------------------------------------------------
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # ------------------------------------------------------------
    # TASK 3: Add a Range Slider to Select Payload
    # - id='payload-slider'
    # - min=0, max=10000, step=1000
    # - value=[min_payload, max_payload]
    # ------------------------------------------------------------
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={0: '0', 2500: '2.5k', 5000: '5k', 7500: '7.5k', 10000: '10k'}
    ),

    html.Br(),

    # ------------------------------------------------------------
    # TASK 4: Scatter plot (payload vs class) colored by booster category
    # - id='success-payload-scatter-chart'
    # - input: site-dropdown, payload-slider
    # ------------------------------------------------------------
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# -----------------------------
# TASK 2: Callback for pie chart
# -----------------------------
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(selected_site):
    if selected_site == 'ALL':
        # Total successful launches by site
        df_success = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
            df_success,
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
    else:
        # Success vs Failure for the selected site
        df_site = spacex_df[spacex_df['Launch Site'] == selected_site].copy()
        df_site['Outcome'] = df_site['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            df_site,
            names='Outcome',
            title=f'Success vs Failure for {selected_site}'
        )
    return fig

# -----------------------------
# TASK 4: Callback for scatter plot
# -----------------------------
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    # Filter by payload range first
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    df = spacex_df[mask].copy()

    # Filter by site if needed
    if selected_site != 'ALL':
        df = df[df['Launch Site'] == selected_site]
        title = f'Payload vs. Outcome for {selected_site}'
    else:
        title = 'Payload vs. Outcome for All Sites'

    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        hover_data=['Launch Site'],
        title=title
    )
    return fig

# -----------------------------
# Run the app (Dash 3+)
# -----------------------------
if __name__ == '__main__':
    app.run()
