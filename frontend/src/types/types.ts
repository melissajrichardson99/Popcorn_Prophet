export type Status = 'Released';

export type Movie = {
  id: number;
  adult: string; // "True" | False" -> Probably fine for now
  backdrop_path: string;
  budget: number;
  genres: string;
  homepage: string;
  imdb_id: string;
  keywords: string;
  original_language: number;
  original_title: string;
  overview: string;
  popularity: number;
  poster_path: string | null;
  production_companies: string;
  production_countries: string;
  release_date: string;
  revenue: number;
  runtime: number;
  spoken_languages: string;
  status: Status;
  tagline: string;
  vote_average: number;
  vote_count: number;
  number_of_production_companies: number;
  number_of_production_countries: number;
  number_of_spoken_languages: number;
  release_month: number;
  predicted_revenue?: number;
};

export type MovieForm = {
  budget: number;
  genres: string[];
  original_language: string;
  revenue: number;
  runtime: number;
  vote_average: number;
  vote_count: number;
  release_month: string;
  popularity: number;
  number_of_production_companies: number;
  number_of_production_countries: number;
  number_of_spoken_languages: number;
};

export type MovieBody = {
  budget: number;
  genres: string;
  original_language: string;
  revenue: number;
  runtime: number;
  vote_average: number;
  vote_count: number;
  release_month: number;
  popularity: number;
  number_of_production_companies: number;
  number_of_production_countries: number;
  number_of_spoken_languages: number;
};

export type Prediction = {
  predicted_revenue: number;
  similar_movies: Array<Movie>;
  // MAE: number,
  // MSE: number,
  // RMSE: number,
  // R2: number,
  // RMSLE: number,
  // MAPE: number,
};

let genre_options: Record<string, string> = {
  'A': 'Action',
  'B': 'Adventure',
  'C': 'Animation',
  'D': 'Comedy',
  'E': 'Crime',
  'F': 'Documentary',
  'G': 'Drama',
  'H': 'Family',
  'I': 'Fantasy',
  'J': 'History',
  'K': 'Horror',
  'L': 'Music',
  'M': 'Mystery',
  'N': 'Romance',
  'O': 'Science Fiction',
  'P': 'TV Movie',
  'Q': 'Thriller',
  'R': 'War',
  'S': 'Western',
}

export function convert_form_to_body(form: MovieForm): MovieBody {
  const ret = {
    ...form,
    vote_count: Number(form.vote_count), 
    vote_average: Number(form.vote_average), 
    budget: Number(form.budget), 
    number_of_production_countries: Number(form.number_of_production_countries),
    number_of_production_companies: Number(form.number_of_production_companies), 
    number_of_spoken_languages: Number(form.number_of_spoken_languages), 
    popularity: Number(form.popularity), 
    runtime: Number(form.runtime), 
    release_month: Number(form.release_month), 
    original_language: form.original_language,
  };

  for (const genre_key of Object.keys(genre_options)){
    if (form.genres.includes(genre_key)) {
      ret[genre_key] = 1;
    } else {
      ret[genre_key] = 0;
    }
  }

  return ret;
};

export type Exploration = {
  plot_dataset: Array<{ x: number, y: number }>,
  total_number_of_movies: number;
  average_revenue: number;
  average_budget: number;
  highest_revenue: number;
}

export type Pie = {
  labels: Array<string>;
  data: Array<number>;
}

export type Bar = {
  labels: Array<string>;
  data: Array<number>;
}

export type MovieAnalytics = {
  id: number;
  adult: string; // "True" | False" -> Probably fine for now
  backdrop_path: string;
  budget: number;
  genres: string;
  homepage: string;
  imdb_id: string;
  keywords: string;
  original_language: number;
  original_title: string;
  overview: string;
  popularity: number;
  poster_path: string | null;
  production_companies: string;
  production_countries: string;
  release_date: string;
  revenue: number;
  runtime: number;
  spoken_languages: string;
  status: Status;
  tagline: string;
  vote_average: number;
  vote_count: number;
  number_of_production_companies: number;
  number_of_production_countries: number;
  number_of_spoken_languages: number;
  release_month: number;
  predicted_revenue?: number;
  shap_values: {[shap_key: string]: number}
  base_value: number;
};
