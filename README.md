# Vibewise *(Spotify Mood Matcher)*
A web app that allows users to play a subsection of a selected playlist based on their mood. This mood is determined by a descriptive sentence entered by the user.

Available at: https://vibewise.herokuapp.com/

## Current functionality:
* Prompts the user to log in using Spotify interface
* Allows user to select from personal playlists (public)
* Allows user to enter a sentence to describe their current mood
* Logs selected songs from user's playlist in browser console (in the form of track IDs)
* Queues song IDs onto user's currently playing device
* Displays confirmation page if request was successful

## Future functionality:
* In future builds, an interactive player will replace the current confirmation page
* Improving conversion between IBM Watson tone assessment and current mood model
* Automatically queue songs from all public playlists with the option of focusing on one
* _Vibe Radio_ - Play songs from your library that match the mood of a single song (or a group of songs)

## Getting things running (locally)
To get things running, follow these steps:
1) Retrieve valid client ID and secret from Spotify API as well as IBM Watson Tone Analyzer keys. Place these next to appropriate variable name within a .env file.
2) Prepare code for local deployment (replace instances of Heroku urls with local ones)
3) In `/core` run `npm start` to initialize the NodeJS and Flask servers. The web app will be accessible at `localhost:8888`.
