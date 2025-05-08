// Dark Mode Toggle
document.getElementById('darkModeToggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const icon = document.querySelector('#darkModeToggle i');
    if (document.body.classList.contains('dark-mode')) {
        icon.classList.replace('fa-moon', 'fa-sun');
    } else {
        icon.classList.replace('fa-sun', 'fa-moon');
    }
});

// Search Movies
document.getElementById('searchBtn').addEventListener('click', searchMovies);
document.getElementById('searchInput').addEventListener('input', debounce(searchMovies, 300));

function debounce(func, delay) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), delay);
    };
}

function searchMovies() {
    const query = document.getElementById('searchInput').value.trim();
    if (query.length < 2) return;

    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('searchResults');
            resultsDiv.innerHTML = '';
            data.forEach(movie => {
                const movieCard = document.createElement('div');
                movieCard.className = 'movie-card';
                movieCard.textContent = movie;
                movieCard.addEventListener('click', () => getRecommendations(movie));
                resultsDiv.appendChild(movieCard);
            });
        });
}

// Get Recommendations
function getRecommendations(movie) {
    fetch(`/recommend?movie=${movie}`)
        .then(response => response.json())
        .then(data => {
            const movieList = document.getElementById('movieList');
            movieList.innerHTML = '';
            data.forEach(movie => {
                const movieCard = document.createElement('div');
                movieCard.className = 'movie-card';
                movieCard.textContent = movie;
                movieCard.addEventListener('click', () => addToWatchlist(movie));
                movieList.appendChild(movieCard);
            });
        });
}

// Watchlist
function addToWatchlist(movie) {
    let watchlist = JSON.parse(localStorage.getItem('watchlist')) || [];
    if (!watchlist.includes(movie)) {
        watchlist.push(movie);
        localStorage.setItem('watchlist', JSON.stringify(watchlist));
        updateWatchlist();
    }
}

function updateWatchlist() {
    const watchlist = JSON.parse(localStorage.getItem('watchlist')) || [];
    const watchlistUl = document.getElementById('watchlist');
    watchlistUl.innerHTML = '';
    watchlist.forEach(movie => {
        const li = document.createElement('li');
        li.textContent = movie;
        watchlistUl.appendChild(li);
    });
}

// Initialize
updateWatchlist();