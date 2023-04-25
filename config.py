# class for creating config files

import _pickle as pickle

class Config(object):
	def __init__(self, resolution, subs, lang_code, subsFormat, videoFormat, browser):
		self.resolution = resolution
		self.subs = subs
		self.lang_code = lang_code
		self.subsFormat = subsFormat
		self.videoFormat = videoFormat
		self.browser = browser

	def createConfig():
		resolution = input('\nEnter desired resolution (if resolution is not found the next highest will be downloaded) leave blank for best resolution: ')
		subs = input('Download and embed subs (English, default is yes) [Y/N]: ').lower().strip()
		subsFormat = ''
		if subs == 'y' or subs == '' :
			subsFormat = input('What format do you want for the subs (srt, vtt, ass, lrc) (default is whatever the original format is) : ').lower().strip()

		videoFormat = input('What video format do you want (embedding subs will only work with mp4 and mkv) (default is mkv): ').lower().strip()
		if videoFormat == '':
			videoFormat = 'mkv'
		# lang_code = input('Enter languge code of the subtitles you wish to download (en for english): ').lower()
		lang_code =  input('If downloading from Crunchyroll, what is your preferred audio language (ja-JP is the default, en-US for English): ')
		if lang_code == '':
			lang_code = 'ja-JP'

		text = 'If you want to download premimum content from Crunchyroll, login to CR on your desired browser and enter the browser name here'\
		'(supporter browsers: brave, chrome, chromium, edge, firefox, opera, safari, vivaldi. Leave blank if you do not wish to use cookies: '
		browser = input(text).lower().strip()

		output = open('config.pkl', 'wb')
		config = Config(resolution, subs, lang_code, subsFormat, videoFormat, browser)
		pickle.dump(config, output, -1)
		output.close()