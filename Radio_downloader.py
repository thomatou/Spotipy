from selenium import webdriver
import json
import time
import spotipy
import spotipy.util as util
import credentials
import sys

class RadioDownloader:
    def __init__(self, username):
        """
        Will probably want to instantiate with the spotify username
        + API key in order to create a new playlist
        """
        self.spotify_username = username

    def djam_radio(self):
        """
        Will want to make the selenium browser headless
        """
        tracks = {}
        counter = 0
        artist_path = '/html/body/div[2]/div[7]/div[1]/div[1]/div[1]/div[2]/span[1]/a'
        song_path = '/html/body/div[2]/div[7]/div[1]/div[1]/div[1]/div[2]/span[2]'
        browser = webdriver.Firefox(executable_path='/Users/tchavas/geckodriver')

        try:
            while counter < 5:
                browser.get('https://www.djamradio.com/')
                time.sleep(2)
                artist = browser.find_element_by_xpath(artist_path).text
                song = browser.find_element_by_xpath(song_path).text

                tracks.update({counter:{'artist': artist, 'song': song}})

                counter += 1

            with open('djam_output.txt', 'w') as file:
                json.dump(tracks, file, indent=2)


        except KeyboardInterrupt:
            with open('djam_output.txt', 'w') as file:
                json.dump(tracks, file, indent=2)

            browser.quit()

        browser.quit()

    def create_spotify_playlist(self, playlist_name):
        """

        """
        self.playlist_name = playlist_name
        token = util.prompt_for_user_token(self.spotify_username,
                                           'playlist-modify-private',
                                           credentials.client_id,
                                           credentials.client_secret,
                                           redirect_uri='http://localhost/')
        if not token:
            print('invalid credentials, cannot create playlist. Exiting now')
            sys.exit()

        sp = spotipy.Spotify(auth=token)

        sp.user_playlist_create(user=self.spotify_username,
                                name=self.playlist_name,
                                public=False,
                                description='Songs curated by Djamradio')

    def populate_playlist(self, playlist_name):



RadioDownloader('thomatou').create_spotify_playlist('DJAM')
