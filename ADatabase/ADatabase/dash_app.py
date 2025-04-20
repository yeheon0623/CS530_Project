import urllib.parse
from collections import Counter
from datetime import datetime

from django_plotly_dash import DjangoDash
from dash import dcc, html, Input, Output
from ADatabase.database import Ratings, Movies
import plotly.express as px

app = DjangoDash(name="useranalytics")

app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        html.Div([
            html.Div(id="output-content", style={
                "maxWidth": "800px",
                "margin": "0 auto",
                "padding": "1.5rem",
                "backgroundColor": "#2b2b2b",
                "borderRadius": "12px",
                "boxShadow": "0 4px 10px rgba(0,0,0,0.4)"
            }),
        ])
    ],
    style={
        "backgroundColor": "#1e1e1e",
        "color": "#FFFFFF",
        "padding": "2rem",
        "minHeight": "100vh"
    }
)



@app.callback(
    Output("output-content", "children"),
    Input("url", "search")
)
def load_user_data(search):
    if not search:
        return html.Div("Waiting for user ID...")

    params = urllib.parse.parse_qs(search.lstrip('?'))
    user_id = params.get("user_id", [None])[0]
    if not user_id:
        return html.Div("User ID not provided.")

    try:
        user_id = int(user_id)
        print(f"User ID received in callback: {user_id}")
    except:
        return html.Div("Invalid user ID.")

    # MongoDB collections
    ratings_col = Ratings().ratings
    movies_col = Movies().movies

    # Fetch user ratings
    ratings = list(ratings_col.find({"userId": user_id}))
    if not ratings:
        return html.Div("No ratings found for this user.")

    # --- Ratings Bar Chart ---
    rating_values = [int(r["rating"]) for r in ratings if "rating" in r]
    rating_counts = Counter(rating_values)
    sorted_ratings = sorted(rating_counts.items())
    x_vals = [str(r[0]) for r in sorted_ratings]
    y_vals = [r[1] for r in sorted_ratings]

    bar_fig = px.bar(
        x=x_vals,
        y=y_vals,
        labels={"x": "Rating Given", "y": "Number of Movies"},
        title="Rating Frequency",
        height=300
    )

    # --- Genre Pie Chart ---
    genre_counter = Counter()
    movie_titles = []
    latest_movies = []

    for r in ratings:
        movie = movies_col.find_one({"movieId": r["movieId"]})
        if movie:
            movie_titles.append((movie.get("title", "Unknown"), r.get("timestamp", 0)))
            genres = movie.get("genres", "")
            for g in genres.split('|'):
                if g != '(no genres listed)':
                    genre_counter[g] += 1

    genre_fig = px.pie(
        names=list(genre_counter.keys()),
        values=list(genre_counter.values()),
        title="Genre Distribution",
        height=300
    )

    # --- Latest 5 Movies ---
    latest_sorted = sorted(movie_titles, key=lambda x: x[1], reverse=True)[:5]
    latest_output = [
        f"{title} – {datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')}" for title, ts in latest_sorted
    ]

    # --- Recommendations ---
    watched_movie_ids = {r["movieId"] for r in ratings}
    top_genres = [g for g, _ in genre_counter.most_common(3)]
    recs = []

    for genre in top_genres:
        candidates = movies_col.find({"genres": {"$regex": f".*{genre}.*"}})
        for movie in candidates:
            if movie["movieId"] not in watched_movie_ids:
                recs.append(movie.get("title", "Unknown"))

    recs = list(dict.fromkeys(recs))[:10]  # deduplicate + limit to 10

    return html.Div([
        html.Div([
            dcc.Graph(id='rating-bar-chart', figure=bar_fig, style={'height': '300px'}),
            dcc.Graph(id='genre-pie-chart', figure=genre_fig, style={'height': '300px'}),
            html.H3(f"Latest Movies Watched by User {user_id}"),
            html.Ul([html.Li(m) for m in latest_output]),
            html.H3("Recommended Movies"),
            html.Ul([html.Li(m) for m in recs]),
        ], style={
            'maxWidth': '500px',
            'margin': '0 auto',
            'padding': '1rem',
            'backgroundColor': '#2b2b2b',
            'borderRadius': '8px'
        })
    ])
