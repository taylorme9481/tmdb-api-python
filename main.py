from flask import Flask, request, render_template, url_for, json
import requests
from datetime import *
from dateutil.relativedelta import *

TMDB_API_KEY = "602ffba9442593b52d93bc5c7bea0054"
movie_genres_dict = dict()
tv_genres_dict = dict()

application = Flask(__name__)


# HOME PAGE - trending movies this week
@application.route('/movies/get-trending-week', methods=['GET'])
def getTrendingMovies():
    """
    Method that returns the JSON of trending movies in the last week.
    """

    # constructing the url
    url = "https://api.themoviedb.org/3/trending/movie/week?"
    url += f"api_key={TMDB_API_KEY}"

    requestResponse = requests.get(url)
    responseDict = requestResponse.json()

    customResponse = {"trending_movies": list()}
    LIMIT = 0
    for movieDict in responseDict['results']:
        customResponse['trending_movies'].append({
            "backdrop_path": "https://image.tmdb.org/t/p/w780" + movieDict["backdrop_path"] if movieDict[
                "backdrop_path"] else "https://www.kindpng.com/picc/m/18-189751_movie-placeholder-hd-png-download.png",
            "genres": ", ".join([movie_genres_dict[num] for num in movieDict['genre_ids']]),
            "title": movieDict['title'],
            "overview": movieDict['overview'],
            "release_date": movieDict["release_date"],
            "vote_average": calculate_stars(movieDict["vote_average"]),
            "vote_count": movieDict["vote_count"]
        })
        LIMIT += 1
        if LIMIT == 5:
            break

    return customResponse


# HOME PAGE - TV Today
@application.route('/tv/airing-today', methods=['GET'])
def getTVOnAirToday():
    """
    Method that returns shows on TV today.
    """

    url = "https://api.themoviedb.org/3/tv/airing_today?" + f"api_key={TMDB_API_KEY}&language=en-US&page=1"
    requestResponse = requests.get(url)
    responseDict = requestResponse.json()

    customResponse = {"tv_airing_today": list()}
    LIMIT = 0
    for tvDict in responseDict['results']:
        customResponse['tv_airing_today'].append({
            "backdrop_path": "https://image.tmdb.org/t/p/w780" + tvDict["backdrop_path"] if tvDict[
                "backdrop_path"] else "https://www.kindpng.com/picc/m/18-189751_movie-placeholder-hd-png-download.png",
            "genres": ", ".join([tv_genres_dict[num] for num in tvDict['genre_ids']]),
            "name": tvDict['name'],
            "overview": tvDict['overview'],
            "first_air_date": tvDict["first_air_date"],
            "vote_average": calculate_stars(tvDict["vote_average"]),
            "vote_count": tvDict["vote_count"]
        })
        LIMIT += 1
        if LIMIT == 5:
            break

    return customResponse


# SEARCH PAGE - search endpoint
@application.route('/search/<category>/<query>', methods=['GET'])
def getSearchResults(category, query):
    """
    Method that returns search query details for a query
    """

    query = query.strip()
    query = query.replace(" ", "%20")

    url = ""
    if category == "movie":
        return searchMovies(query)
    elif category == "tv":
        return searchTV(query)
    else:
        return searchMoviesAndTV(query)


@application.route('/movie/<movie_id>', methods=['GET'])
def getMovieDetails(movie_id):
    """
    return all details about the movie.
    """
    # get details endpoint
    # get credits endpoint
    # get reviews endpoint
    # get watch providers endpoint
    customResponse = dict()

    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    requestResponse = requests.get(details_url)
    responseDict = requestResponse.json()

    customResponse["backdrop_path"] = "https://image.tmdb.org/t/p/w780" + responseDict["backdrop_path"] if responseDict[
        "backdrop_path"] else "https://www.kindpng.com/picc/m/18-189751_movie-placeholder-hd-png-download.png"
    customResponse["genres"] = ", ".join([movie_genres_dict[num["id"]] for num in responseDict['genres']])
    customResponse['id'] = responseDict["id"]
    customResponse["title"] = responseDict["title"]
    customResponse['overview'] = responseDict["overview"]
    customResponse["poster_path"] = "https://image.tmdb.org/t/p/w185" + responseDict["poster_path"] if responseDict[
        "poster_path"] else "https://cinemaone.net/images/movie_placeholder.png"
    customResponse["release_date"] = responseDict["release_date"]
    customResponse["runtime"] = responseDict["runtime"]
    customResponse["spoken_languages"] = calculate_spoken_languages(responseDict["spoken_languages"])
    customResponse["vote_average"] = calculate_stars(responseDict["vote_average"]),
    customResponse["vote_count"] = responseDict["vote_count"]

    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=en-US"
    requestResponse = requests.get(credits_url)
    responseDict = requestResponse.json()

    customResponse["actors"] = list()
    LIMIT = 0
    for actor in responseDict["cast"]:
        customResponse["actors"].append({
            "name": actor["name"],
            "picture": "https://image.tmdb.org/t/p/w185" + actor["profile_path"] if actor[
                "profile_path"] else "https://i1.wp.com/roanecountytn.gov/wp-content/uploads/2019/08/Placeholder-Person-1.jpg?ssl=1",
            "character": actor["character"]
        })
        LIMIT += 1
        if LIMIT == 8:
            break

    reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={TMDB_API_KEY}&language=en-US&page=1"
    requestResponse = requests.get(reviews_url)
    responseDict = requestResponse.json()

    customResponse["reviews"] = list()
    LIMIT = 0
    for review in responseDict["results"]:
        customResponse["reviews"].append({
            "username": review["author_details"]["username"],
            "rating": calculate_stars(review["author_details"]["rating"]),
            "content": review["content"],
            "created_at": datetime.strptime(review['created_at'][:10], "%Y-%m-%d").strftime("%m/%d/%Y"),
        })

        LIMIT += 1
        if LIMIT == 5:
            break

    return customResponse


