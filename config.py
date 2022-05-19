# class for creating config files

import _pickle as pickle

class Config(object):
	def __init__(self, resolution, subs, lang_code):
		self.resolution = resolution
		self.subs = subs
		self.lang_code = lang_code

	def createConfig():
		resolution = input('Desired resolution of the videos you want to download (144, 360, 720, 1080, etc.): ')
		x = input('Do you want to download subtitles [Y,N]: ').lower()
		if x == 'y':
			subs = '1'
		else:
			subs = '2'
		lang_code = input('Enter languge code of the subtitles you wish to download (en for english): ').lower()

		output = open('config.pkl', 'wb')
		config = Config(resolution, subs, lang_code)
		pickle.dump(config, output, -1)
		output.close()