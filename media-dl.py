#TODO: more tests
import yt_dlp
import os
from os import path
import _pickle as pickle
from config import Config

def main():
	# check to see if the yt-dlp is up to date
	os.system('yt-dlp.exe -U')
	
	output_dir = "output"
	while True:
		ydl_opts = {'external_downloader': 'aria2c'}
		postprocessors = []
		title = ''
		formatVideoTitle = ''
		# check to see if config file exists
		if path.exists('config.pkl') == False:
			Config.createConfig()
		else:
			url = ''
			# open the config file
			data = open('config.pkl', 'rb')
			con = pickle.load(data)

			print('\nEnter Selection\n' + '---------------')
			print('1. Enter url\n2. View config\n3. Edit config\n4. Quit')
			select = input('Enter: ')
			if select == '1':
				url = input('url: ')
				# check to see if it is a crunchyroll link
				cr = 'crunchyroll' in url
				# check to see if it is a playlist or series link
				playlist = 'playlist' in url  or 'series' in url

				

				if playlist:
					title = input('\nEnter directory name for this playlist to be downloaded to: ')
					formatVideoTitle = input('\nDo you want the video titles to be in the format of "Directory_Name - playlist_index" [Y/N] (default is No): ').lower()
					ydl_opts['ignoreerrors'] = True

				res = con.resolution
				if res == '':
					ydl_opts['format'] = 'bv+ba/b'
				else:
					# have to do this stupid if statement for cr because of how the beta works hopefully it gets fixed
					if cr:
						
						#check to see if its a playlist
						if playlist:
							language = '[language=' + con.lang_code + ']'
							ydl_opts['format'] = 'bv*[height<=' + con.resolution + ']+ba' + language + '/b[height<=' + con.resolution + ']' + language +'/ wv*+ba' + language +'/w' + language
						else:
							ydl_opts['format'] = 'bv*[height<=' + con.resolution + ']+ba/b[height<=' + con.resolution + '] / wv*+ba/w'
					else:
						ydl_opts['format'] = 'bv*[height<=' + con.resolution + ']+ba/b[height<=' + con.resolution + '] / wv*+ba/w'
				subs = con.subs
				if subs == 'y' or subs == '':
					subsFormat = con.subsFormat

					ydl_opts['writesubtitles'] = True
					if cr: # if it is a crunchyroll link then ass is automatically selected because it looks better in the video
						subsFormat = 'ass'

						ydl_opts['subtitleslangs'] = ['en-US']

					elif subsFormat == '' and cr == False:
						# subsFormat = 'srt'
						ydl_opts['subtitleslangs'] = ['en']
					else:
						postprocessors.append(dict({'key': 'FFmpegSubtitlesConvertor', 'format' : subsFormat}))
					
				postprocessors.append(dict({'key': 'FFmpegVideoRemuxer', 'preferedformat' : con.videoFormat}))
				postprocessors.append(dict({'key': 'FFmpegEmbedSubtitle'}))

				if cr == True:
					language = con.lang_code
					browser = con.browser
					if browser != '':
						ydl_opts['cookiesfrombrowser'] = (con.browser,)
					
				# if the url is a playlist then it will have its own directory in the output dicrectory
				if playlist:
					out = f'{output_dir}/{title}/%(title)s.%(ext)s'
					if formatVideoTitle == 'y':
						# correctly formats the video title to be in the for of directory_name - playlist_index
						out = f'{output_dir}/{title}/{title} - %(playlist_index)s.%(ext)s'
					ydl_opts['outtmpl'] = out
				else:
					ydl_opts['outtmpl'] = f'{output_dir}/%(title)s.%(ext)s'
				ydl_opts['postprocessors'] = postprocessors

				with yt_dlp.YoutubeDL(ydl_opts) as ydl:
					error_code = ydl.download(url)
				# pprint(ydl_opts)
			elif select == '2':
				r = con.resolution
				s = con.subs
				l = con.lang_code
				sf = con.subsFormat
				b = con.browser

				if r == '':
					r = 'Highest resolution'
				if s == '':
					s = 'Yes'
				if sf == '':
					sf = 'Default format'
				if b == '':
					b = 'None'

				print(f'\nCurrent Config\n--------------\nResolution: {r}\nSubs: {s}\nSubs Format: {sf}\nBrowser: {b}')

			elif select == '3':
				Config.createConfig()
			elif select == '4':
				exit()

def fix_text(text):
	badChars = ['/', ':','*', '?', '"', '<', '>', '|', ',', "'"]
	textList = list(text)
	for i in range(len(textList)):
		if textList[i] in badChars:
			textList[i] = ''
	return ''.join(textList)

main()