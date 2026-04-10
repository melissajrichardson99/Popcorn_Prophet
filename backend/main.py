from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import shap
import sqlite3

conn = sqlite3.connect('movies.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

model = joblib.load("../data-analysis/scikit-learn-extra-tree-model.pkl")

class Movie(BaseModel):
    budget: int
    release_month: int
    runtime: int
    popularity: float
    vote_count: int
    vote_average: float
    original_language: str
    number_of_spoken_languages: int 
    number_of_production_companies: int
    number_of_production_countries: int
    A: int
    B: int
    C: int
    D: int
    E: int
    F: int
    G: int
    H: int
    I: int
    J: int
    K: int
    L: int
    M: int
    N: int
    O: int
    P: int
    Q: int
    R: int
    S: int

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

shap_columns = ['vote_average', 'vote_count', 'runtime', 'budget', 'original_language',
               'popularity', 'number_of_production_companies',
               'number_of_production_countries', 'number_of_spoken_languages',
               'release_month', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']

original_language_dict = {
    "en": 1,
    "es": 2,
    "fr": 3,
    "hi": 4,
    "ja": 5,
    "ru": 6,
    "others": 0
}

name_original_language_dict = {
    1: "English",
    2: "Spanish",
    3: "French",
    4: "Hindi",
    5: "Japanese",
    6: "Russian",
    0: "Others"
}

month_map_dict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

genre_dict = {
    'Action': 'A',
    'Adventure': 'B',
    'Animation': 'C',
    'Comedy': 'D', 
    'Crime': 'E',
    'Documentary': 'F',
    'Drama': 'G',
    'Family': 'H',
    'Fantasy': 'I',
    'History': 'J',
    'Horror': 'K',
    'Music': 'L',
    'Mystery': 'M',
    'Romance': 'N',
    'Science Fiction': 'O',
    'TV Movie': 'P',
    'Thriller': 'Q',
    'War': 'R',
    'Western': 'S',
}

@app.get("/movies")
async def get_movies(title:str = "", last_id = None):
    title = title.strip()
    if title == "":
        return []

    if last_id:
        res = cursor.execute("SELECT * FROM movies WHERE id > ? AND title LIKE ? LIMIT 12", (last_id, '%'+title+'%'));
    else:
        res = cursor.execute("SELECT * FROM movies WHERE title LIKE ? LIMIT 12", ('%'+title+'%', ));

    return res.fetchall()

@app.get("/analytics/{movie_id}")
async def get_analytics_for_move(movie_id: int):
    exec = cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id, ))
    movie = exec.fetchone()
    explainer = shap.TreeExplainer(model)
    movie_df_row = pd.DataFrame([dict(movie)])
    movie_df_row = movie_df_row[shap_columns]
    shap_values = explainer(movie_df_row)

    ret_value = dict(movie)
    ret_value['shap_values'] = dict(zip(shap_columns, shap_values.values[0].tolist()))
    ret_value['base_value'] = explainer.expected_value.tolist()[0]

    return ret_value

@app.post("/predict")
async def predict(movie: Movie):
    movie_dict = dict(movie);
    row = {};
    for shap_column in shap_columns:
        if shap_column == 'original_language':
            row[shap_column] = original_language_dict[movie_dict[shap_column]]
        else:
            row[shap_column] = movie_dict[shap_column]

    input_df = pd.DataFrame([row])
    predictions_df = model.predict(input_df)

    budget = movie.budget;
    budget_upper_limit = budget * 4;
    budget_lower_limit = budget / 4;

    vote_average = movie.vote_average;
    vote_average_upper_limit = vote_average + 4;
    vote_average_lower_limit = vote_average - 4;

    similar_movies_q = cursor.execute(f'''SELECT * FROM movies
                                          WHERE vote_average BETWEEN {vote_average_lower_limit} AND {vote_average_upper_limit} 
                                          AND budget BETWEEN {budget_lower_limit} AND {budget_upper_limit}
                                          AND revenue > 0
                                          LIMIT 10''')

    similar_movies = similar_movies_q.fetchall()

    return {'predicted_revenue': predictions_df.tolist()[0], 'similar_movies': similar_movies}

@app.get("/exploration")
async def get_exploration(x_param: str, genres = None):
    # FIXME: SQL Injection alert !!!!!!!!!!!!
    where_clause = "";
    if (genres):
        genres = genres.split(", ")
        print(genres)
        genres = map(lambda genre: f"{genre_dict[genre]} = 1", genres)
        print(genres)
        where_clause = " WHERE " + (" OR ").join(genres)
        print(where_clause)

    pairs_q = f"SELECT {x_param} as x, revenue as y FROM MOVIES" + where_clause
    pairs_q_exec = cursor.execute(pairs_q)
    pairs = pairs_q_exec.fetchall();

    total_number_of_movies_q = "SELECT COUNT(*) FROM movies" + where_clause
    total_number_of_movies_q_exec = cursor.execute(total_number_of_movies_q)
    total_number_of_movies = total_number_of_movies_q_exec.fetchone()['COUNT(*)']

    average_revenue_q = "SELECT AVG(revenue) FROM movies" + where_clause
    average_revenue_q_exec = cursor.execute(average_revenue_q)
    average_revenue = average_revenue_q_exec.fetchone()['AVG(revenue)']

    average_budget_q = "SELECT AVG(budget) FROM movies" + where_clause
    average_budget_q_exec = cursor.execute(average_budget_q)
    average_budget = average_budget_q_exec.fetchone()['AVG(budget)']

    highest_revenue_q = "SELECT MAX(revenue) FROM movies" + where_clause
    highest_revenue_q_exec = cursor.execute(highest_revenue_q)
    highest_revenue = highest_revenue_q_exec.fetchone()['MAX(revenue)']

    return {
        "plot_dataset": pairs,
        "total_number_of_movies": total_number_of_movies,
        "average_revenue": average_revenue,
        "average_budget": average_budget,
        "highest_revenue": highest_revenue
    }

@app.get("/exploration-pie")
async def get_exploration_pie():
    exec = cursor.execute("SELECT original_language, COUNT(*) FROM movies GROUP BY original_language")
    temp = exec.fetchall()
    count_dict = dict(temp)

    sum = 0;
    for language, count in count_dict.items():
        sum += count

    for language, count in count_dict.items():
        count_dict[language] = count / sum * 100

    mapped_labels = list(map(lambda k: name_original_language_dict[k], list(count_dict.keys())))

    return {
        "labels": mapped_labels,
        "data": list(count_dict.values())
    }

@app.get("/exploration-bar")
async def get_exploration_bar(x_param: str):
    exec = cursor.execute(f"SELECT {x_param}, AVG(revenue) FROM movies GROUP BY {x_param}")
    temp = exec.fetchall()
    revenue_dict = dict(temp)

    labels = list(revenue_dict.keys())
    if (x_param == "original_language"):
        labels = list(map(lambda k: name_original_language_dict[k], labels))
    elif x_param == 'release_month':
        labels = list(map(lambda k: month_map_dict[k], labels))

    return {
        "labels": labels,
        "data": list(revenue_dict.values())
    }


