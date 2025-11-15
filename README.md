# Music & Movie Recommender System
A web-based recommender system that suggests music and movies based on user genre preferences. Built with Python Flask backend and integrates with TMDB API for real-time movie data.
Features

Music Recommendations: Get popular songs based on selected genre (Pop, Rock, Hip-Hop, Classical, Jazz, R&B, Electronic)
Movie Recommendations: Fetch real-time movie suggestions from TMDB API based on genre (Action, Comedy, Drama, Horror, Romance, Sci-Fi, Thriller)
User-Friendly Interface: Clean and responsive web UI built with HTML, CSS, and JavaScript
Real-time Data: Movie data fetched live from TMDB API
Genre-Based Filtering: Select preferred genre to get customized recommendations

Technology Stack

Backend: Python 3.x with Flask framework
Frontend: HTML5, CSS3, JavaScript (Vanilla)
APIs: TMDB API for movie data
Database: Mock data for music recommendations
Deployment: Flask development server
Python 3.7 or higher
pip (Python package manager)
TMDB API key (free account from https://www.themoviedb.org)
Spotify API credentials (optional, currently using mock data)

# Installation
# Step 1: Clone the Repository
git clone https://github.com/yourusername/recommender-system.git
cd recommender_system
# Step 2: Create Virtual Environment
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
# Step 3: Install Dependencies
pip install flask requests python-dotenv
# Step 4: Configure API Keys
Create a .env file in the root directory and add your API keys:
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
TMDB_API_KEY=your_tmdb_api_key
How to get API keys:

TMDB API Key: Register at https://www.themoviedb.org/settings/api
Spotify Credentials: Register at https://developer.spotify.com/dashboard
# Step 5: Run the Application
python app.py
The application will start at http://127.0.0.1:5000
# Music Recommendations
1. Displays: Song name, Artist, Album, Spotify link
2. Genres: Pop, Rock, Hip-Hop, Classical, Jazz, R&B, Electronic
# Movie Recommendations
1. Displays: Movie title, Description, Rating, Release date, Poster image
2. Genres: Action, Comedy, Drama, Horror, Romance, Sci-Fi, Thriller
# Features Explained
Music Recommendations
Uses curated mock data of popular songs
Returns 5 songs per genre
Includes artist name, album, and Spotify links
# Movie Recommendations
Integrates with TMDB API for real-time data
Fetches movies by genre with popularity sorting
Displays movie posters, ratings, and descriptions
Returns 5 movies per request
# How It Works
1. User selects category (Music/Movie) and genre
2. Frontend sends POST request to /api/recommend endpoint
3. Backend processes request:
For Music: Returns curated data from mock dataset
For Movie: Fetches data from TMDB API in real-time
4. Backend returns JSON response with recommendations
5. Frontend displays recommendations in user-friendly format
# Future Enhancements
Implement user authentication and personalized recommendations
Add machine learning-based collaborative filtering
Integrate Spotify API for real music data
Add user ratings and review system
Implement recommendation caching
Add more genres and categories
Deploy to cloud platform (Heroku, AWS)
# Troubleshooting
Issue: API keys not loading
Solution: Ensure .env file is in the root directory and properly formatted
Issue: 404 Error on recommendations
Solution: Check API key validity and ensure TMDB account is active
Issue: Port 5000 already in use
Solution: Change port in app.py - modify app.run(port=5001)
# Dependencies
flask==2.3.0 - Web framework
requests==2.31.0 - HTTP library
python-dotenv==1.0.0 - Environment variable management
# License
This project is open source and available under the MIT License.
# Author
[Anisur Rahaman Maruf] - University Project
# Acknowledgments
TMDB API for providing movie data
Flask framework documentation
Bootstrap for UI inspiration
# Note: This is a university project demonstrating web development concepts including API integration, backend development, and frontend design.

























