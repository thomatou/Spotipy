import re
import os
import sys




# Some of the songs don't download properly, usually when the song is uploaded by the actual artist account on youtube (blocked ytmdl and other downloading tools?) We can catch those by looking at the size of the file.

# The songs that weren't downloaded properly tend to have a size < 1 MB (tested on ~ 1300 different songs).
# List those out from the directory where the newly downloaded songs are stored

# For these files, downloading the second choice proposed by ytmdl usually resolves the problem

def re_download(path_to_music_folder):

    redownloads = []

    os.chdir(path_to_music_folder)

    for filename in os.listdir():
        if filename.endswith('.mp3'):
            if os.stat(filename).st_size < 1e6:
                redownloads.append(filename)
                os.remove(filename)
                # Now delete those files once filenames are stored

    #print(redownloads)
    # The stupid names outputted by ytmdl have hashtags instead of spaces,
    # so sub those out, along with any non-alphanumeric character that might trip up the shell


    for filename in redownloads:
        temp = re.sub('\W+', ' ', " ".join(filename.split('_')[:2]))
        os.system('''ytmdl --choice 2 -q '%s' ''' %temp)


    # Now we have done our best, move on to name matching

if __name__ == '__main__':
    if len(sys.argv) == 2:
        re_download(sys.argv[1])
        print('Re-downloads complete. Now please move all music to the ytmdl folder and proceed to name_matching.py')
    else:
        print('Try again with the following usage: %s path_to_music_folder' %(sys.argv[0]))
