import csv
import pandas as pd
import sqlite3

# model = load_model('../data-analysis/et_movie_revenue')
# movies = movies.rename(columns={'prediction_label': 'predicted_revenue'})
movies = pd.read_csv("../data-analysis/movies_trained.csv")

conn = sqlite3.connect('movies.db');
print("Connecting to database")
cursor = conn.cursor();

cursor.execute("DROP TABLE IF EXISTS \"movies\"")

cursor.execute("""CREATE TABLE "movies" (
	"id"	INTEGER,
	"title"	TEXT,
	"vote_average"	REAL,
	"vote_count"	INTEGER,
	"status"	TEXT,
	"release_date"	TEXT,
	"revenue"	INTEGER,
	"runtime"	INTEGER,
	"adult"	TEXT,
	"backdrop_path"	TEXT,
	"budget"	INTEGER,
	"homepage"	TEXT,
	"imdb_id"	TEXT,
	"original_language"	INTEGER,
	"original_title"	TEXT,
	"overview"	TEXT,
	"popularity"	REAL,
	"poster_path"	TEXT,
	"tagline"	TEXT,
	"genres"	TEXT,
	"production_companies"	TEXT,
	"production_countries"	TEXT,
	"spoken_languages"	TEXT,
	"keywords"	TEXT, 
    "release_month" INTEGER,
    "number_of_production_companies" INTEGER, 
    "number_of_production_countries" INTEGER, 
    "number_of_spoken_languages" INTEGER, 
    "A" REAL,
    "B" REAL,
    "C" REAL,
    "D" REAL,
    "E" REAL,
    "F" REAL,
    "G" REAL,
    "H" REAL,
    "I" REAL,
    "J" REAL,
    "K" REAL,
    "L" REAL,
    "M" REAL,
    "N" REAL,
    "O" REAL,
    "P" REAL,
    "Q" REAL,
    "R" REAL,
    "S" REAL,
    "predicted_revenue" REAL,
	PRIMARY KEY("id")
) """)
print("\"movies\" table created")

cursor.execute("DROP TABLE IF EXISTS \"metrics\"")

cursor.execute("""CREATE TABLE "metrics" (
    "MAE" REAL,
    "MSE" REAL,
    "RMSE" REAL,
    "R2" REAL,
    "RMSLE" REAL,
    "MAPE" REAL
) """)
print("\"metrics\" table created")

print("Inserting data into tables...")

with open('../data-analysis/metrics.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""INSERT INTO metrics(MAE, MSE, RMSE, R2, RMSLE, MAPE) VALUES (?, ?, ?, ?, ?, ?)""", 
                          (row['MAE'], row['MSE'], row['RMSE'], row['R2'], row['RMSLE'], row['MAPE']))

try:
    movies.to_sql("movies", conn, if_exists='replace', index=False, method="multi", chunksize=10)

except Exception as e:
    print(f"Error during transaction, rolling back: {e}")

conn.close()

