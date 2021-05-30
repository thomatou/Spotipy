import sys
import spotipy
import spotipy.util as util
import credentials
import os
import re
import json
import subprocess
import time


class Spotify_downloader:
    """
    This class needs to be instantiated with two arguments.

    First one is the spotify username.
    Second one is the path to the folder where you want the music to be placed.
    Works best if that directory is empty to begin with.
    """

    def __init__(self, username, path_to_directory):
        """
        Instantiate the class.

        music_dir is the folder in which the music is downloaded.
        It gets used by the two functions automate_download() and add_id_tags()
        """
        self.spotify_username = username
        self.music_dir = path_to_directory
        self.SPOTIFY_SCOPE = 'user-library-read'
        self.json_output_file = 'list_of_spotify_songs.json'

    def get_saved_tracks_from_user(self):
        """
        Get a spotify user's saved tracks.

        Save a list of the music
        and returns that list as a json object that is also saved to disk.
        """
        token = util.prompt_for_user_token(self.spotify_username,
                                           self.SPOTIFY_SCOPE,
                                           credentials.client_id,
                                           credentials.client_secret,
                                           redirect_uri='http://localhost/')

        if token:
            sp = spotipy.Spotify(auth=token)
            file = open(self.json_output_file, 'w')

            total = 0
            max = 20

            data = sp.current_user_saved_tracks(limit=max, offset=total)

            # all_tracks is a dictionary with the correct template
            # to contain all the song data in json format
            # each song is identified by a unique number, which is
            # the song's index in the user's spotify library (starts at 1).
            all_tracks = {}

            while total < data['total']:

            # Uncomment this line if you only want your most recent 100 songs
            # to be downloaded (and comment out the line above)
            # while total < 100:

                results = sp.current_user_saved_tracks(limit=max, offset=total)
                counter = 0

                for item in results['items']:
                    counter += 1
                    temp = total + counter
                    track = item['track']
                    all_tracks.update({temp: {'track_name': track['name'],
                                              'artist':
                                              track['artists'][0]['name'],
                                              'album': track['album']['name'],
                                              'track_no':
                                              track['track_number']}})

                total += max

            json.dump(all_tracks, file, indent=2)

            file.close()

            return all_tracks

        else:
            print("Can't get token for", self.spotify_username)

    def automate_download(self, json_list_of_songs):
        """
        Download all the songs from the json input using youtube-dl.

        Prints out the songs that weren't properly downloaded.
        It renames every song based on the last mp3 file that was downloaded
        """
        # Youtube search only using track name and artist name
        # Need to remove any characters in those fields that might trip up the
        # shell, such as an apostrophe - keep only alphanumeric characters

        # youtube-dl downloads music to the current working directory.
        os.chdir(self.music_dir)

        download_fails = []  # This will contain the list of songs that have
        # not been downloaded properly

        for element in json_list_of_songs.keys():
            # This is to keep track of the time
            # at which we start downloading a particular song
            time_before_download = time.time()

            try:
                temp = json_list_of_songs[element]
                song_artist = temp['track_name'] + " " + temp['artist']
                search_string = re.sub(r'\W+', ' ', song_artist)

                os.system('''youtube-dl --extract-audio --audio-format mp3 --no-mtime "ytsearch1: %s"''' % (search_string))

                print('this song is now downloaded')

            except Exception:
                download_fails.append(element)
                print('This one is going to download_fails')
                continue

            # This gets the name of the latest downloaded .mp3 file
            latest_song = subprocess.run(
                 ['ls -t *.mp3 |head -1'],
                 stdout=subprocess.PIPE,
                 shell=True).stdout.decode('utf-8').split('\n')[0]

        # This check is in place to make sure that the latest file downloaded
        # was downloaded after the start of this iteration of the for loop.
        # Otherwise, we'd rename the latest file downloaded, regardless of
        # whether it actually needed to be renamed

            if os.path.getmtime(latest_song) > time_before_download:
                os.rename(latest_song,
                          str(element) + '_' + search_string + '.mp3')

                print('song has been renamed')

        print('These are the songs that could not be downloaded:',
                download_fails)

    def add_id_tags(self, json_list_of_songs):
        r"""
        Add id_tags to all the songs.

        Need to remove special characters such as "\" or "/" from song name/
        artist/album in order to not trip up the command passed to terminal
        """
        os.chdir(self.music_dir)
        id_tag_update_fail = []

        for filename in os.listdir():
            if filename.endswith('.mp3'):
            # This try/catch is in place in case the directory where the music
            # is being saved has pre-existing files, or files which weren't
            # downloaded/renamed properly
                try:
                    temp = json_list_of_songs[filename.split('_')[0]]
                except KeyError:
                    print("could not find this file in the original list of \
                    downloads:", filename)
                    id_tag_update_fail.append(filename)
                    continue

                name = re.sub("[`/\"]", "'", temp['track_name'])
                artist = re.sub("[`/\"]", "'", temp['artist'])
                album = re.sub("[`/\"]", "'", temp['album'])
                new_filename = filename.split('.mp3')[0] + '_updated.mp3'

                command = ('''ffmpeg -i "%s" -c copy -metadata title="%s" \
                -metadata artist="%s" -metadata album="%s" \
                -metadata track="%s" "%s"''') % (filename, name, artist,
                          album, temp['track_no'], new_filename)

                try:
                    os.system(command)
                    os.rename(new_filename, filename)
                except Exception:
                    id_tag_update_fail.append(filename)


        if id_tag_update_fail:
            print('Here are the files whose id3 tags were not updated\
            properly:')
            print(id_tag_update_fail)


if __name__ == '__main__':
    if len(sys.argv) == 3:

        spotify_username = sys.argv[1]
        path_to_music_folder = sys.argv[2]
        user_class = Spotify_downloader(spotify_username, path_to_music_folder)

        list_of_songs = user_class.get_saved_tracks_from_user()

        # with open("./list_of_spotify_songs.json") as f:
        #     list_of_songs = json.load(f)

        print("Song list has been downloaded \
        into 'list_of_spotify_songs.json'")

        user_class.automate_download(list_of_songs)

        print('Songs have been downloaded')

        user_class.add_id_tags(list_of_songs)

        print('Mp3 id tags have been updated, \
        # music is now ready to be uploaded to iTunes.')

    else:
        print('Usage: %s spotify_username path/to/music/folder' % (sys.argv[0]))
