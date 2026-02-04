import MovieCard from "../components/MovieCard";
import { useEffect, useState } from "react";
import { searchMovies } from "../services/api";
import { getPopularMovies } from "../services/api";
import "../css/Home.css";

function Home() {
  const [searchTerm, setSearchTerm] = useState("");
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {

    const fetchPopularMovies = async () => {
      try {
        const popularMovies = await getPopularMovies();
        setMovies(popularMovies);
      } catch (error) {
        console.log(error);
        setError("Failed to fetch popular movies.");
      }
      finally {
        setLoading(false);
      }
    }
    ;
    fetchPopularMovies();
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchTerm.trim()) return
    if (loading) return

    setLoading(true);
    try {
      const searchResults = await searchMovies(searchTerm);
      setMovies(searchResults);
      setError(null);
    } catch (error) {
      console.log(error);
      setError("Failed to search movies.");
    }
    finally {
      setLoading(false);
    }
  };

  return (
    <div className="home">
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Search for movies..."
          className="search-input"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit" className="search-button">
          Search
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}
      

      {loading ? <div className="Loading">Loading...</div> : <div className="movies-grid">
        {movies.map((movie) => (
          <MovieCard movie={movie} key={movie.id} />
        ))}
      </div>}
       

      <div className="movies-grid">
        {movies.map(
          (movie) =>
            movie.title.toLowerCase().startsWith(searchTerm.toLowerCase()) && (
              <MovieCard movie={movie} key={movie.id} />
            ),
        )}
      </div>
    </div>
  );
}

export default Home;