@application.route("/tv/<tv_id>", methods=['GET'])
def getTVDetails(tv_id):
    # get details endpoint
    # get credits endpoint
    # get reviews endpoint
    # get watch providers endpoint

    customResponse = dict()

    details_url = f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}&language=en-US"
    requestResponse = requests.get(details_url)
    responseDict = requestResponse.json()

    customResponse["backdrop_path"] = "https://image.tmdb.org/t/p/w780" + responseDict["backdrop_path"] if responseDict[
        "backdrop_path"] else "https://www.kindpng.com/picc/m/18-189751_movie-placeholder-hd-png-download.png"
    customResponse["genres"] = ", ".join([tv_genres_dict[num["id"]] for num in responseDict['genres']])
    customResponse['id'] = responseDict["id"]
    customResponse["title"] = responseDict["name"]
    customResponse['overview'] = responseDict["overview"]
    customResponse["poster_path"] = "https://image.tmdb.org/t/p/w185" + responseDict["poster_path"] if responseDict[
        "poster_path"] else "https://cinemaone.net/images/movie_placeholder.png"
    customResponse["release_date"] = responseDict["first_air_date"]
    customResponse["episode_run_time"] = responseDict["episode_run_time"]
    customResponse["number_of_seasons"] = responseDict["number_of_seasons"]
    customResponse["spoken_languages"] = calculate_spoken_languages(responseDict["spoken_languages"])
    customResponse["vote_average"] = calculate_stars(responseDict["vote_average"])
    customResponse["vote_count"] = responseDict["vote_count"]

    credits_url = f"https://api.themoviedb.org/3/tv/{tv_id}/credits?api_key={TMDB_API_KEY}&language=en-US"
    requestResponse = requests.get(credits_url)
    responseDict = requestResponse.json()

    customResponse["actors"] = list()
    LIMIT = 0
    for actor in responseDict["cast"]:
        customResponse["actors"].append({
            "name": actor["name"],
            "picture": "https://image.tmdb.org/t/p/w185" + actor["profile_path"] if actor[
                "profile_path"] else "https://i1.wp.com/roanecountytn.gov/wp-content/uploads/2019/08/Placeholder-Person-1.jpg?ssl=1",
            "character": actor["character"]
        })
        LIMIT += 1
        if LIMIT == 8:
            break

    reviews_url = f"https://api.themoviedb.org/3/tv/{tv_id}/reviews?api_key=97588ddc4a26e3091152aa0c9a40de22&language=en-US&page=1"
    requestResponse = requests.get(reviews_url)
    responseDict = requestResponse.json()
    customResponse["reviews"] = list()

    LIMIT = 0
    for review in responseDict["results"]:
        customResponse["reviews"].append({
            "username": review["author_details"]["username"],
            "rating": calculate_stars(review["author_details"]["rating"]),
            "content": review["content"],
            "created_at": datetime.strptime(review['created_at'][:10], "%Y-%m-%d").strftime("%m/%d/%Y"),
        })

        LIMIT += 1
        if LIMIT == 5:
            break

    return customResponse


# HELPER FUNCTIONS
def searchMovies(query):
    url = "https://api.themoviedb.org/3/search/movie?" + f"api_key={TMDB_API_KEY}&language=en-US&query={query}&page=1&include_adult=false"

    requestResponse = requests.get(url)
    responseDict = requestResponse.json()
    customResponse = {"search_results": list()}

    LIMIT = 0
    for movieDict in responseDict['results']:
        customResponse['search_results'].append({
            "poster_path": "https://image.tmdb.org/t/p/w185" + movieDict["poster_path"] if movieDict[
                "poster_path"] else "https://cinemaone.net/images/movie_placeholder.png",
            "genres": ", ".join([movie_genres_dict[num] for num in movieDict['genre_ids']]),
            "name": movieDict['title'],
            "overview": movieDict['overview'],
            "release_date": movieDict["release_date"],
            "vote_average": calculate_stars(movieDict["vote_average"]),
            "vote_count": movieDict["vote_count"],
            "id": movieDict["id"],
            "media_type": "movie"
        })
        LIMIT += 1
        if LIMIT == 10:
            break

    return customResponse


