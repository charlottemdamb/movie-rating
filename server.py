"""Server for movie ratings app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route ("/")        
def homepage():
    """Homepage.html"""
    # if 'email' not in session:
    user = session.get('email', None)
    if user == None:
        return render_template("homepage.html")
    else:
        return redirect("/dashboard")


@app.route ("/dashboard")        
def dashboard():
    """Dashboard.html"""
    movies = crud.get_movies()

    return render_template("dashboard.html",movies=movies)

@app.route ("/rating", methods=['POST'])        
def rate_movie():
    """Dashboard.html"""
    user = crud.get_user_by_email(session['email'])
    movie = crud.get_movie_by_title(request.form.get('movie'))
    print(f"######### Movie: {movie}")
    score = request.form.get('score')
    new_rating = crud.create_rating(movie=movie, user=user, score=int(score)) 
    db.session.add(new_rating)
    db.session.commit()
    print(f'########## {new_rating.movie}')
    flash("Rating successfully added")

    return redirect("/dashboard")


@app.route("/movies")
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template("movies.html", movies=movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    movie= crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)

@app.route("/users", methods=["GET"])
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("users.html", users=users)

@app.route("/users", methods= ["POST"])
def register_users():
    """View all users."""
    email = request.form.get('email')
    password = request.form.get('password')

    user_email = crud.get_user_by_email(email)
    
    if user_email:
       flash('Try again with a new email.')
       
    else:
       user = crud.create_user(email, password)
       db.session.add(user)
       db.session.commit()
       flash('Your account was created successfully! You can now log in.')

    return redirect("/")

@app.route("/login", methods= ["POST"])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if password == user.password: 
        flash('Success!')
        session['email'] = user.email
        return redirect("/dashboard")
    else:
        flash('Incorrect email or password')
        return redirect('/')

@app.route('/users/<user_id>')
def show_user_profile(user_id):
    user= crud.get_user_by_id(user_id)

    return render_template('user_profile.html', user=user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", port=4008, debug=True)
