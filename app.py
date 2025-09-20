import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Load the processed sales data
df = pd.read_csv("output.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by date to ensure the line chart is chronological
df = df.sort_values("date")

# Calculate summary statistics
total_sales = df['sales'].sum()
avg_daily_sales = df['sales'].mean()
total_days = df['date'].nunique()
best_region = df.groupby('region')['sales'].sum().idxmax()
best_region_sales = df.groupby('region')['sales'].sum().max()

# Build Dash app
app = dash.Dash(__name__)

# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .summary-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
                margin: 10px;
                min-width: 200px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .summary-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            }
            .dash-table-container {
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .dash-graph {
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                background: white;
                padding: 10px;
            }
            .dash-dropdown {
                border-radius: 5px;
            }
            .dash-datepicker {
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define custom CSS styles
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🍓 Soul Foods - Pink Morsel Sales Dashboard", 
                style={
                    'textAlign': 'center', 
                    'color': '#2E86AB', 
                    'marginBottom': '30px',
                    'fontSize': '2.5rem',
                    'fontWeight': 'bold',
                    'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
                }),
        html.P("Comprehensive Sales Analytics & Insights", 
               style={'textAlign': 'center', 'color': '#666', 'fontSize': '1.2rem', 'marginBottom': '40px'})
    ]),
    
    # Summary Cards
    html.Div([
        html.Div([
            html.H3(f"${total_sales:,.0f}", style={'color': '#2E86AB', 'margin': '0', 'fontSize': '2rem'}),
            html.P("Total Sales", style={'margin': '0', 'color': '#666'})
        ], className="summary-card"),
        
        html.Div([
            html.H3(f"${avg_daily_sales:,.0f}", style={'color': '#A23B72', 'margin': '0', 'fontSize': '2rem'}),
            html.P("Average Daily Sales", style={'margin': '0', 'color': '#666'})
        ], className="summary-card"),
        
        html.Div([
            html.H3(f"{total_days}", style={'color': '#F18F01', 'margin': '0', 'fontSize': '2rem'}),
            html.P("Total Days", style={'margin': '0', 'color': '#666'})
        ], className="summary-card"),
        
        html.Div([
            html.H3(f"{best_region.title()}", style={'color': '#C73E1D', 'margin': '0', 'fontSize': '2rem'}),
            html.P(f"Best Region (${best_region_sales:,.0f})", style={'margin': '0', 'color': '#666'})
        ], className="summary-card"),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '40px', 'flexWrap': 'wrap'}),
    
    # Controls
    html.Div([
        html.Div([
            html.Label("Select Date Range:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=df['date'].min(),
                end_date=df['date'].max(),
                display_format='YYYY-MM-DD',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'marginRight': '20px'}),
        
        html.Div([
            html.Label("Filter by Region:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': 'All Regions', 'value': 'all'}] + 
                        [{'label': region.title(), 'value': region} for region in df['region'].unique()],
                value='all',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'marginRight': '20px'}),
        
        html.Div([
            html.Label("Chart Type:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Area Chart', 'value': 'area'},
                    {'label': 'Scatter Plot', 'value': 'scatter'}
                ],
                value='line',
                style={'width': '100%'}
            )
        ], style={'width': '30%'})
    ], style={'display': 'flex', 'marginBottom': '30px', 'alignItems': 'end', 'flexWrap': 'wrap'}),
    
    # Main Charts Row
    html.Div([
        # Sales Over Time Chart
        html.Div([
            dcc.Graph(id="sales-time-chart")
        ], style={'width': '70%', 'display': 'inline-block'}),
        
        # Regional Sales Pie Chart
        html.Div([
            dcc.Graph(id="regional-pie-chart")
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'marginBottom': '30px'}),
    
    # Secondary Charts Row
    html.Div([
        # Daily Sales Distribution
        html.Div([
            dcc.Graph(id="sales-distribution-chart")
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        # Regional Comparison
        html.Div([
            dcc.Graph(id="regional-comparison-chart")
        ], style={'width': '50%', 'display': 'inline-block'})
    ], style={'marginBottom': '30px'}),
    
    # Data Table
    html.Div([
        html.H3("Sales Data Table", style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#2E86AB'}),
        dash_table.DataTable(
            id='sales-table',
            columns=[
                {"name": "Date", "id": "date", "type": "datetime"},
                {"name": "Region", "id": "region"},
                {"name": "Sales ($)", "id": "sales", "type": "numeric", "format": {"specifier": ",.0f"}}
            ],
            data=df.to_dict('records'),
            sort_action="native",
            filter_action="native",
            page_action="native",
            page_current=0,
            page_size=20,
            style_cell={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif'},
            style_header={'backgroundColor': '#2E86AB', 'color': 'white', 'fontWeight': 'bold'},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f8f9fa'
                }
            ]
        )
    ], style={'marginTop': '40px'})
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f8f9fa'})

# Callback for updating charts based on filters
@app.callback(
    [Output('sales-time-chart', 'figure'),
     Output('regional-pie-chart', 'figure'),
     Output('sales-distribution-chart', 'figure'),
     Output('regional-comparison-chart', 'figure'),
     Output('sales-table', 'data')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('region-dropdown', 'value'),
     Input('chart-type-dropdown', 'value')]
)
def update_charts(start_date, end_date, selected_region, chart_type):
    # Filter data based on inputs
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['date'] >= start_date) & 
            (filtered_df['date'] <= end_date)
        ]
    
    if selected_region != 'all':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    # Sales over time chart
    if chart_type == 'line':
        time_fig = px.line(filtered_df, x='date', y='sales', color='region',
                          title='Sales Over Time by Region',
                          color_discrete_sequence=px.colors.qualitative.Set2)
    elif chart_type == 'bar':
        time_fig = px.bar(filtered_df, x='date', y='sales', color='region',
                         title='Sales Over Time by Region',
                         color_discrete_sequence=px.colors.qualitative.Set2)
    elif chart_type == 'area':
        time_fig = px.area(filtered_df, x='date', y='sales', color='region',
                          title='Sales Over Time by Region',
                          color_discrete_sequence=px.colors.qualitative.Set2)
    else:  # scatter
        time_fig = px.scatter(filtered_df, x='date', y='sales', color='region',
                             title='Sales Over Time by Region',
                             color_discrete_sequence=px.colors.qualitative.Set2)
    
    time_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        legend_title="Region",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
    )
    
    # Regional pie chart
    regional_sales = filtered_df.groupby('region')['sales'].sum().reset_index()
    pie_fig = px.pie(regional_sales, values='sales', names='region',
                     title='Sales Distribution by Region',
                     color_discrete_sequence=px.colors.qualitative.Set2)
    pie_fig.update_traces(textposition='inside', textinfo='percent+label')
    pie_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    
    # Sales distribution histogram
    dist_fig = px.histogram(filtered_df, x='sales', nbins=30,
                           title='Daily Sales Distribution',
                           color_discrete_sequence=['#2E86AB'])
    dist_fig.update_layout(
        xaxis_title="Sales ($)",
        yaxis_title="Frequency",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Regional comparison bar chart
    regional_avg = filtered_df.groupby('region')['sales'].mean().reset_index()
    comp_fig = px.bar(regional_avg, x='region', y='sales',
                     title='Average Sales by Region',
                     color='region',
                     color_discrete_sequence=px.colors.qualitative.Set2)
    comp_fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Average Sales ($)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return time_fig, pie_fig, dist_fig, comp_fig, filtered_df.to_dict('records')

if __name__ == "__main__":
    app.run(debug=True)