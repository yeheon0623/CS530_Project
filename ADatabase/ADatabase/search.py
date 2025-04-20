# # Database related operations, the query codes for the three tasks of this major assignment are implemented in this folder
from ADatabase.database import *
import pprint
import operator
import time

# Task 1
# Based on the user ID, search for the names and ratings of the movies watched by the user, sort them from new to old, and give the top three tags and relevance ratings of the movies
def missionOne(userId):

    ratings = Ratings()
    tags = Tags()
    genome_scores = GenomeScores()
    genome_tags = GenomeTags()
    movies = Movies()


    movieId = []
    title = []
    rating = []
    result = []
    timestamp = []
    tag = []
    tagId = []
    relevance = []

    dict_tag_relevance = {}
    list_dict_tag_relevance = []
    query1 = {"userId":userId }

    for y in ratings.ratings.find(query1):
        movieId.append(y["movieId"])
        print("执行7")
        print(y["movieId"])

    print("movieId：",movieId)

    movieId_remove_duplicate_value = list(set(movieId))
    print("movieId_remove_duplicate_value:")
    print(movieId_remove_duplicate_value)



    # arrange into dict form
    i = 0
    for x in  movieId_remove_duplicate_value:

        query2 = {"movieId": x}
        query3 = {"movieId": x,"userId": userId}

        for y in movies.movies.find(query2):
            title.append(y["title"])

        for y in ratings.ratings.find(query2):
            timestamp.append(y["timestamp"])

        for y in ratings.ratings.find(query3):
            rating.append(y["rating"])
            print(y["rating"])


        # Get tagId and relevance and sort them to get the first three. The format is as follows: {'relevance': 0.036250000000000004, 'tag': 805}
        query4 = {"movieId": x}
        for y in genome_scores.genome_scores.find(query4):
            r = y["relevance"]
            r = round(r, 4)

            query5 = {"tagId": y["tagId"]}
            for z in genome_tags.genome_tags.find(query5):

                dict_tag_relevance = {"tag":z["tag"],"relevance":r}
            list_dict_tag_relevance.append(dict_tag_relevance)
        sorted_list_dict_tag_relevance = sorted(list_dict_tag_relevance,
                                                key=operator.itemgetter('relevance'),reverse=True)  # 降序

        tag_relevance = sorted_list_dict_tag_relevance[:3]

        result.append({"timestamp": timestamp[i], "title": title[i],
                       "rating": rating[i], "tags_relevance": tag_relevance})

        i = i+1

    pprint.pprint(result)
    sorted_result = sorted(result, key=operator.itemgetter('timestamp'), reverse=True)


    # Add a sequence number to the result
    i =  1
    for x in sorted_result:
        sorted_result[i-1]["num"] = i
        i = i+1

    pprint.pprint(sorted_result)

    item1 = [{'num': 1, 'timestamp': '20180101', 'title': 'hello', 'rating': 100,
             'tags_relevance': [{'tag': 'comedy', 'relevance': 0.8}, {'tag': 'comedy', 'relevance': 0.8},
                                {'tag': 'comedy', 'relevance': 0.8}]}]
    pprint.pprint(item1)

    return sorted_result





# Task 2
# Based on the input keywords, search for movies with keywords in their titles
def missionTwo(keyword, page=0):
    from ADatabase.database import Movies
    movies_col = Movies().movies

    results = movies_col.find(
        {"title": {"$regex": keyword, "$options": "i"}},
        {"title": 1, "movieId": 1}
    ).skip(page * 20).limit(20)

    return list(results)






