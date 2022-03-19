import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
import mysql.connector as mysql

# ---------- Import and clean data (importing csv into pandas)

df = pd.read_csv("complaints.csv", sep=",")
df.shape

df1 = df[['Date received', 'Year', 'Product', 'Consumer complaint narrative', 'Company', 'State', 'Submitted via', 'Company response to consumer', 'Complaint ID']].copy()
df1 = df1[pd.notnull(df1['Consumer complaint narrative'])]
df1.columns = ['Date received', 'Year', 'Product', 'Consumer complaint narrative', 'Company', 'State', 'Submitted via', 'Company response to consumer', 'Complaint ID']
df1.shape
df2 = df1.sample(10000, random_state=1).copy()
df2.replace({'Product': 
             {'Credit reporting, credit repair services, or other personal consumer reports':'Credit card', 
              'Credit reporting': 'Credit card',
              'Credit card or prepaid card': 'Credit card',
              'Credit card': 'Credit card',
              'Prepaid card': 'Credit card',
              'Other financial service': 'Bank account or service',
              'Payday loan, title loan, or personal loan': 'Payday loan',      
              'Money transfer, virtual currency, or money service': 'Money transfer & virtual currency',
              'Consumer Loan': 'Vehicle loan or lease',
              'Bank account or service': 'Checking or savings account',
              'Money transfers': 'Money transfer & virtual currency',
              'Virtual currency': 'Money transfer & virtual currency'}}, 
              inplace= True)

#df = df.groupby(['Year', 'State'])[['Complaint ID']].count()
#df.reset_index(inplace=True)
#print(df[:5])

dff = df2.copy()
dff = dff.groupby(['State'])[['Complaint ID']].count()
dff.reset_index(inplace=True)

fig3 = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='State',
        scope="usa",
        color='Complaint ID',
        hover_data=['State', 'Complaint ID'],
        color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
    )

dff = df2.copy()
dff = dff.groupby(['Product'])[['Complaint ID']].count()
dff.reset_index(inplace=True)
fig4 = px.pie(dff, values='Complaint ID', names='Product', color_discrete_sequence=px.colors.diverging.RdYlGn)

#dff4 = df2.copy()
#dff4 = dff4.groupby(['Product', 'Year'])[['Complaint ID']].count()
#fig6 = px.imshow(dff4)

con = mysql.connect(host="localhost", user="root", password="", database="complains")
cursor = con.cursor()
cursor.execute("select complain_id, date_complain, product_category, company, state, submitted_via from complains")
table_rows = cursor.fetchall()
df20 = pd.DataFrame(table_rows, columns=cursor.column_names)
df20['Year']=pd.DatetimeIndex(df20['date_complain']).year
df20.rename(columns={'complain_id': 'Complaint ID', 'date_complain': 'Date received', 'product_category': 'Product', \
                   'company': 'Company', 'state':'State', 'submitted_via': 'Submitted via'}, inplace=True)
df20.shape

df10 = pd.read_csv("Results.csv", sep=",")
df10.shape

