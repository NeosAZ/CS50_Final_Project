from flask import Flask, flash, redirect, render_template, request, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import helpers
import time

app = Flask(__name__)

app.secret_key = helpers.secret_key()
app.config['SESSION_COOKIE_NAME'] = 'Spotify Liked Playlist Cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def index():
    try:
        token_info=get_token()
    except:
        return render_template("index.html")
    return redirect('/select_playlist')

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info

    return redirect("/select_playlist")

@app.route('/select_playlist', methods=["GET", "POST"])
def select():
    if request.method == "GET":
        try:
            token_info=get_token()
        except:
            return redirect("/")
        ##create a list with all of the playlist##
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_id = sp.current_user()["id"]
        session['result'] = []
        iter = 0
        while True:
            offset = iter * 50
            iter += 1
            user_playlist = sp.current_user_playlists(limit = 50, offset = offset)["items"]
            for item in user_playlist:
                playlist = {}
                if item["owner"]["id"] == user_id:
                    playlist["name"] = item["name"]
                    playlist["id"] = item["id"]
                    session['result'].append(playlist)
            if (len(user_playlist) < 50):
                break
        return render_template("select_playlist.html", index = session['result'])
    else:
        session['current_action'] = request.form.get("action")
        session['selected_playlist']= request.form.get("playlist")
        return  redirect('/edit_playlist')


@app.route('/edit_playlist', methods=["GET", "POST"])
def edit():
    try:
        token_info=get_token()
    except:
        return redirect("/")
        ##create a list with all the songs in the play list##
    sp = spotipy.Spotify(auth=token_info['access_token'])
    if request.method == "GET":
        playlist_tracks = []
        iter = 0
        while True:
            offset = iter * 20
            iter += 1
            if session['selected_playlist'] == "liked":
                playlist_content = sp.current_user_saved_tracks(limit = 20, offset = offset)["items"]
            else:
                playlist_content = sp.playlist_items(session['selected_playlist'], limit = 20, offset = offset)["items"]
            for idx, item in enumerate(playlist_content):
                track = {}
                track["name"] = item["track"]["name"]
                track["id"] = item["track"]["id"]
                playlist_tracks.append(track)
            if (len(playlist_content) < 20):
                break
        
        if session['current_action'] == "move":
            return render_template("edit_playlist.html", index = playlist_tracks, playlist = session['result'])
        else:
            return render_template("edit_playlist.html", index = playlist_tracks)
    else:
        ##create a list of the songs that we selected
        songs = request.form.getlist('song_name')
        ##add exception where if list is blank return something
        if session['current_action'] == "move":
            ##get the playlist we are moving to##
            ##add to that playlist##
            ##remove it from the current playlist
            to_playlist = request.form.get("moved_playlist")
            if session['selected_playlist'] == "liked":
                sp.current_user_saved_tracks_delete(tracks=songs)
                sp.playlist_add_items(to_playlist,songs)
            else:
                sp.playlist_remove_all_occurrences_of_items(session['selected_playlist'],songs)
                if to_playlist == "liked":
                    sp.current_user_saved_tracks_add(tracks=songs)
                else:
                    sp.playlist_add_items(to_playlist, songs)

        elif session['current_action'] == "remove":
            ##remove it from the current playlist
            if session['selected_playlist'] == "liked":
                sp.current_user_saved_tracks_delete(tracks=songs)
            else:
                sp.playlist_remove_all_occurrences_of_items(session['selected_playlist'],songs)
        return redirect("/select_playlist")
        


def get_token():
    token_info=session.get(TOKEN_INFO,None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id = helpers.client_id(),
            client_secret = helpers.client_secret(),
            redirect_uri = url_for('authorize', _external=True),
            scope="user-library-read playlist-read-private playlist-modify-private user-library-modify")
