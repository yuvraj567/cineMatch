import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_option_menu import option_menu

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
import os

def download_file(url, filename):
    if not os.path.exists(filename):
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

# Download the file from your actual public link
download_file('https://drive.google.com/file/d/1brRGWLa0B_WYK0iEbQl0BbEoVlATsu25/view?usp=sharing', 'similarity.pkl')

# Load the similarity matrix
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)


# OMDB API Key
API_KEY = "9bd299c4"

# Page configuration
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

def fetch_movie_details(movie_name):
    """Fetch movie metadata and poster using OMDB API"""
    url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}"
    response = requests.get(url)
    data = response.json()
    if data['Response'] == 'True':
        ratings = {r['Source']: r['Value'] for r in data.get('Ratings', [])}
        return {
            'title': data.get('Title', 'N/A'),
            'poster': data.get('Poster', 'https://upload.wikimedia.org/wikipedia/commons/c/c2/No_image_poster.png?20170513175923'),
            'year': data.get('Year', 'N/A'),
            'runtime': data.get('Runtime', 'N/A'),
            'genre': data.get('Genre', 'N/A'),
            'rating': data.get('imdbRating', 'N/A'),
            'plot': data.get('Plot', 'N/A'),
            'awards': data.get('Awards', 'N/A'),
            'ratings': ratings,
            'director': data.get('Director', 'N/A'),
            'actors': data.get('Actors', 'N/A')
        }
    else:
        return {
            'title': movie_name,
            'poster': 'https://upload.wikimedia.org/wikipedia/commons/c/c2/No_image_poster.png?20170513175923',
            'year': 'N/A',
            'runtime': 'N/A',
            'genre': 'N/A',
            'rating': 'N/A',
            'plot': 'N/A',
            'awards': 'N/A',
            'ratings': {},
            'director': 'N/A',
            'actors': 'N/A'
        }

def recommend(movie):
    """Get top 5 similar movies' metadata"""
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended = []

    for i in distances[1:6]:
        movie_name = movies.iloc[i[0]].title
        recommended.append(fetch_movie_details(movie_name))

    return recommended

