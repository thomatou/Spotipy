## Spotify: how to retrieve your saved music, format it neatly, and keep it locally

### Intro and overview

The python scripts in this repo allow any Spotify user (with a free or paid subscription) to download the entirety of one's Spotify library ('Liked songs') from Youtube, ensuring that the info relating to those files is appropriately formatted; thus enabling the user to keep a well-organized library in iTunes.

Briefly, the code contained in `get_track_list_download.py` retrieves the list of a user's saved songs. The information contained in this list of songs is passed to the `ytmdl` command from the eponymous [package](https://github.com/deepjyoti30/ytmdl), which enables downloading of the corresponding songs from Youtube.

The name of the files downloaded through the `ytmdl` package is usually that of the corresponding Youtube video. Unfortunately, those names are not standardized and often lack important information to keep one's music library organized (name of the album, for instance). Thus, each .mp3 file's name (usually containing the name of the song and of the artist in random order) needs to be matched back to one of the entries of the list that was originally retrieved from Spotify (which contains all of the relevant information in a standard format). This is done through a fuzzy string search, using the `fuzzywuzzy` [package](https://github.com/seatgeek/fuzzywuzzy).

Once a match is found, the `updating_id_tags.py` iterates through the list of downloaded songs and updates each file's id3 tags according to the information that was originally obtained from Spotify (specifically, name of the song, name of the artist, name of the album, and the track's number in the album). The files can then be imported into iTunes, thus enabling one to keep a local copy of your Spotify music.


### Prerequisites: 
* Python 3.x
* [`spotipy`](https://spotipy.readthedocs.io/en/2.9.0/)
* [`ffmpeg`](https://github.com/FFmpeg/FFmpeg)
* [`ytmdl`](https://github.com/deepjyoti30/ytmdl)
* [`fuzzywuzzy`](https://github.com/seatgeek/fuzzywuzzy)

### Getting started

Assuming you already have an account with Spotify, you'll need to register an app with them ([see here](https://developer.spotify.com/dashboard/applications) (which will take a whole minute). In return, you will be given a client ID and a client secret, which you will want to put into the `credentials.py`; this will authorize the call that you'll make with the Spotify API. 

From the command-line, run the following command: 
`python3.x get_track_list_download.py spotify_username name_of_file_containing_spotify_data.txt`

Assuming your client ID and client secret are valid, this will download a list of `spotify_username`'s liked songs into `name_of_file_containing_spotify_data.txt`. The songs from this list will be downloaded into ~/Music/ytmdl primarily, as well as into ~/Music. Move all the songs in the ~/Music folder into the ~/Music/ytmdl folder.

Next, run the following command:
`python3.x re_download.py ~/Music/ytmdl`

Followed by:
`python3.x name_matching.py name_of_file_containing_spotify_data.txt ~/Music/ytmdl`

Finally: 
`python3.x updating_id_tags.py ~/Music/ytmdl`

Your music should now be in ~/Music/ytmdl_upated. Opening those files in iTunes will reveal that the tags have been properly formatted, and your library should automatically organize itself.
