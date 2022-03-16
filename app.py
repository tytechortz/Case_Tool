from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def get_layout():
    return html.Div(
        [
            html.Div([
                html.H4('Case Tool')
            ])
        ]
    )

app = Dash(__name__)

df = pd.read_csv(r'C:\Users\jswank\Desktop\File2.csv')

df = df.astype('Int64')
df = df.astype('str')
df = df.sort_values(by='CreationDate_1')

df = df.iloc[-5000:]
print(df)

df = df.applymap(lambda x: pd.to_datetime(str(x),format='%Y%m%d', errors='coerce'))
mask = (df['SpecCollectionDate1'] >= '2022-03-04') & (df['SpecCollectionDate1'] <= '2022-03-11')
df = df.loc[mask]
print(df)
df['create_minus_report'] = df['CreationDate_1'] - df['ReportDate']
df['report_minus_collection'] = df['ReportDate'] - df['SpecCollectionDate1']




df.create_minus_report = df.create_minus_report / np.timedelta64(1, 'D')
df.report_minus_collection = df.report_minus_collection / np.timedelta64(1, 'D')

df = df[df['report_minus_collection'] >= 0]
print(df)

fig = px.histogram(df, x=df['create_minus_report'],
                    title='Difference In Days Between Creation Date <br> and Report Date for Cases Reported Between 3-4-2022 and 3-11-2022',
                    labels={'create_minus_report': 'Days', 'Count':'Count'},
                    text_auto=True)

fig.update_layout(bargap=0.2)

fig.show()

if __name__ == '__main__':  
    app.run_server(debug=True)