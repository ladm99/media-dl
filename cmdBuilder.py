class cmdBuilder(object):
	"""
	docstring for cmdBuilder
	Builds the command prompt commands 
	options are stored in a list	
	"""
	def __init__(self, url, options):
		super(cmdBuilder, self).__init__()
		self.url = url
		self.options = options

	def addOption(self, option):
		self.options.append(' ' + option)

	def buildCommand(self):
		out = 'yt-dlp.exe'
		# aria2c will always be used, -q to make output less verbose, --progress for download progress
		out = out + ' --downloader "aria2c" --progress ' 
		for x in self.options:
			out = out + x
		out = out + ' ' +self.url
		return out
		