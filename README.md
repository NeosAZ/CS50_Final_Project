# Spotify_API

My App is a simple uses the spotify API to allow users to remove or move multiple songs from a play list at once. I noticed spotify by default makes it difficult to remove or move multiple songs at once which is why i made this app.

My project is built on the spotify API and flask and in order to use the API we need a client ID and client secret which is specific to each individual spotify API project. I utilize the helpers.py file to access the ID and scret stored in an .env file.

The Template folder is filled with page templates which includes the remove, move, login, and selection page.

App.py include my main functions and the endpoints for each of my actions. It also include the function on how to login with the users spotify account.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Video Demo:
https://youtu.be/vFXct-ymp2I

### Prerequisites

Need a spotify Developor account
DOTENV
VENV
FLASK
PYTHON


## Running the tests

You can select multiple songs from your playlist and try to remove the songs or move the songs to another playlist. If the songs either moves or removes then the application is successful.

### Break down into end to end tests

Select the remove action and then selet the playlist to test removing songs from your current playlist.

Select the move action and select the playlist you want to be moving your songs from. Then select the playlist you want to move your songs to and click submit. See if the songs are correctly moved and removed from the selected playlist.

### And coding style tests

Def create-spotyify_oauth: Object to store the client ID, Secret, the redirect URI, and the scope that this app can access in the spotify API

Def index: check if the user is logged in. If they are go to select_playlist route. Else bring them to index.html to log in.

Def login: redirected the user tothe spotify login and also stores that spotyify authorization

Def authorize: clears the session, get the code and then used the code to get the token_info and store it into the session and redirects tothe select_playlist method.

Def select: Displays all of the users current playlist and return the results into the edit_playlist.HTML.

Def edit: Get all the tracks within the playlis. Based on the selections from the select_playlist.html it can display the playlist we like to move the songs to. THe results then returns to select_playlist.html

## Deployment

Open a virtual environment and run flask with app.py. Log in to spotify account when prompted to

## Built With

* SPOTIFY API


## Versioning

This is version 1

## Authors

Haifeng Zheng


## License

I created this app using the Spotfy API
