from django.shortcuts import render
import json
from ADatabase.search import missionOne,missionTwo,missionThree, missionFour



# Home page
def homePage(request):
    return render(request, 'index.html')

# Query one
from django.shortcuts import render

def query1(request):
    if request.method == "POST" and "UserID" in request.POST:
        return render(request, "index.html", {"show_dash": True})
    return render(request, "index.html", {"show_dash": False})


#Query 2
def query2(request):
    from ADatabase.database import Links
    keyword = request.POST.get('KeyWord')
    mode = request.POST.get('mode', 'basic')
    page = int(request.POST.get('page', 0))
    result = {}
    template = 'result2.html'

    if keyword:
        if mode == "fts":
            raw_data = missionFour(keyword, page)
        else:
            raw_data = missionTwo(keyword, page)

        links_col = Links().links
        formatted = []
        for i, doc in enumerate(raw_data):
            movie_id = doc.get("movieId")
            link = links_col.find_one({"movieId": movie_id}) if movie_id else {}
            imdb_id = link.get("imdbId")
            tmdb_id = link.get("tmdbId")
            formatted.append({
                "num": i + 1 + (page * 20),
                "title": doc.get("title", "Unknown"),
                "imdb": f"https://www.imdb.com/title/tt{str(imdb_id).zfill(7)}" if imdb_id else None,
                "tmdb": f"https://www.themoviedb.org/movie/{tmdb_id}" if tmdb_id else None
            })

        result['data'] = formatted
        result['page'] = page
        result['pages'] = list(range(10))  # Show first 10 pages (can be dynamic later)

    return render(request, template, result)



# Query three
def query3(request):
    Style = request.POST.get('Style')
    result = {}
    template = 'result3.html'

    if Style is not None:
        #Query database
        result['data'] = missionThree(Style)

    return render(request, template, result)