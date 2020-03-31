import sys
import spotipy
import spotipy.util as util
import credentials_real # Need a file name credentials.py containing the client_id and and client_secret
import os
import re
import json
import subprocess





def get_saved_tracks_from_user(username, name_of_output_file):

    '''
    This function gets a spotify user's saved tracks
    saves a list of the music
    and returns that list as a json object
    '''

    scope = 'user-library-read'

    token = util.prompt_for_user_token(username,
                                        scope,
                                        credentials_real.client_id,
                                        credentials_real.client_secret,
                                        redirect_uri = 'http://localhost/')

    if token:
        sp = spotipy.Spotify(auth=token)
        file = open(name_of_output_file, 'w')

        total = 0
        max = 20

        data = sp.current_user_saved_tracks(limit = max, offset = total)

        all_tracks = {}

        while total < data['total']:

            results = sp.current_user_saved_tracks(limit = max, offset = total)
            counter = 0

            for item in results['items']:
                counter += 1
                temp = total + counter
                track = item['track']
                all_tracks.update({temp : {'track_name': track['name'], 'artist': track['artists'][0]['name'], 'album': track['album']['name'], 'track_no': track['track_number']}})

            total += max

        json.dump(all_tracks, file, indent = 2)

        file.close()

        return all_tracks

    else:
        print("Can't get token for", username)



def automate_download(json_list_of_songs, music_directory):

    '''
    This function downloads all the songs from the json input using ytmdl
    Keeps in memory the songs that weren't properly downloaded
    It renames every song based on being the last mp3 file that was downloaded
    IMPORTANT: make sure that the SONG_DIR and SONG_TEMP_DIR in defaults.py in ytmdl folder are set to the same folder of your choice
    '''

    # Youtube search only using track name and artist name
    # Need to remove any characters in those fields that might trip up the shell, such as an apostrophe - keep only alphanumeric characters

    os.chdir('/Users/tchavas/Music/ytmdl')

    download_fails = [] # This will contain the list of songs that have not been downloaded properly

    for element in json_list_of_songs.keys():
        try:
            temp = json_list_of_songs[element]
            song_artist = temp['track_name'] + " " + temp['artist']
            search_string = re.sub('\W+', ' ', song_artist)
            os.system('ytmdl -q ' + search_string)

            print('this song is now downloaded')

            latest_song = subprocess.run(['ls -t *.mp3 |head -1'], stdout=subprocess.PIPE, shell = True).stdout.decode('utf-8').split('\n')[0]

            os.rename(latest_song, element + '_' + search_string + '.mp3')

            print('song has been renamed')
        except:
            download_fails.append(element)
            continue

def add_id_tags(json_list_of_songs, music_directory):
    '''

    '''
    os.chdir(music_directory)
    id_tag_update_fail = []

    for filename in os.listdir():
        if filename.endswith('.mp3'):
            print(filename)
            temp = json_list_of_songs[filename.split('_')[0]]

            name = re.sub("[`/\"]", "'", temp['track_name'])
            artist = re.sub("[`/\"]", "'", temp['artist'])
            album = re.sub("[`/\"]", "'", temp['album'])
            new_filename = filename.split('.mp3')[0] + '_updated.mp3'

            command = ('''ffmpeg -i "%s" -c copy -metadata title="%s" -metadata artist="%s" -metadata album="%s" -metadata track="%s" "%s" ''') %(filename, name, artist, album, temp['track_no'], new_filename)

            try:
                os.system(command)
                # Need to delete the original file
                os.remove(filename)
            except:
                id_tag_update_fail.append(filename)
                continue

    if id_tag_update_fail:
        print('Here are the files whose id3 tags were not updated properly:')
        return id_tag_update_fail
