from flask import Flask, render_template, request
from dash import Dash, html as dhtml, dcc
import plotly.express as px
import pandas as pd

df = pd.read_csv("title.basics.tsv", sep="\t", na_values="\\N")
movies_df = df.copy()

genre_list = sorted(
    movies_df['genres']
    .dropna()
    .str.split(',')
    .explode()
    .unique()
)

server = Flask(__name__)

@server.route("/", methods=["GET", "POST"])
def index():
    search_results = []

    if request.method == "POST":
        if "title" in request.form:
            title = request.form["title"]
            filtered = movies_df[movies_df['primaryTitle'].str.contains(title, case=False, na=False)]
            search_results = (
                filtered[['primaryTitle', 'startYear', 'genres']]
                .dropna()
                .head(20)
                .values
                .tolist()
            )

        elif "genre" in request.form:
            genre = request.form["genre"]
            filtered = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)]
            search_results = (
                filtered[['primaryTitle', 'startYear', 'genres']]
                .dropna()
                .head(20)
                .values
                .tolist()
            )

    return render_template("index.html", results=search_results, genres=genre_list)

dash_app = Dash(__name__, server=server, url_base_pathname='/dash/')

genre_counts = (
    movies_df['genres']
    .dropna()
    .str.split(',')
    .explode()
    .value_counts()
    .reset_index()
)
genre_counts.columns = ['Genre', 'Count']

fig = px.bar(genre_counts, x="Genre", y="Count", title="Movie Genre Distribution")

dash_app.layout = dhtml.Div([
    dhtml.H2("IMDb Genre Chart"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    server.run(debug=True)
