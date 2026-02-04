import "../css/MovieCard.css";
import { useMovieContext } from "../contexts/MovieContext";

function MovieCard({ movie }) {
  const { addToFavorites, removeFromFavorites, isFavorite } = useMovieContext();
  const favorite = isFavorite(movie.id);

  function handleFavoriteClick(e) {
    e.preventDefault()
    if (favorite) {
      removeFromFavorites(movie.id);
      alert(`${movie.title} removed from favorites!`);  
    } else {
      addToFavorites(movie);
      alert(`${movie.title} added to favorites!`);
    }
  }
 
  return (
    <div className="movie-card">
      <div className="movie-poster">
        <img src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} alt={movie.title} />
        <div className="movie-overlay">
          <button className={`favorite-button ${favorite ? "favorited" : ""}`} onClick={handleFavoriteClick}>
            {favorite ? "♥" : "♡"}
          </button>
        </div>
      </div>
      <div className="movie-info">
        <h3>{movie.title}</h3>
        <p>{movie.release_date}</p>
      </div>
    </div>
  );
}

export default MovieCard;