# Task 3
# Query the 20 most popular movies of a certain style (optional)
def missionThree(type):

    movies = Movies()
    ratings = Ratings()
    links = Links()
    tags = Tags()
    genome_scores = GenomeScores()
    genome_tags = GenomeTags()

    query1 = {"genres": type}
    query3 = {"genres": {"$regex": type,"$options":"i"}}
    query4 = {"movieId": 4}
    query5 = {"tagId": 1}
    query6 = {"movieId": 422}


    time_start = time.time()
    print("=======movies======")


    movieId = []
    title = []
    i=0

    for x in movies.movies.find(query3):
        movieId.append(x["movieId"])
        i+=1
    print(movieId)
    print(i)
    time_end1 = time.time()
    print(time_end1 - time_start)




    #Find the average_rating for each movieId in the ratings table
    print("=======ratings======")
    movieId_averagerating_list = []
    for x in movieId:
        time_start1 = time.time()
        query7 = {"movieId":x}
        rating = []
        for y in ratings.ratings.find(query7):
            rating.append(y["rating"])

        print(x)
        print(rating)

        time_end2 = time.time()
        print(time_end2 - time_start1)
        # This step takes a long time, mainly because it takes time to query data from the table. Each query takes about 9 seconds.

        # Find average_ratings
        sum = 0

        # If the rating is less than 10, it will be counted as 0
        if (len(rating) <= 10):
            average_rating = 0
        else:
            for y in rating:
                sum += y
            average_rating = sum / len(rating)



        # Keep two decimal places
        average_rating = round(average_rating, 2)
        print("average_rating = %.2f" % average_rating)



        #Get title
        for y in movies.movies.find(query7):
            title = y["title"]

        # Create a dictionary type dict
        movieId_averagerating_dict = {"movieId": x, "average_rating": average_rating, "title": title}
        movieId_averagerating_list.append(movieId_averagerating_dict)


    # Sort by average_ratings
    sorted_movieId_averageratings_list = sorted(movieId_averagerating_list,
                                                key=operator.itemgetter('average_rating'),
                                                reverse=True)

    account = len(sorted_movieId_averageratings_list)
    print("%s 类型一共有 %d 部电影"%(type,account))
    result = sorted_movieId_averageratings_list[:20]

    # Add sequence numbers 1-20 to result
    i =  1
    for x in result:
        result[i-1]["num"] = i
        i = i+1


    # Print the top 20 most popular movies
    pprint.pprint(result)

    return result

def missionFour(text, page=0):
    from ADatabase.database import Movies, GenomeTags, GenomeScores
    movies_col = Movies().movies
    genome_tags_col = GenomeTags().genome_tags
    genome_scores_col = GenomeScores().genome_scores

    start = page * 20
    end = start + 20

    # --- 1. Exact + prefix title match ---
    exact_matches = list(movies_col.find(
        {"title": {"$regex": f"^{text}$", "$options": "i"}},
        {"title": 1, "movieId": 1}
    ))

    prefix_matches = list(movies_col.find(
        {"title": {"$regex": f"^{text}", "$options": "i"}},
        {"title": 1, "movieId": 1}
    ))

    # --- 2. Full-text title match ---
    text_matches = list(movies_col.find(
        {"$text": {"$search": text}},
        {"score": {"$meta": "textScore"}, "title": 1, "movieId": 1}
    ).sort([("score", {"$meta": "textScore"})]))

    # --- 3. Genome relevance-based matches ---
    matching_tags = genome_tags_col.find({"tag": {"$regex": text, "$options": "i"}})
    tag_ids = [t["tagId"] for t in matching_tags]

    genome_matches = []
    if tag_ids:
        score_matches = genome_scores_col.find({
            "tagId": {"$in": tag_ids},
            "relevance": {"$gte": 0.6}
        })

        movie_ids = list({score["movieId"] for score in score_matches})
        genome_matches = list(movies_col.find(
            {"movieId": {"$in": movie_ids}},
            {"title": 1, "movieId": 1}
        ))

    # --- 4. Merge all results with deduplication ---
    all_ids = set()
    prioritized = []

    for group in [exact_matches, prefix_matches, text_matches, genome_matches]:
        for doc in group:
            mid = doc.get("movieId")
            if mid and mid not in all_ids:
                prioritized.append(doc)
                all_ids.add(mid)

    return prioritized[start:end]
