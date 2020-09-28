import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import sd_material_ui
from newspaper import Article
from summarizer import Summarizer
from dash.exceptions import PreventUpdate

# importing CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# instantiating dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    html.Div(html.H3("BERT Extractive Summarizer"), style={'font-weight':'bold','background-color':'darkorange', 'color':'white','text-align':'center'}),

    html.Br(),

    dbc.Row([

        dbc.Col(dbc.Input(id='url', type='url', size=30, placeholder="Type or copy/paste an URL"), width={'size':6, 'order':1, 'offset':3}),
        dbc.Col(dbc.Button("Summarize", id='button', n_clicks=1, color="primary", className="mr-1"), width={'order':2})

        ]),

    html.Br(),

    dbc.Row([

        dbc.Col(dcc.Loading(html.Div(html.Div(id="summary"), style={'font-weight':'bold'})), width={'size':6, 'offset':3})

    ], align='end')

    ],
    )


# summarize text
def summarize(url):
    from newspaper import fulltext
    import requests
    text = fulltext(requests.get(url).text)
    model = Summarizer()
    result = model(text, ratio=0.1)
    full = ''.join(result)
    return full

# callbacks
@app.callback(
    Output('summary', 'children'),
    [Input("button", "n_clicks")], state=[State('url', 'value')])
def update_table(n_click:int, url):
    if n_click>1:
        return summarize(url)
    else: PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
