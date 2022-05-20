import yt_dlp
import os
from os import path
import subprocess
import _pickle as pickle
from config import Config
from cmdBuilder import cmdBuilder

def main():
	# check to see if the yt-dlp is up to date
	os.system('yt-dlp.exe -U')
	ydl_opts = {'quiet' : False}
	while True:
		title = ''
		formatVideoTitle = ''
		# check to see if config file exists
		if path.exists('config.pkl') == False:
			Config.createConfig()
		else:
			url = ''

			print('\nEnter Selection\n' + '---------------')
			print('1. Enter url\n2. Edit config\n3. Quit')
			select = input('Enter: ')
			if select == '1':
				url = input('url: ')
				# check to see if it is a crunchyroll link
				cr = 'crunchyroll' in url
				# check to see if it is a playlist or series link
				playlist = 'playlist' in url  or 'series' in url

				# open the config file
				data = open('config.pkl', 'rb')
				con = pickle.load(data)

				# have to use pytube to get the title for playlists because it takes too long with yt-dlp
				if playlist == False:
					with yt_dlp.YoutubeDL(ydl_opts) as ydl:
						info = ydl.extract_info(url, download = False)
						title = info.get('title', None)
						print(title)

				if playlist:
					title = input('\nEnter directory name for this playlist to be downloaded to: ')
					formatVideoTitle = input('\nDo you want the video titles to be in the format of "Directory_Name - playlist_index" [Y/N] (default is yes): ').lower()
				else:
					print('\nVideo found - ' + title)


				# create builder object
				builder = cmdBuilder(url, [])

				res = con.resolution
				if res == '':
					builder.addOption('-f "bv+ba/b"')
				else:
					res = '-f "bv*[height<=' + con.resolution + ']+ba/b[height<=' + con.resolution + '] / wv*+ba/w"'
					builder.addOption(res)

				subs = con.subs
				if subs == 'y' or subs == '':
					builder.addOption('--embed-subs')
					subsFormat = con.subsFormat
					if cr:
						subsFormat = 'ass'
					elif subsFormat == '' and cr == False:
						subsFormat = 'srt'
					# elif subsFormat == '' and cr:
					# 	subsFormat = 'ass'
					subsFormat = '--convert-subs "' + subsFormat + '"'
					builder.addOption(subsFormat)

				videoFormat = '--remux-video "' + con.videoFormat  + '"'
				builder.addOption(videoFormat)

				if cr == True and playlist == True:
					language = con.lang_code
					language = '--extractor-args "crunchyroll:language=' + language + '"'
					builder.addOption(language)
					

				# if the url is a playlist then it will have its own directory in the output dicrectory
				if playlist:
					out = ' -P "Output\\' + fix_text(title) + '"'
					if formatVideoTitle == 'y' or formatVideoTitle == '':
						# correctly formats the video title to be in the for of directory_name - playlist_index
						outputTemplate = ' -o "' + fix_text(title) + ' - "%(playlist_index)s.%(ext)s'
						out = out + outputTemplate
					builder.addOption(out)
				else:
					builder.addOption('-P "Output"')

				os.system(builder.buildCommand())
			elif select == '2':
				Config.createConfig()
			elif select == '3':
				exit()


def fix_text(text):
	replace_text = text.replace('/', '')
	replace_text = replace_text.replace(':', '')
	replace_text = replace_text.replace('*', '')
	replace_text = replace_text.replace('?', '')
	replace_text = replace_text.replace('"', '')
	replace_text = replace_text.replace('<', '')
	replace_text = replace_text.replace('>', '')
	replace_text = replace_text.replace('|', '')
	replace_text = replace_text.replace(',', '')
	replace_text = replace_text.replace("'", '')

	return replace_text

main()