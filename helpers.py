from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth
from flask import url_for
load_dotenv()

def client_id():
    return os.getenv("CLIENT_ID")

def client_secret():
    return os.getenv("CLIENT_SECRET")

def secret_key():
    return os.getenv("secret_key")
