import dash
from dash import html

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout (what shows on the webpage)
app.layout = html.Div(children=[
    html.H1("Hello, Dash!"),
    html.P("Your environment is working 🎉")
])

# Run the server
if __name__ == "__main__":
    app.run(debug=True)
