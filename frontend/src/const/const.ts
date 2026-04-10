export const TMDB_MOVIE_PREFIX = "https://www.themoviedb.org/movie";
export const POSTER_PREFIX = "https://image.tmdb.org/t/p/original";
const LOCAL_URL = "http://localhost:8000";
const PRODUCTION_URL = "https://popcorn-prophet.onrender.com";
// const PRODUCTION_URL = "https://camren-elliptical-amelia.ngrok-free.dev";
export let API_URL = "";

if (import.meta.env.PROD) {
  API_URL = PRODUCTION_URL;
} else {
  API_URL = LOCAL_URL;
}
