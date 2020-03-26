### Spotify: how to retrieve your saved music, format it neatly, and keep it locally

The code in this repo allows any Spotify user (with a free or paid subscription) to download the entirety of one's Spotify library ('Liked songs') from Youtube, ensuring that the info relating to those files is appropriately formatted; thus enabling the user to keep a well-organized library in iTunes.

Briefly, the code contained in `get_track_list_download.py` retrieves the list of a user's saved songs. The information contained in this list of songs is passed to the `ytmdl` command from the eponymous [package](https://github.com/deepjyoti30/ytmdl), which enables downloading of the corresponding songs from Youtube.

The name of the files downloaded through the `ytmdl` package is usually that of the corresponding Youtube video. Unfortunately, those names are not standardized and often lack important information to keep one's music library organized (name of the album, for instance). Thus, each .mp3 file's name (usually containing the name of the song and of the artist in random order) needs to be matched back to one of the entries of the list that was originally retrieved from Spotify (which contains all of the relevant information in a standard format). This is done through a fuzzy string search, using the `fuzzywuzzy` [package](https://github.com/seatgeek/fuzzywuzzy).

Once a match is found, the `updating_id_tags.py` iterates through the list of downloaded songs and updates each file's id3 tags according to the information that was originally obtained from Spotify (specifically, name of the song, name of the artist, name of the album, and the track's number in the album). The files can then be imported into iTunes, thus enabling one to keep a local copy of your Spotify music.


#### Prerequisites (all available through pip): 
* Python 3.x
* [`spotipy`](https://spotipy.readthedocs.io/en/2.9.0/)
* [`ffmpeg`](https://github.com/FFmpeg/FFmpeg)
* [`ytmdl`](https://github.com/deepjyoti30/ytmdl)
* [`fuzzywuzzy`](https://github.com/seatgeek/fuzzywuzzy)

