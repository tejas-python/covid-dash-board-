import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
from plotly.validator_cache import ValidatorCache


df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/main/data/time-series-19-covid-combined.csv')
df['Date'] = pd.to_datetime(df['Date'])
# print(df.info())
df.drop(columns='Province/State',inplace=True)
g = df.groupby('Country/Region')
india = pd.read_csv('https://data.covid19india.org/csv/latest/case_time_series.csv')
india['Date'] = pd.to_datetime(india['Date'])
country = []
for con in g.groups.keys():
    country.append({'label':str(con),'value':con})




states  = pd.read_csv('https://data.covid19india.org/csv/latest/state_wise_daily.csv')
states['Date'] = pd.to_datetime(states['Date'])
states.drop('TT',axis=1,inplace=True)
states_con = states[states['Status']=='Confirmed']

states_death = states[states['Status']=='Deceased']

states_recoverd = states[states['Status']=='Recovered']
state = []
for con in states.loc[:,'AN':]:

    state.append({'label':str(con),'value':con})















dis   = pd.read_csv('https://data.covid19india.org/csv/latest/district_wise.csv')
dis['Confirmed'] = abs(dis['Confirmed'])
dis['Recovered'] = abs(dis['Recovered'])
dis['Deceased'] = abs(dis['Deceased'])
dis['Active'] = abs(dis['Active'])
dis_g = dis.groupby('State')
states_d = []
for con in dis_g.groups.keys():
    states_d.append({'label':str(con),'value':con})
# print(states_d)







app = dash.Dash()

app.layout = html.Div(style={'backgroundColor': 'white'},children=[html.H1('Welcome to covid dash board',style={'color':'green','textAlign':'center','fontSize': 40}),
dcc.Dropdown(id='country-picker',options=country,value='India',style={'width':'50%'}) ,
dcc.Graph(id='country_wise'),
html.Hr(),
dcc.RadioItems(id='bar-line',options=['Bar','line'],value='Bar',style={'width':'50%','textAlign':'right'})
,dcc.Graph(id='india'),
html.Hr(),
dcc.Dropdown(id='in-state',options=state,value= 'AN',style={'width':'50%'}),
dcc.RadioItems(id='bar-lines',options=['Bar-chart','line-chart'],value='Bar-chart',style={'width':'50%','textAlign':'right'})

,dcc.Graph(id='state-graph'),
html.Hr(),
dcc.Dropdown(id='district_wise',options=states_d,value= 'Kerala',style={'width':'50%'}),
dcc.Graph(id='District-graph')

]

)

@app.callback(Output('District-graph','figure'),
[Input('district_wise','value')])
def select2(state):
    data = [go.Bar(x=dis_g.get_group(state)['District'],y=dis_g.get_group(state)['Confirmed'],name='confirmed',marker=dict(color='orange')),
            go.Bar(x=dis_g.get_group(state)['District'],y=dis_g.get_group(state)['Deceased'],name='Deceased',marker=dict(color='red')),
            go.Bar(x=dis_g.get_group(state)['District'],y=dis_g.get_group(state)['Recovered'],name='Recovered',marker=dict(color='green')),
            go.Bar(x=dis_g.get_group(state)['District'],y=dis_g.get_group(state)['Active'],name='Active',marker=dict(color='yellow'))]

    layout = go.Layout(title='COVID -19 District  wise  bar plot',
        #paper_bgcolor='rgba(0,0,0,0)',
        xaxis={'title': 'Total values'},
        yaxis={'title': 'Count'},
        hovermode='closest')

    return  {'data':data,'layout':layout}




