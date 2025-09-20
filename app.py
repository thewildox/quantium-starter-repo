# import dash
# from dash import html

# # Initialize the Dash app
# app = dash.Dash(__name__)

# # Define the layout (what shows on the webpage)
# app.layout = html.Div(children=[
#     html.H1("Hello, Dash!"),
#     html.P("Your environment is working 🎉")
# ])

# # Run the server
# if __name__ == "__main__":
#     app.run(debug=True)

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash()

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the processed sales data
df = pd.read_csv("output.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by date to ensure the line chart is chronological
df = df.sort_values("date")

# Create a line chart
fig = px.line(
    df,
    x="date",
    y="sales",
    color="region",  # Optional: remove this if you want a single line
    title="Pink Morsel Sales Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales ($)",
    legend_title="Region"
)

# Build Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Soul Foods Sales Visualiser", style={"textAlign": "center"}),

    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )
])

if __name__ == "__main__":
    app.run(debug=True)
