from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

#dataset
df = pd.read_csv('https://raw.githubusercontent.com/rara-by/WikiTableQA/main/dataset.csv',
                 on_bad_lines='warn', index_col=0)
df['Final Year'] = df['Final Year'].astype('Int64') # NaN values cause the column to be of float type

# group the dataframe by clubs, and then region 
df_clubs = df[['Region', 'Association', 'Country', 'Player', 'Clubs']]

# split the values in the Clubs column by the delimeter ','
df_clubs['Clubs'] = df_clubs['Clubs'].str.split(',')

# Explode the Clubs column to create separate rows for each value
df_clubs = df_clubs.explode('Clubs')
df_clubs['Clubs'] = df_clubs['Clubs'].str.strip(' ')

df_club_counts = df_clubs.groupby('Clubs')['Region'].value_counts().unstack(fill_value=0)
df_club_counts = df_club_counts.astype("Int64")
df_club_counts["Total"] = df_club_counts.sum(axis=1)

# sort the clubs in alphabetical order
df_clubs_sorted = df_club_counts.sort_values(by="Total", ascending=False)

# divide the clubs into two groups for better visualization
df_clubs_group1 = df_clubs_sorted.iloc[0:28]
df_clubs_group2 = df_clubs_sorted.iloc[28:]

# Create the stacked bar chart
fig = px.bar(df_clubs_group1.iloc[:, :-1],
             title='Top 27 Clubs',
             orientation='v')

fig.update_layout(barmode='stack',
                xaxis_title="Clubs",
                yaxis_title="Player Count",)

# Create the stacked bar chart
fig1 = px.bar(df_clubs_group2.iloc[:, :-1],
             title='Bottom 27 Clubs',
             orientation='v')

fig1.update_layout(barmode='stack',
                xaxis_title="Clubs",
                yaxis_title="Player Count",)

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children="Foreign Players in the Premier League"),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig1)
]
)

if __name__== '__main__':
    app.run(debug=True)