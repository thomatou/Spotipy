import sys
import spotipy
import spotipy.util as util
import credentials # Need a file name credentials.py containing the client_id and and client_secret
import os
import re






def get_saved_tracks_from_user(username, name_of_output_file):

    scope = 'user-library-read'

    token = util.prompt_for_user_token(username,
                                        scope,
                                        credentials.client_id,
                                        credentials.client_secret,
                                        redirect_uri = 'http://localhost/')

    if token:
        sp = spotipy.Spotify(auth=token)
        f = open(name_of_output_file, 'w')

        total = 0
        max = 20
        data = sp.current_user_saved_tracks(limit = max, offset = total)

        while total < data['total']:
            results = sp.current_user_saved_tracks(limit = max, offset = total)
            total += max
            for item in results['items']:
                track = item['track']
                f.write(track['name'] + '_' + track['artists'][0]['name'] + '_' + track['album']['name'] + '_' + str(track['track_number']) + '\n')
        f.close()

    else:
        print("Can't get token for", username)


def automate_download(list_of_songs):

    with open(list_of_songs, 'r') as f:
        data = f.read().split('\n')

    # Each line in data is formatted in the following way:
    # Track name, artist, album, track number, each field separated by '_'

    # Youtube search only using track name and artist name
    # Need to remove any characters in those fields that might trip up the shell, such as an apostrophe - keep only alphanumeric characters

    for element in data:
        temp = ' '.join(element.split('_')[:2])
        search_string = re.sub('\W+', ' ', temp)
        os.system('ytmdl -q ' + search_string)

    # This will spit out all the mp3 files, albeit with no id3 tags (needed for itunes) and without a proper name


    # This will spit out all the mp3 files, albeit with no id3 tags (needed for itunes) and without a proper name

    # By default, most songs will be put in the /Users/your_username/Music/ytmdl folder, with some in the /Users/your_username/Music/folder.

    # Transfer manually all the songs to the /Users/your_username/Music/ytmdl folder.

    # Then run re_download.py



if __name__ == '__main__':
    if len(sys.argv) == 3:
        get_saved_tracks_from_user(sys.argv[1], sys.argv[2])
        automate_download(sys.argv[2])
        print('Download of tracks is complete\n. Please move all downloaded files to the ytmdl folder before proceeding to the next step.')

    else:
        print('Try again with the following usage: %s username name_of_output_file' %(sys.argv[0]))
