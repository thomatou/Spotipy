# Spotify: how to retrieve your saved music, format it neatly, and keep it locally

The code in this repo allows any Spotify user (with a free or paid subscription) to download the entirety of one's Spotify library ('Liked songs') from Youtube, ensuring that the info relating to those files (i.e. 'id3 tags') is appropriately formatted; thus enabling the user to keep a well-organized library in iTunes.

Briefly, the code contained in `get_track_list_download.py` retrieves the list of the user's saved songs. The information contained in this list of songs is passed to the `ytmdl` command, which enables downloading of the corresponding songs from Youtube.

The name of the files downloaded through the `ytmdl` package is usually that of the corresponding Youtube video. Unfortunately, those names are not standardized and often lack important information to keep one's music library organized (name of the album, for instance). Thus, each .mp3 file's name (usually containing the name of the song and of the artist in undefined order) needs to be matched back to one of the entries of the list that was retrieved from Spotify.





#### Pre-requisites (all available through pip): 
* spotipy
* ffmpeg
* ytmdl
* fuzzywuzzy




A streamgraph representation of the gender split in Congress, using R’s dedicated `streamgraph` [package](https://github.com/hrbrmstr/streamgraph), provides an insightful look at the 20,000 members of Congress that have been in office over the past century. While the number of women in Congress has been steadily increasing over the past 30 years, the number of female democrats is growing noticeably faster than the number of female republicans.



<span style="font-size:4em;">Female Democrats are represented in dark blue, female Republicans in dark red; male Democrats in light blue, and male Republicans in light red. The yellow line corresponds to independent members.</span>


