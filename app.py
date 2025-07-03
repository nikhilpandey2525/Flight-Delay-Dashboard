import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data
airline_data = pd.read_csv(
    'airline_data.csv',
    encoding="ISO-8859-1",
    dtype={
        'Div1Airport': str, 'Div1TailNum': str,
        'Div2Airport': str, 'Div2TailNum': str
    }
)

# Create Dash app
app = dash.Dash(__name__)
server = app.server  # for deployment

# Layout with dark theme
app.layout = html.Div(
    children=[
        html.H1('Flight Delay Dashboard', style={
            'textAlign': 'center',
            'color': 'white',
            'font-size': 36,
            'marginTop': '20px'
        }),

        html.Div([
            html.P("Input Year:", style={'color': 'white', 'marginRight': '10px'}),
            dcc.Input(
                id='input-year',
                value='2010',
                type='number',
                style={
                    'height': '40px',
                    'font-size': 25,
                    'padding': '5px',
                    'color': 'white',
                    'backgroundColor': '#222',
                    'border': '1px solid white',
                    'borderRadius': '5px'
                }
            )
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'marginBottom': '30px',
            'gap': '10px'
        }),

        html.Div([
            html.Div(dcc.Graph(id='carrier-plot'), style={'flex': '1', 'padding': '10px'}),
            html.Div(dcc.Graph(id='weather-plot'), style={'flex': '1', 'padding': '10px'})
        ], style={'display': 'flex'}),

        html.Div([
            html.Div(dcc.Graph(id='nas-plot'), style={'flex': '1', 'padding': '10px'}),
            html.Div(dcc.Graph(id='security-plot'), style={'flex': '1', 'padding': '10px'})
        ], style={'display': 'flex'}),

        html.Div(dcc.Graph(id='late-plot'), style={
            'width': '80%',
            'margin': 'auto',
            'padding': '10px'
        })
    ],
    style={'backgroundColor': '#111111', 'padding': '20px'}  # 🖤 dark layout applied here
)

# Compute averages per delay type
def compute_info(data, entered_year):
    df = data[data['Year'] == int(entered_year)]

    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late

# Callback to update plots
@app.callback(
    [
        Output('carrier-plot', 'figure'),
        Output('weather-plot', 'figure'),
        Output('nas-plot', 'figure'),
        Output('security-plot', 'figure'),
        Output('late-plot', 'figure')
    ],
    Input('input-year', 'value')
)
def update_charts(entered_year):
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)

    def dark_fig(fig):
        fig.update_layout(
            paper_bgcolor='#111111',
            plot_bgcolor='#111111',
            font_color='white',
            title_font_color='white',
            legend_font_color='white'
        )
        return fig

    fig1 = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline',
                   title='Average Carrier Delay (min) by Airline')
    fig2 = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
                   title='Average Weather Delay (min) by Airline')
    fig3 = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline',
                   title='Average NAS Delay (min) by Airline')
    fig4 = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline',
                   title='Average Security Delay (min) by Airline')
    fig5 = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
                   title='Average Late Aircraft Delay (min) by Airline')

    return [dark_fig(fig1), dark_fig(fig2), dark_fig(fig3), dark_fig(fig4), dark_fig(fig5)]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
