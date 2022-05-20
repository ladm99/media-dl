# class for creating config files

import _pickle as pickle

class Config(object):
	def __init__(self, resolution, subs, lang_code, subsFormat, videoFormat):
		self.resolution = resolution
		self.subs = subs
		self.lang_code = lang_code
		self.subsFormat = subsFormat
		self.videoFormat = videoFormat

	def createConfig():
		resolution = input('\nEnter desired resolution (if resolution is not found the next highest will be downloaded) leave blank for best resolution: ')
		subs = input('Download and embed subs (English, default is yes) [Y/N]: ').lower()
		subsFormat = ''
		if subs == 'y' or subs == '' :
			subsFormat = input('What format do you want for the subs (srt, vtt, ass, lrc) (default is srt, ass for crunchyroll) : ').lower()
			if subsFormat =='':
				subsFormat = 'srt'

		videoFormat = input('What video format do you want (embedding subs will only work with mp4 and mkv) (default is mkv): ').lower()
		if videoFormat == '':
			videoFormat = 'mkv'
		# lang_code = input('Enter languge code of the subtitles you wish to download (en for english): ').lower()
		lang_code =  input('If downloading from Crunchyroll, what is your preferred audio language (jaJp is the default)')
		if lang_code == '':
			lang_code = 'jaJp'

		output = open('config.pkl', 'wb')
		config = Config(resolution, subs, lang_code, subsFormat, videoFormat)
		pickle.dump(config, output, -1)
		output.close()