# Home Page
def home_page():
    st.markdown("""
    <style>
        .app-header {
            background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%);
            padding: 1.5rem 2rem;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 8px 25px rgba(110, 72, 170, 0.4);
        }

        .app-header .title {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .app-header .title .main-title {
            font-size: 2rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .app-header .title .tagline {
            font-size: 0.95rem;
            font-weight: 300;
            opacity: 0.9;
            margin-left: 2.5rem;
        }

        .app-header .nav-items {
            display: flex;
            gap: 1.2rem;
            font-size: 1.05rem;
        }

        .app-header .nav-item {
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            color: white;
        }

        .app-header .nav-item:hover {
            text-decoration: underline;
        }
                
        .recommendation-header {
            font-family: 'Arial', sans-serif;
            text-align: center;
            margin: 2rem 0;
            color: #333;
        }

        .highlight {
            color: #9d50bb;
            font-weight: bold;
        }

        /* Movie Card Container Styling */
        .movie-card {
            display: flex;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 2rem;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease-in-out;
            cursor: pointer;
        }

        /* Hover effect for card */
        .movie-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
        }

        /* Movie Poster Styling */
        .movie-poster img {
            width: 250px;
            height: 370px;
            object-fit: cover;
            border-radius: 12px 0 0 12px;
            transition: transform 0.3s ease-in-out;
        }

        .movie-card:hover .movie-poster img {
            transform: scale(1.05);
        }

        /* Movie Details Container Styling */
        .movie-details {
            padding: 1.5rem;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        /* Movie Title and Year */
        .movie-details h3 {
            font-size: 1.6rem;
            margin-bottom: 1rem;
            color: #333;
            font-weight: bold;
        }

        /* Movie Meta Information (Rating, Runtime, Genre) */
        .movie-meta {
            display: flex;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
            color: #777;
            font-size: 1rem;
        }

        .movie-meta span {
            font-weight: bold;
        }

        .movie-meta .rating {
            color: #ffb400;
        }

        .movie-meta .genre {
            color: #6c63ff;
        }

        /* Movie Plot */
        .plot {
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: 1rem;
            color: #555;
            font-style: italic;
        }

        /* Movie Credits (Director, Cast) */
        .movie-credits p {
            font-size: 1rem;
            margin: 0.3rem 0;
            color: #444;
        }

        /* Awards Section Styling */
        .awards {
            margin-top: 1rem;
            font-style: italic;
            font-size: 1rem;
            color: #9d50bb;
        }
                
        .custom-footer {
            margin-top: 7rem;
            padding: 2rem 1rem;
            background: linear-gradient(135deg, #6c63ff, #9d50bb);
            text-align: center;
            color: #ffffff;
            border-radius: 16px;
            box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.25);
            font-family: 'Poppins', sans-serif;
        }

        .custom-footer h3 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .custom-footer p {
            margin: 0.5rem 0;
            font-size: 1rem;
            letter-spacing: 0.4px;
        }

        .footer-content {
            max-width: 700px;
            margin: 0 auto;
        }

        .footer-links {
            margin: 1rem 0;
        }

        .footer-links a {
            color: #fff;
            text-decoration: none;
            margin: 0 12px;
            font-weight: 600;
            transition: color 0.3s ease;
        }

        .footer-links a:hover {
            color: #ffea00;
        }

        .footer-contact p {
            margin: 0.3rem 0;
            font-size: 0.95rem;
        }

        .copyright {
            margin-top: 1.5rem;
            font-size: 0.85rem;
            color: #ddd;
        }

        /* Responsive */
        @media (max-width: 600px) {
            .custom-footer h3 {
                font-size: 1.5rem;
            }
            .footer-links a {
                display: block;
                margin: 8px 0;
            }
        }

    </style>

    <div class="app-header">
        <div class="title">
            <div class="main-title">
                🎥 CineMatch
            </div>
            <div class="tagline">
                Your personal AI-powered movie concierge 🎬✨
            </div>
        </div>
        <div class="nav-items">
            <a href="#home-section" class="nav-item">🏠 Home</a>
            <a href="#recommendations-section" class="nav-item">📊 Recommendations</a>
            <a href="#about-section" class="nav-item">ℹ️ About</a>
            <a href="#contact-section" class="nav-item">📞 Contact</a>
        </div>
    </div>
         
    """, unsafe_allow_html=True)


    # 👉 Selectbox inside a container to keep spacing
    with st.container():
        selected_movie = st.selectbox(
            'Select a movie you love:',
            movies['title'].values,
            key="movie_select",
            help="Start typing or choose from the dropdown"
        )

    # closing div after selectbox cleanly
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

    if st.button('Get Recommendations', key="recommend_btn"):
        with st.spinner('Finding the perfect matches...'):
            recommendations = recommend(selected_movie)

            st.markdown(f"""
            <div class="recommendation-header">
                <h2>Because you liked <span class="highlight">{selected_movie}</span></h2>
                <p>Here are 5 movies you might enjoy:</p>
            </div>
            """, unsafe_allow_html=True)

            for movie in recommendations:
                st.markdown(f"""
                <div class="movie-card">
                    <div class="movie-poster">
                        <img src="{movie['poster']}" alt="{movie['title']}">
                    </div>
                    <div class="movie-details">
                        <h3>{movie['title']} ({movie['year']})</h3>
                        <div class="movie-meta">
                            <span class="rating">⭐ {movie['rating']}</span>
                            <span class="runtime">⏱️ {movie['runtime']}</span>
                            <span class="genre">🎭 {movie['genre']}</span>
                        </div>
                        <p class="plot">{movie['plot']}</p>
                        <div class="movie-credits">
                            <p><strong>Director:</strong> {movie['director']}</p>
                            <p><strong>Cast:</strong> {movie['actors']}</p>
                        </div>
                        {f"<p class='awards'>🏆 {movie['awards']}</p>" if movie['awards'] != 'N/A' else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)


def footer():
    st.markdown("""
    <div class="custom-footer">
        <p>Made with ❤️ by CineMatch Team</p>
        <div class="footer-links">
            <a href="https://github.com/yuvraj567" target="_blank">GitHub</a> |
            <a href="https://linkedin.com/in/yuvraj123" target="_blank">LinkedIn</a> |
            <a href="mailto:dummyuploadyuvraj@gmail.com">Email Us</a>
        </div>
        <p>© 2025 CineMatch. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)



import streamlit as st

import streamlit as st

