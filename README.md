## Spotify: how to retrieve your saved music, format it neatly, and keep it locally

### Intro and overview

The python scripts in this repo allow any Spotify user (with a free or paid subscription) to download the entirety of one's Spotify library ('Liked songs') from Youtube, ensuring that the info relating to those files is appropriately formatted; thus enabling the user to keep a well-organized library in iTunes.

Assuming all the external pre-requisites are installed (see below), the code in `Spotify_downloader.py` allows one to do this. Briefly, the `Spotify_downloader().get_saved_tracks_from_user()` function retrieves the list of a Spotify user's saved songs and gives each song a unique identifier. A copy of this dictionary is also saved to disk in .json format, for reference.

Next, the `Spotify_downloader().automate_download()` function passes the downloaded list of songs to the `youtube-dl` command from the eponymous [package](https://github.com/ytdl-org/youtube-dl), which enables downloading of the corresponding songs from Youtube.

The name of the files downloaded through the `youtube-dl` package is usually that of the corresponding Youtube video. Unfortunately, those names are not standardized and often lack important information to keep one's music library organized (name of the album, for instance). The `Spotify_downloader().automate_download()` function renames each downloaded file so that it includes the song's unique identifier, as defined by the `Spotify_downloader().get_saved_tracks_from_user()` function.

Finally, the `Spotify_downloader().add_id_tags()` function iterates through the list of downloaded songs and updates each file's id3 tags according to the information that was originally obtained from Spotify (specifically, name of the song, name of the artist, name of the album, and the track's number in the album) using each song's unique identifier. The files can then be imported into iTunes, thus enabling one to keep a local copy of your Spotify music.

### Prerequisites: 
* Python 3.x
* [`spotipy`](https://spotipy.readthedocs.io/en/2.9.0/)
* [`ffmpeg-python`](https://github.com/kkroening/ffmpeg-python)
* [`youtube-dl`](https://github.com/ytdl-org/youtube-dl)

### Let's go!

Assuming you already have an account with Spotify, you'll need to register an app with them ([see here](https://developer.spotify.com/dashboard/applications) which will take you a whole two minutes). In return, you will be given a client ID and a client secret, which you will want to put into the `credentials.py`; this will authorize the call that you'll make to the Spotify API. 

`youtube-dl` will download songs in the directory from which the command is called. We start by creating an empty `songs` folder, whose relative path we will pass as the second argument to our program. You can of course choose a different directory if you want your downloaded music to end up somewhere else (but make sure that directory is empty).

From the command-line, change directory to this repo and create an empty folder called `songs`, then install the requirements: 

`mkdir songs`

`pip install -r requirements.txt`

Finally, run the following command, replacing `spotify_username` with your actual username:

`python3.x Spotify_downloader.py spotify_username ./songs`

Assuming your client ID and client secret are valid, this will download a list of `spotify_username`'s liked songs into `list_of_spotify_songs.json`. The songs from this list will be downloaded into `./songs`, and their id tags will be updated. 

You can then import the music from this folder into iTunes to find your neatly organized music library. Enjoy!  
