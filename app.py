from pydoc import classname
from dash import dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date


# df = pd.read_csv(r'C:\Users\jswank\Desktop\File2.csv')
df = pd.read_csv('file2.csv')
# print(df)
df = df.astype('Int64')
df = df.astype('str')
df = df.sort_values(by='CreationDate_1')

# #df = df.iloc[-5000:]
# print(df)

df = df.applymap(lambda x: pd.to_datetime(str(x),format='%Y%m%d', errors='coerce'))
# mask = (df['SpecCollectionDate1'] >= '2022-03-04') & (df['SpecCollectionDate1'] <= '2022-03-11')
# df = df.loc[mask]
# print(df)
# df['create_minus_report'] = df['CreationDate_1'] - df['ReportDate']
# df['report_minus_collection'] = df['ReportDate'] - df['SpecCollectionDate1']




# df.create_minus_report = df.create_minus_report / np.timedelta64(1, 'D')
# df.report_minus_collection = df.report_minus_collection / np.timedelta64(1, 'D')

# df = df[df['report_minus_collection'] >= 0]
print(df)


def get_layout():
    return html.Div(
        [
            html.Div([
                html.H4('Case Tool')
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(id='creation-minus-report-hist')
                ],
                    className='eight columns'
                ),
                html.Div([
                    dcc.DatePickerRange(
                        id='date',
                        end_date=date(2022, 3, 11)
                    )
                ],  
                    className='four columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(id='report-minus-collection-hist')
                ],
                    className='eight columns'
                ),
                html.Div(id='counts')
                # html.Div([
                #     html.H6('Count of Records in Selected Date Range')
                # ],
                #     className='four columns'
                # ),
            ],
                className='row'
            ),
            # html.Div([
            #     html.Div([], className='one column'),
            #     html.Div([
            #         html.H6('Analysis of the 339 new death cases downloaded from CEDRS with a death date of 3-21-2022')
            #     ],
            #         className='eight columns'
            #     ),
            # ],
            #     className='row'
            # ),
        ]
    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True



@app.callback(
    Output('counts', 'children'),
    Output('creation-minus-report-hist', 'figure'),
    Output('report-minus-collection-hist', 'figure'),
    Input('date', 'end_date'),
    Input('date', 'start_date'))
def update_histogram1(end_date, start_date):
    print(end_date)
    print(start_date)
    mask = (df['ReportDate'] >= start_date) & (df['ReportDate'] <= end_date)
    df_test = df.loc[mask]

    df_test['create_minus_report'] = df_test['CreationDate_1'] - df_test['ReportDate']
    df_test['report_minus_collection'] = df_test['ReportDate'] - df_test['SpecCollectionDate1']
    print(df_test)
    df_test.create_minus_report = df_test.create_minus_report / np.timedelta64(1, 'D')
    df_test.report_minus_collection = df_test.report_minus_collection / np.timedelta64(1, 'D')
    print(df_test)
    df_test = df_test[df_test['report_minus_collection'] >= 0]
    count = len(df_test.index)
    print(count)

    
    cmrh_traces = []
    rmch_traces = []

    cmrh_traces.append(go.Histogram(
        x=df_test['create_minus_report']
    ))

    cmrh_layout = go.Layout(
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        bargap=0.2,
        xaxis={'title':'Difference in Creation and Report Dates in Days'}
    )

    rmch_traces.append(go.Histogram(
        x=df_test['report_minus_collection']
    ))

    rmch_layout = go.Layout(
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        bargap=0.2,
        xaxis={'title':'Difference in Report and Collection Dates in Days'}
    )


    return html.Div([
        html.Div([
            html.H6('Count of Records in Selected Date Range'),
            html.H6('{}'.format(count))
        ],
            className='four columns'
        ),
    ],
        className='row'
    ), {'data': cmrh_traces, 'layout': cmrh_layout}, {'data': rmch_traces, 'layout': rmch_layout}


if __name__ == "__main__":  
    app.run_server(port=8080, debug=True)