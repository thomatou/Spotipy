import os
import re
import sys

def update_id_tags(name_of_directory):
    '''
    name_of_directory is where the music is stored
    '''

    files_that_had_issue = []
    #os.chdir(name_of_directory)

    # Need to create a new directory that will contain the new files
    # Otherwise will be iterating over a list of files that is changing
    # which will lead to issues

    new_directory = name_of_directory + '_updated'

    os.mkdir(new_directory)

    os.chdir(name_of_directory)


# Need to remove the " characters as they trip up the os.system(command)

    for filename in os.listdir():
        if filename.endswith('.mp3'):
            os.rename(filename, re.sub("[`\"]", "'", filename))

        # What happens if one of these fields is missing?
            try:
                track = filename.split('_')[0]
                artist = filename.split('_')[1]
                album = filename.split('_')[2]
                track_no = filename.split('_')[3].split('.')[0]

            except:
                print('except')
                continue #otherwise the commands below will throw an error


            output_name = filename.split('.')[0] + '_updated.mp3'
            # First thing to do is to create a copy of the file with
            # the correct tags

            command = ('''ffmpeg -i "%s" -c copy -metadata title="%s" -metadata artist="%s" -metadata album="%s" -metadata track="%s" "%s" ''') %(os.path.join(name_of_directory,filename), track, artist, album, track_no, os.path.join(name_of_directory,output_name))

            #print(command)
            try:
                os.system(command)

                # Now move the new file to the new directory
                os.rename(os.path.join(name_of_directory,output_name), os.path.join(new_directory,output_name))

                # Now restore its original name
                os.rename(os.path.join(new_directory, output_name), os.path.join(new_directory, filename))

            except:
                    files_that_had_issue.append(filename)
                    continue

    if files_that_had_issue:
        print('The files that had issues with tag updating are shown below, consider updating the tags manually')
        for element in files_that_had_issue:
            print(element)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        update_id_tags(sys.argv[1])
    else:
        print('Try again with the following usage: %s path_to_music_folder' %(sys.argv[0]))



# update_id_tags('/Users/tchavas/Music/ytmdl')
