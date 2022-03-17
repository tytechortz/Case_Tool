from pydoc import classname
from dash import dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date


# df = pd.read_csv(r'C:\Users\jswank\Desktop\File2.csv')
df = pd.read_csv('File2.csv')
# print(df)
df = df.astype('Int64')
df = df.astype('str')
df = df.sort_values(by='CreationDate_1')

df = df.iloc[-5000:]
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
# print(df)


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
                    dcc.Graph(id='histogram1')
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
            )
        ]
    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

@app.callback(
    Output('histogram1', 'figure'),
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
    
    traces = []

    traces.append(go.Histogram(
        x=df_test['create_minus_report']
    ))

    layout = go.Layout(
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        bargap=0.2
    )


    return {'data': traces, 'layout': layout}
    # data = 


# fig = px.histogram(df, x=df['create_minus_report'],
#                     title='Difference In Days Between Creation Date <br> and Report Date for Cases Reported Between 3-4-2022 and 3-11-2022',
#                     labels={'create_minus_report': 'Days', 'Count':'Count'},
#                     text_auto=True)

# fig.update_layout(bargap=0.2)

# fig.show()

if __name__ == "__main__":  
    app.run_server(port=8080, debug=True)