def searchTV(query):
    url = "https://api.themoviedb.org/3/search/tv?" + f"api_key={TMDB_API_KEY}&language=en-US&page=1&query={query}&include_adult=false"
    requestResponse = requests.get(url)
    responseDict = requestResponse.json()

    customResponse = {"search_results": list()}
    LIMIT = 0
    for tvDict in responseDict['results']:
        customResponse['search_results'].append({
            "poster_path": "https://image.tmdb.org/t/p/w185" + tvDict["poster_path"] if tvDict[
                "poster_path"] else "https://cinemaone.net/images/movie_placeholder.png",
            "genres": ", ".join([tv_genres_dict[num] for num in tvDict['genre_ids']]),
            "name": tvDict['name'],
            "overview": tvDict['overview'],
            "release_date": tvDict["first_air_date"],
            "vote_average": calculate_stars(tvDict["vote_average"]),
            "vote_count": tvDict["vote_count"],
            "id": tvDict["id"],
            "media_type": "tv"
        })
        LIMIT += 1
        if LIMIT == 10:
            break

    return customResponse


def searchMoviesAndTV(query):
    url = "https://api.themoviedb.org/3/search/multi?" + f"api_key={TMDB_API_KEY}&language=en-US&query={query}&page=1&include_adult=false"
    requestResponse = requests.get(url)
    responseDict = requestResponse.json()

    customResponse = {"search_results": list()}

    LIMIT = 0
    for entDict in responseDict['results']:
        if entDict["media_type"] == "movie":
            customResponse['search_results'].append({
                "poster_path": "https://image.tmdb.org/t/p/w185" + entDict["poster_path"] if entDict[
                    "poster_path"] else "https://cinemaone.net/images/movie_placeholder.png",
                "genres": ", ".join([movie_genres_dict[num] for num in entDict['genre_ids']]),
                "name": entDict['title'],
                "overview": entDict['overview'],
                "release_date": entDict["release_date"],
                "vote_average": calculate_stars(entDict["vote_average"]),
                "vote_count": entDict["vote_count"],
                "id": entDict['id'],
                "media_type": "movie"
            })
            LIMIT += 1
        elif entDict["media_type"] == "tv":
            customResponse['search_results'].append({
                "poster_path": "https://image.tmdb.org/t/p/w185" + entDict["poster_path"] if entDict[
                    "poster_path"] else "https://cinemaone.net/images/movie_placeholder.png",
                "genres": ", ".join([tv_genres_dict[num] for num in entDict['genre_ids']]),
                "name": entDict['name'],
                "overview": entDict['overview'],
                "release_date": entDict["first_air_date"],
                "vote_average": calculate_stars(entDict["vote_average"]),
                "vote_count": entDict["vote_count"],
                "id": entDict['id'],
                "media_type": "tv"
            })
            LIMIT += 1

        if LIMIT == 10:
            break

    return customResponse


def populate_genres_dict():
    # constructing the url
    global movie_genres_dict
    global tv_genres_dict

    url = "https://api.themoviedb.org/3/genre/movie/list?" + f"api_key={TMDB_API_KEY}&language=en-US"
    requestResponse = requests.get(url)
    responseDict = requestResponse.json()
    movie_genres_dict = {genre['id']: genre['name'] for genre in responseDict['genres']}

    url = "https://api.themoviedb.org/3/genre/tv/list?" + f"api_key={TMDB_API_KEY}&language=en-US"
    requestResponse = requests.get(url)
    responseDict = requestResponse.json()
    tv_genres_dict = {genre['id']: genre['name'] for genre in responseDict['genres']}


def calculate_stars(rating):
    if rating != None:
        scaled_down_rating = float(rating) / 2
        return str(scaled_down_rating)
    else:
        return rating


def calculate_spoken_languages(languages):
    return ", ".join([language["english_name"] for language in languages])


@application.route('/', methods=['GET'])
def home():
    print("Welcome!")
    home_movies = getTrendingMovies()
    home_TV = getTVOnAirToday()
    # print("home_movies:", home_movies)
    # print("home_TV:", home_TV)
    # home_movies=home_movies, home_TV=home_TV
    return application.send_static_file("hw3.html")


if __name__ == '__main__':
    populate_genres_dict()
    application.run(debug=True, port=5001)