from flask import Flask, render_template, request, jsonify
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# API Configuration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"
TMDB_API_URL = "https://api.themoviedb.org/3"

# Get Spotify Access Token
def get_spotify_token():
    try:
        auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
        auth_bytes = auth_str.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
        
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {"grant_type": "client_credentials"}
        
        response = requests.post(SPOTIFY_AUTH_URL, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        json_result = response.json()
        
        token = json_result.get("access_token")
        if not token:
            print("Error: No access token received from Spotify")
            return None
        return token
    except Exception as e:
        print(f"Error getting Spotify token: {str(e)}")
        return None

# Music data - Popular songs by genre
MUSIC_DATA = {
    "pop": [
        {"name": "Blinding Lights", "artist": "The Weeknd", "album": "After Hours", "url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMwbk", "image": ""},
        {"name": "Levitating", "artist": "Dua Lipa", "album": "Future Nostalgia", "url": "https://open.spotify.com/track/3AJwUDP5qsKUktXPMq4G5V", "image": ""},
        {"name": "As It Was", "artist": "Harry Styles", "album": "Harry's House", "url": "https://open.spotify.com/track/20OjkXlsK5DFua6yvchXFu", "image": ""},
        {"name": "Anti-Hero", "artist": "Taylor Swift", "album": "Midnights", "url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMwbk", "image": ""},
        {"name": "Good 4 U", "artist": "Olivia Rodrigo", "album": "SOUR", "url": "https://open.spotify.com/track/0V3wPSX9ygBnCmUychJ2N0", "image": ""}
    ],
    "rock": [
        {"name": "Bohemian Rhapsody", "artist": "Queen", "album": "A Night at the Opera", "url": "#", "image": ""},
        {"name": "Stairway to Heaven", "artist": "Led Zeppelin", "album": "Led Zeppelin IV", "url": "#", "image": ""},
        {"name": "Comfortably Numb", "artist": "Pink Floyd", "album": "The Wall", "url": "#", "image": ""},
        {"name": "Hotel California", "artist": "Eagles", "album": "Hotel California", "url": "#", "image": ""},
        {"name": "Highway to Hell", "artist": "AC/DC", "album": "Highway to Hell", "url": "#", "image": ""}
    ],
    "hip-hop": [
        {"name": "Lose Yourself", "artist": "Eminem", "album": "8 Mile", "url": "#", "image": ""},
        {"name": "One Dance", "artist": "Drake", "album": "Views", "url": "#", "image": ""},
        {"name": "HUMBLE.", "artist": "Kendrick Lamar", "album": "DAMN.", "url": "#", "image": ""},
        {"name": "Gold Digger", "artist": "Kanye West", "album": "Late Registration", "url": "#", "image": ""},
        {"name": "In Da Club", "artist": "50 Cent", "album": "Get Rich or Die Tryin'", "url": "#", "image": ""}
    ],
    "classical": [
        {"name": "Moonlight Sonata", "artist": "Ludwig van Beethoven", "album": "Piano Sonata No. 14", "url": "#", "image": ""},
        {"name": "Eine kleine Nachtmusik", "artist": "Wolfgang Amadeus Mozart", "album": "Serenades", "url": "#", "image": ""},
        {"name": "The Four Seasons", "artist": "Antonio Vivaldi", "album": "Concertos", "url": "#", "image": ""},
        {"name": "Clair de Lune", "artist": "Claude Debussy", "album": "Suite bergamasque", "url": "#", "image": ""},
        {"name": "Nocturne Op.9 No.2", "artist": "Frédéric Chopin", "album": "Nocturnes", "url": "#", "image": ""}
    ],
    "jazz": [
        {"name": "Take Five", "artist": "Dave Brubeck", "album": "Time Out", "url": "#", "image": ""},
        {"name": "Autumn Leaves", "artist": "Bill Evans", "album": "Peace Piece", "url": "#", "image": ""},
        {"name": "Fly Me to the Moon", "artist": "Frank Sinatra", "album": "It Might as Well Be Swing", "url": "#", "image": ""},
        {"name": "Kind of Blue", "artist": "Miles Davis", "album": "Kind of Blue", "url": "#", "image": ""},
        {"name": "Giant Steps", "artist": "John Coltrane", "album": "Giant Steps", "url": "#", "image": ""}
    ],
    "r&b": [
        {"name": "Blurred Lines", "artist": "Robin Thicke", "album": "Blurred Lines", "url": "#", "image": ""},
        {"name": "Redbone", "artist": "Childish Gambino", "album": "Awaken, My Love!", "url": "#", "image": ""},
        {"name": "Earn It", "artist": "The Weeknd", "album": "House of Balloons", "url": "#", "image": ""},
        {"name": "No Scrubs", "artist": "TLC", "album": "FanMail", "url": "#", "image": ""},
        {"name": "Untitled (How Does It Feel)", "artist": "D'Angelo", "album": "Voodoo", "url": "#", "image": ""}
    ],
    "electronic": [
        {"name": "Around the World", "artist": "Daft Punk", "album": "Homework", "url": "#", "image": ""},
        {"name": "Strobe", "artist": "deadmau5", "album": "For Lack of a Better Name", "url": "#", "image": ""},
        {"name": "One", "artist": "Swedish House Mafia", "album": "Until One", "url": "#", "image": ""},
        {"name": "Animals", "artist": "Martin Garrix", "album": "Animals", "url": "#", "image": ""},
        {"name": "Satisfaction", "artist": "Benny Benassi", "album": "Hypnotica", "url": "#", "image": ""}
    ]
}

# Get Spotify recommendations by genre
def get_spotify_recommendations_by_genre(genre, limit=5):
    try:
        genre_lower = genre.lower()
        
        # Use mock data instead of API
        tracks = MUSIC_DATA.get(genre_lower, [])
        
        if not tracks:
            print(f"No data for genre: {genre}")
            return []
        
        print(f"Retrieved {len(tracks[:limit])} tracks for genre: {genre} (using mock data)")
        return tracks[:limit]
    except Exception as e:
        print(f"Error getting music recommendations: {str(e)}")
        return []

# Get Movie recommendations from TMDB
def get_tmdb_recommendations_by_genre(genre, limit=5):
    try:
        genre_map = {
            "action": 28,
            "comedy": 35,
            "drama": 18,
            "horror": 27,
            "romance": 10749,
            "sci-fi": 878,
            "thriller": 53
        }
        
        genre_id = genre_map.get(genre.lower(), 28)
        
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": genre_id,
            "sort_by": "popularity.desc",
            "page": 1
        }
        
        response = requests.get(f"{TMDB_API_URL}/discover/movie", params=params, timeout=10)
        response.raise_for_status()
        results = response.json()
        
        movies = []
        if "results" in results and results["results"]:
            for item in results["results"][:limit]:
                try:
                    movie_info = {
                        "title": item.get("title", "Unknown"),
                        "overview": item.get("overview", "No overview available"),
                        "rating": round(item.get("vote_average", 0), 1),
                        "release_date": item.get("release_date", "N/A"),
                        "poster": f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item.get("poster_path") else ""
                    }
                    movies.append(movie_info)
                except Exception as e:
                    print(f"Error parsing movie: {str(e)}")
                    continue
        
        print(f"Retrieved {len(movies)} movies for genre: {genre}")
        return movies
    except Exception as e:
        print(f"Error getting TMDB recommendations: {str(e)}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/music-genres', methods=['GET'])
def get_music_genres():
    genres = ["Pop", "Rock", "Hip-Hop", "Classical", "Jazz", "R&B", "Electronic"]
    return jsonify({"genres": genres})

@app.route('/api/movie-genres', methods=['GET'])
def get_movie_genres():
    genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller"]
    return jsonify({"genres": genres})

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    category = data.get('category')
    genre = data.get('genre')
    
    print(f"Recommendation request: category={category}, genre={genre}")
    
    try:
        if category == 'music':
            recommendations = get_spotify_recommendations_by_genre(genre, limit=5)
        elif category == 'movie':
            recommendations = get_tmdb_recommendations_by_genre(genre, limit=5)
        else:
            recommendations = []
        
        return jsonify({
            'success': True,
            'category': category,
            'genre': genre,
            'recommendations': recommendations
        })
    except Exception as e:
        print(f"Error in recommend route: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print(f"Starting server...")
    print(f"Spotify Client ID: {SPOTIFY_CLIENT_ID[:10]}..." if SPOTIFY_CLIENT_ID else "Spotify Client ID: NOT SET")
    print(f"TMDB API Key: {TMDB_API_KEY[:10]}..." if TMDB_API_KEY else "TMDB API Key: NOT SET")
    app.run(debug=True, port=5000, host='127.0.0.1')
    # python app.py
    # http://127.0.0.1:5000/