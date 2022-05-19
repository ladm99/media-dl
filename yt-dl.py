from os import path
import os
import subprocess as sp
from cmdBuilder import cmdBuilder
"""
- Pulls a youtube video from a url
- Gives opteion to downald progressive videos or adaptive videos (video + audio, usually higher quality)
- Can download captions
- Will mux the audio, video, and captions into an mkv file while deleteing the original files
-Cap means captions, don't know why I didn't just name it subs
"""

#Main funcition is for the menu selection and the calls for the other functions
def main():
	
	while True:

		url = ''
		url = input('Enter a url: ')
		title = sp.getoutput('yt-dlp.exe --print title ' + url)
		print('YouTube video found - ' + title)
		dash = '\n--------------------'
		for s in range(len(title)):
			dash = dash + '-'

		builder = cmdBuilder(url, [])
		#Creates output directory
		try:
			os.mkdir('Output')
		except OSError as error:
			print('')

		print('Enter Selection for ' + title + dash)
		res = input('\nEnter desired resolution (if resolution is not found the next highest will be downloaded) leave blank for best resolution: ')
		if res == '':
			builder.addOption('-f "bv+ba/b"')
		else:
			res = '-f "bv*[height<=' + res + ']+ba/b[height<=' + res + '] / wv*+ba/w"'
			builder.addOption(res)

		subs = input('Download and embed subs (English, default is yes) [Y/N]: ').lower()
		if subs == 'y' or subs == '':
			builder.addOption('--embed-subs')
			subsFormat = input('What format do you want for the subs (srt, vtt, ass, lrc) (default is srt): ').lower()
			if subsFormat == '':
				subsFormat = 'srt'
			subsFormat = '--convert-subs "' + subsFormat + '"'
			builder.addOption(subsFormat)

		videoFormat = input('What video format do you want (embedding subs will only work with mp4 and mkv) (default is mkv): ').lower()
		if videoFormat == '':
			videoFormat = 'mkv'
		videoFormat = '--remux-video "' + videoFormat + '"'
		builder.addOption(videoFormat)
		builder.addOption('-P "Output"') #outputs download to the output folder
		# print(builder.buildCommand())
		os.system(builder.buildCommand())


main()