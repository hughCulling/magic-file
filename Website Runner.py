#############################################
# Test site using Python and Flask
# Tutorial 6
# Retrieve data from a SQLite database and
# use it to create a dynamic web page.
# The database is created and populated in
# this program: tutorial06-credb.py
# (HTML templates are located in /templates)
#############################################

# Import Flask libraries
from flask import Flask, render_template

# Instantiate Flask application
app = Flask(__name__)

# Import SQLite libraries
import sqlite3
from sqlite3 import Error

# Query SQLite database
def retrieve_song():
    try:
        db=sqlite3.connect(dbname)
        print(sqlite3.version)
        db.row_factory=sqlite3.Row
        cursor = db.cursor()
# Create a temporary table to hold the concatenated results of the query
        cursor.execute("""drop table if exists tempSong""")
        cursor.execute("""create table tempSong (songName varchar(32), artistName varchar(32), songLink varchar(100))""")
        cursor.execute("""insert into tempSong select song.songname, group_concat(artist.artistname), song.songLink from song, songartist, artist
where song.songid = songartist.songid and artist.artistid = songartist.artistid
group by song.songname""")
        cursor.execute("""select songName, artistName, songLink from tempSong""")
        posts = [dict(row) for row in cursor.fetchall()]
        print(posts)
        return(posts)
    except Error as e:
        print(e)
    finally:
        db.close()

def retrieve_artist():
    try:
        db=sqlite3.connect(dbname)
        print(sqlite3.version)
        db.row_factory=sqlite3.Row
        cursor = db.cursor()
        cursor.execute('SELECT * FROM artist')
        posts = [dict(row) for row in cursor.fetchall()]
        print(posts)
        return(posts)
    except Error as e:
        print(e)
    finally:
        db.close()

def retrieve_single_artist(artistId):
    try:
        db=sqlite3.connect(dbname)
        print(sqlite3.version)
        db.row_factory=sqlite3.Row
        cursor = db.cursor()
        cursor.execute("""SELECT artistName, songName, releaseDate FROM artist, song, songArtist where song.songId = songArtist.songId
                       and artist.artistId = songArtist.artistId and songArtist.artistId = ?""", (artistId,))
        posts = [dict(row) for row in cursor.fetchall()]
        print(posts)
        return(posts)
    #except Error as e:#
        #print(e)#
    finally:
        db.close()



# Home page
# (http://localhost:5000 or http://localhost:5000/home)
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# Artists page
# (http://localhost:5000/artists)
@app.route("/artists")
def artist():
    posts=retrieve_artist()
    print(posts)
    return render_template("artists.html", posts=posts)

# Single artists page
# (http://localhost:5000/artist/<artistId>)
@app.route("/artist/<artistId>")
def singleartist(artistId):
    posts=retrieve_single_artist(artistId)
    print(posts)
    return render_template("single-artist.html", posts=posts)


# Songs page
# (http://localhost:5000/songs)
@app.route("/songs")
def songs():
    posts=retrieve_song()
    print(posts)
    return render_template("songs.html", posts=posts)

# Debug mode enables you to see changes to your HTML
# without having to restart the web server
print("Start program")
if __name__ == "__main__":
    dbname = "/home/pi/Desktop/Project/Magic File/sqlite.db"
    app.run(debug=True)
