# Importing packages
# To clarify, it´s necesary to run the next comman if you don´t have the dash library installed in your server:
# pip install dash, with your activated virtual env, then finally you´ll import all of these libraries
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('ecommerce_data.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    [
    html.H1(children='My First App with Data, Graph, and Controls',style={'color':'rgb(95, 141, 78)'}),
    html.Br(),
    dash_table.DataTable(data=df.to_dict('records'), page_size=20),
    html.Br(),
    html.Div(
        [
            html.Label('Select your option: ',htmlFor='controls-and-radio-item'),
            dcc.RadioItems(options=['Price', 'Qualification','Discount'], value='Price', id='controls-and-radio-item'),
            html.Br(),
            
            html.Label("Select an x axis:", htmlFor='x-input',style={'margin-right':'10px'}),
            dcc.Input(
                id='x-input', # Specify the ID of the datalist
                type='text',
                list='x-list',  
                value='Brand',
                style={'font-weight': 'bold','padding':'8px'}
            ),
            html.Datalist(
                id='x-list',  # ID must match the list attribute of the input 
                children=[
                    html.Option(value='Product Name'),
                    html.Option(value='Brand'),
                    html.Option(value='Available')
                ]
            ),
            html.Br(),
            html.Br(),
            
            html.Label('Select another option: ',htmlFor='controls-and-radio-histfunc'),
            dcc.RadioItems(options=['avg', 'sum','min','max','count'], value='avg', id='controls-and-radio-histfunc'),
        ],
        style={'background-color':'rgb(64, 81, 59)','border-radius':'10px','color':'rgb(96, 153, 102)',
               'padding':'15px','font-weight': 'bold'}
        ),
    html.Br(),
    
    dcc.DatePickerRange(id='date_selector',start_date=pd.to_datetime(df['Order Date'].min()),
        end_date=pd.to_datetime(df['Order Date'].max())),
    html.Hr(style={'height':'7px','background-color':'white'}),
    dcc.Graph(figure={}, id='controls-and-graph')
],style={'background-color':'rgb(40, 84, 48)','padding':'30px','border-radius':'15px'})

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    [Input(component_id='controls-and-radio-item', component_property='value'),
    Input('x-input', 'value'),
    Input('controls-and-radio-histfunc','value'),
    Input('date_selector','start_date'),
    Input('date_selector','end_date')]
    )
def update_graph(value,sec_value,third,min_date,max_date):
    new_df = df[(df['Order Date']>=min_date) & (df['Order Date']<=max_date)]
    fig = px.histogram(new_df, x=sec_value, y=value, histfunc=third)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)