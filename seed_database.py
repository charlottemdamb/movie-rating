
import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')
model.connect_to_db(server.app)
model.db.create_all()
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())
movies_in_db = []
for movie in movie_data:
    release_date = datetime.strptime(movie['release_date'], "%Y-%m-%d")
    movies_in_db.append(crud.create_movie(movie['title'], movie['overview'], release_date, movie['poster_path']))
model.db.session.add(movies_in_db)
model.db.session.commit()