@app.callback(Output('state-graph','figure'),
[Input('bar-lines','value'),
Input('in-state','value')])
def select1(charts,state):
    #print(chart)
    if charts == 'line-chart':
        return {'data':[go.Scatter(x=states_con.Date,y=states_con[state],mode='lines',opacity=0.7,marker={'size': 15,'color':'orange'},name='Daily Confirmed'),
                    go.Scatter(x=states_con.Date,y=states_death[state],mode='lines',opacity=0.7,marker={'size': 15,'color':'red'},name='Daily Deceased'),
                    go.Scatter(x=states_con.Date,y=states_recoverd[state],mode='lines',opacity=0.7,marker={'size': 15,'color':'green'},name='Daily Recovered')],
                    'layout':go.Layout(title='COVID -19 INDIA Line chart',
                    #paper_bgcolor='rgba(0,0,0,0)',
                    xaxis={'title': 'DATE ','type': 'date'},
                    yaxis={'title': 'COVID CASES'},

                    hovermode='closest')}
    if charts == 'Bar-chart':
        return {'data':[go.Bar(x=states_con.Date,y=states_con[state],opacity=0.7,marker={'color':'orange'},name='Daily Confirmed'),
                    go.Bar(x=states_con.Date,y=states_death[state],opacity=0.7,marker={'color':'red'},name='Daily Deceased'),
                    go.Bar(x=states_con.Date,y=states_recoverd[state],opacity=0.7,marker={'color':'green'},name='Daily Recovered')],
                    'layout':go.Layout(title='COVID -19 INDIA Bar chart',
                    #paper_bgcolor='rgba(0,0,0,0)',
                    xaxis={'title': 'DATE ','type': 'date'},
                    yaxis={'title': 'COVID CASES'},
                    hovermode='closest')}























@app.callback(Output('india','figure'),
[Input('bar-line','value')])
def select(chart):
    #print(chart)
    if chart == 'line':
        return {'data':[go.Scatter(x=india.Date,y=india['Daily Confirmed'],mode='lines',opacity=0.7,marker={'size': 15,'color':'orange'},name='Daily Confirmed'),
                    go.Scatter(x=india.Date,y=india['Daily Deceased'],mode='lines',opacity=0.7,marker={'size': 15,'color':'red'},name='Daily Deceased'),
                    go.Scatter(x=india.Date,y=india['Daily Recovered'],mode='lines',opacity=0.7,marker={'size': 15,'color':'green'},name='Daily Recovered')],
                    'layout':go.Layout(title='COVID -19 INDIA Line chart',
                    #paper_bgcolor='rgba(0,0,0,0)',
                    xaxis={'title': 'DATE ','type': 'date'},
                    yaxis={'title': 'COVID CASES'},

                    hovermode='closest')}
    if chart == 'Bar':
        return {'data':[go.Bar(x=india.Date,y=india['Daily Confirmed'],opacity=0.7,marker={'color':'orange'},name='Daily Confirmed'),
                    go.Bar(x=india.Date,y=india['Daily Deceased'],opacity=0.7,marker={'color':'red'},name='Daily Deceased'),
                    go.Bar(x=india.Date,y=india['Daily Recovered'],opacity=0.7,marker={'color':'green'},name='Daily Recovered')],
                    'layout':go.Layout(title='COVID -19 INDIA Bar chart',
                    #paper_bgcolor='rgba(0,0,0,0)',
                    xaxis={'title': 'DATE ','type': 'date'},
                    yaxis={'title': 'COVID CASES'},
                    hovermode='closest')}






@app.callback(Output('country_wise','figure'),
[Input('country-picker','value')])
def update_country(country_val):
    # print(country_val,"name")
    date = pd.to_datetime(g.get_group(country_val)['Date'])
    # print(date)
    data = [go.Scatter(x=date,y=g.get_group(country_val)['Confirmed'],text=country_val,
    mode='lines',opacity=0.7,marker={'size': 15,'color':'orange'},name='confirmed'),go.Scatter(x=date,y=g.get_group(country_val)['Deaths'],text=country_val,
    mode='lines',opacity=0.7,marker={'size': 15,'color':'red'},name='deaths'),
    go.Scatter(x=date,y=g.get_group(country_val)['Recovered'],text=country_val,
    mode='lines',opacity=0.7,marker={'size': 15,'color':'green'},name='recoverd')
    ]
    layout = go.Layout(title='COVID -19 Country wise plot',
    #paper_bgcolor='rgba(0,0,0,0)',
    xaxis={'title': 'DATE ','type': 'date'},
    yaxis={'title': 'COVID CASES'},
    hovermode='closest')

    return  {'data':data,'layout':layout}

if __name__ =="__main__":
    app.run_server()