# Dash Configuration------------------------------------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# App layout------------------------------------------------------------------------------
app.layout = dbc.Container([
    
    dbc.Row(
        dbc.Col(html.H1("Dashboard Complaint Processing Suite",
                        className='text-center text-primary mb-4'),
                width=12)
    ),

    dbc.Row([

        dbc.Col([
            html.H3('Risk per States', style={'text-align': 'center'}),
            dcc.Graph(id='complaint_risk', figure=fig3)
        ], width={'size':5, 'offset':1, 'order':1},

         ),

        dbc.Col([
            html.H3('Risk per Product', style={'text-align': 'center'}),
            dcc.Graph(id='product_risk', figure=fig4)
        ], width={'size':5, 'offset':0, 'order':2},

         ),

    ], no_gutters=True, justify='start'),

    dbc.Row([
        dbc.Col([
            html.H3('Text Classification results', style={'text-align': 'center'}),
            html.Br(),
            dash_table.DataTable(
                    id='results_table',
                    columns=[{"name": i, "id": i} for i in df10.columns],
                    data=df10.to_dict('records'),
                    )               
        ], width={'offset':2, 'size':8},
    ),
    ], no_gutters=True, justify='start'),

    dbc.Row([
        dbc.Col([
            html.Br(),
            dcc.Dropdown(id="slct_year", value=2021, multi=False, style={'offset':1, 'width': "40%"},
                 options=[{'label': x, 'value': x} for x in 
                        df2.Year.unique()]),
            html.H3('Number of Complaints per State and Product', style={'text-align': 'center'}),
            dcc.Graph(id='complaint_map', figure={})
        ], width={'offset':1, 'size':10},
        ),

    ], no_gutters=True, justify='start'),

    dbc.Row([
        dbc.Col([
            html.H3('Number of Complaints per Product', style={'text-align': 'center'}),
            html.Div(id='output_container', children=[]),
            dcc.Graph(id='bar_chart', figure={})
        ], width={'size':5, 'offset':1, 'order':1},

         ),

        dbc.Col([
            html.Br(),
            html.H3('Complains per Company', style={'text-align': 'center'}),
            dcc.Graph(id='bar_company', figure={})
        ], width={'size':5, 'offset':0, 'order':2},

        ),
    ], no_gutters=True, justify='start'),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="slct_company", value='TRANSUNION INTERMEDIATE HOLDINGS, INC.', multi=False, style={'width': "70%"},
                 options=[{'label': x, 'value': x} for x in 
                        df2.Company.unique()]),
            html.Br(),
            html.H3('Type of response', style={'text-align': 'center'}),
            dcc.Graph(id='bar_chart2', figure={})           
    ], width={'size':6, 'offset':3},      
     ),
    ], no_gutters=True, justify='start'),

], fluid=True)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
     Output(component_id='complaint_map', component_property='figure'),
     Input(component_id='slct_year', component_property='value')
)
                           
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dff = df2.copy()
    dff = dff.groupby(['Year', 'Product', 'State'])[['Complaint ID']].count()
    dff.reset_index(inplace=True)
    dff = dff[dff["Year"] == option_slctd]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='State',
        scope="usa",
        color='Complaint ID',
        facet_col='Product', facet_col_wrap=4,
        hover_data=['State', 'Complaint ID'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Nr. Complaints': 'nr. complaints'},
    )

    return fig

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='bar_chart', component_property='figure')],
     Input(component_id='slct_year', component_property='value')
)

def update_side_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The selected year was: {}".format(option_slctd)

    dff = df20.copy()
    dff = dff.groupby(['Year', 'Product'])[['Complaint ID']].count()
    dff.reset_index(inplace=True)
    dff = dff[dff["Year"] == option_slctd]

    # Plotly Express
    fig1 = px.bar(dff, x='Product', y='Complaint ID').update_xaxes(categoryorder="total descending")
    
    return container, fig1

@app.callback(
     Output(component_id='bar_company', component_property='figure'),
     Input(component_id='slct_year', component_property='value')
)

def update_side_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dff = df20.copy()
    dff = dff.groupby(['Year', 'Company'])[['Complaint ID']].count()
    dff.reset_index(inplace=True)
    dff = dff[dff["Year"] == option_slctd]

    # Plotly Express
    fig5 = px.bar(dff, x='Company', y='Complaint ID').update_xaxes(categoryorder="total descending")
    
    return fig5

@app.callback(
     Output(component_id='bar_chart2', component_property='figure'),
     Input(component_id='slct_company', component_property='value')
)

def update_side_graph2(option_company):
    print(option_company)
    print(type(option_company))


    dff = df2.copy()
    dff = dff.groupby(['Company', 'Company response to consumer'])[['Complaint ID']].count()
    dff.reset_index(inplace=True)
    dff = dff[dff["Company"] == option_company]

    # Plotly Express
    fig2 = px.pie(dff, values='Complaint ID', names='Company response to consumer')
    return fig2

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
