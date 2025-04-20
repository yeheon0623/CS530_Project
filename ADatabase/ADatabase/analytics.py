from ADatabase.database import Ratings, Movies, GenomeScores, GenomeTags
from collections import defaultdict
import operator

def userAnalytics(user_id):
    user_id = int(user_id)

    ratings_col = Ratings().ratings
    movies_col = Movies().movies
    genome_scores_col = GenomeScores().genome_scores
    genome_tags_col = GenomeTags().genome_tags

    print(f"Running analytics for user {user_id}")
    
    rating_docs = list(ratings_col.find({"userId": user_id}).sort("timestamp", -1))
    print(f"Found {len(rating_docs)} ratings for user {user_id}")
    if not rating_docs:
        return {}, {}, [], []

    avg_scores = {}
    genre_count = defaultdict(int)
    latest_movies = []
    watched_ids = set()

    for i, doc in enumerate(rating_docs):
        movie_id = doc.get("movieId")
        watched_ids.add(movie_id)

        movie = movies_col.find_one({"movieId": movie_id})
        if not movie:
            continue

        title = movie.get("title", "Unknown")
        genres = movie.get("genres", "")
        genres_list = genres.split("|") if genres else []

        avg_scores[title] = float(doc["rating"])

        for genre in genres_list:
            genre_count[genre] += 1

        if i < 5:
            latest_movies.append({
                "title": title,
                "timestamp": doc["timestamp"]
            })

    # Most common genre
    if not genre_count:
        return avg_scores, dict(genre_count), latest_movies, []

    most_common_genre = max(genre_count.items(), key=lambda x: x[1])[0]

    # Recommend unwatched high-rated movies in same genre
    recommendations = []
    genre_matches = movies_col.find({"genres": {"$regex": most_common_genre, "$options": "i"}})

    for movie in genre_matches:
        mid = movie["movieId"]
        if mid in watched_ids:
            continue

        related_ratings = ratings_col.find({"movieId": mid})
        scores = [r["rating"] for r in related_ratings if isinstance(r.get("rating"), (int, float))]
        if len(scores) < 10:
            continue

        avg_rating = round(sum(scores) / len(scores), 2)

        recommendations.append({
            "title": movie.get("title", "Unknown"),
            "avg_rating": avg_rating
        })

    recommendations.sort(key=lambda x: x["avg_rating"], reverse=True)
    recommendations = recommendations[:5]

    return avg_scores, dict(genre_count), latest_movies, recommendations
