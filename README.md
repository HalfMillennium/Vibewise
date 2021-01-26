# Vibewise *(Spotify Mood Matcher)*
A web app that allows users to play a subsection of a selected playlist based on their mood. This mood is determined by a descriptive sentence entered by the user.

## Current functionality:
* Prompts the user to log in using Spotify interface
* Allows user to select from personal playlists (public)
* Allows user to enter a sentence to describe their current mood
* Logs selected songs from user's playlist in browser console (in the form of track IDs)

## Getting things running
To get things running, follow these steps:
1) In `/flask` run `python vibe_engine.py` to get the Flask API running on your machine.
2) In `/core` (new command window/terminal) run `node server.js` to make the web app accessible at `localhost:8888`.