def about_page():
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background-color: #f4f4f4; font-family: 'Arial', sans-serif;">
        <h1 style="font-size: 2.5rem; color: #2c3e50; margin-bottom: 1rem;">🎬 About CineMatch</h1>
        <p style="font-size: 1.2rem; max-width: 900px; margin: 0 auto; color: #555555;">
            CineMatch is a platform that marries the rich history of cinema with modern technology. Our aim is to provide
            personalized movie recommendations, combining advanced algorithms with expert curation to offer a unique
            cinematic experience for every film lover.
        </p>
    </div>

    <div style="padding: 3rem; background-color: #ffffff; text-align: center;">
        <h2 style="font-size: 2rem; color: #2c3e50; margin-bottom: 1.5rem;">🎯 Our Mission</h2>
        <p style="font-size: 1.1rem; max-width: 800px; margin: 0 auto; color: #6f6f6f;">
            At CineMatch, our mission is simple – to bring the world’s cinematic history to your fingertips. 
            We want to help you discover films that resonate with your soul, from the timeless classics to modern gems. 
            With our tailored recommendations, you’ll always find something to watch, no matter your taste.
        </p>
    </div>

    <div style="padding: 3rem; background-color: #f8f8f8; text-align: center;">
        <h2 style="font-size: 2rem; color: #2c3e50; margin-bottom: 1.5rem;">💡 Why Choose CineMatch?</h2>
        <p style="font-size: 1.1rem; max-width: 800px; margin: 0 auto; color: #6f6f6f;">
            What sets CineMatch apart is the blend of human touch and intelligent technology. Our platform leverages 
            machine learning to analyze your viewing preferences while curating film suggestions reviewed by experts, ensuring 
            that every recommendation meets the highest standards of artistic quality.
        </p>
    </div>

    <div style="padding: 3rem; background-color: #ffffff; text-align: center;">
        <h2 style="font-size: 2rem; color: #2c3e50; margin-bottom: 1.5rem;">🌍 Join Us on Our Cinematic Journey</h2>
        <p style="font-size: 1.1rem; max-width: 800px; margin: 0 auto; color: #6f6f6f;">
            Whether you're an aficionado of film history or just beginning your cinematic adventure, CineMatch welcomes 
            all movie lovers to explore, discover, and enjoy the magic of cinema. Join us today and begin your journey through 
            the vast and captivating world of film.
        </p>
    </div>
    """, unsafe_allow_html=True)

def contact_page():
    st.markdown("""
        <div style="text-align: center; padding: 3rem; background-color: #f4f4f4; font-family: 'Arial', sans-serif;">
            <h1 style="font-size: 2.5rem; color: #2c3e50; margin-bottom: 1rem;">📬 Contact Us</h1>
            <p style="font-size: 1.1rem; max-width: 800px; margin: 0 auto; color: #555555;">
                We would love to hear from you! Fill in the form below and we'll get back to you as soon as possible.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📑 Fill in the Form</h2>", unsafe_allow_html=True)
    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("📨 Send Message")

        if submitted:
            if name and email and message:
                st.success(f"✅ Thank you {name}! Your message has been received.")
            else:
                st.error("⚠️ Please fill in all fields.")

    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background-color: #f4f4f4;">
            <h3 style="font-size: 1.5rem; color: #2c3e50;">🌍 Our Office Location</h3>
            <p style="font-size: 1.1rem; color: #6f6f6f;">Salt lake Sector V, 700156</p>
        </div>
        <div style="padding: 2rem; background-color: #2c3e50; color: white; text-align: center;">
            <p style="font-size: 1.1rem; font-style: italic; color: #bdc3c7;">
                "The best way to predict the future is to create it." – Peter Drucker
            </p>
        </div>
    """, unsafe_allow_html=True)


# Main App
def main():
    # Navigation menu
    with st.sidebar:
        st.image("https://img.freepik.com/premium-vector/its-movie-time-poster-design_639669-47.jpg", use_container_width=True)
        selected = option_menu(
            menu_title=None,
            options=["Home", "About", "Contact"],
            icons=["house", "info-circle", "envelope"],
            default_index=0,
            styles={
                "container": {"padding": "0!important"},
                "icon": {"color": "orange", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#ff4b4b"},
            }
        )
    
    # Page selection
    if selected == "Home":
        home_page()
        footer()
    elif selected == "About":
        about_page()
    elif selected == "Contact":
        contact_page()

if __name__ == "__main__":
    main()







