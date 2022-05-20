from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
import os
from os import path
import subprocess
from config import Config

def main():
	while True:

		if path.exists('config.pkl') == False:
			Config.createConfig()
		else:
			pklPath = os.path.abspath('config.pkl')
			ffmpegPath = os.path.abspath('ffmpeg.exe')
			print('Enter Selection\n' + '---------------')
			print('1. Enter url\n2. Edit config\n3. Quit')
			select = input('Enter: ')
			if select == '1':
				url = ''
				url = input('url: ')
				playlist = Playlist(url)
				pl(playlist, pklPath, ffmpegPath)
			elif select == '2':
				createConfig()
			elif select == '3':
				exit()


#adapt function shows the filesize and a progressbar while downloading
def adapt(yt, path):
	data = open(path, 'rb')
	config = pickle.load(data)

	video = yt.streams.filter(resolution = config.resolution, only_video = True, adaptive=True, file_extension='mp4')
	audio = yt.streams.filter(only_audio=True,file_extension='mp4').order_by('abr').desc()
	#puts audio stream with highest bitrate at index 0

	if len(video) != 0 and len(audio):
		print('Downloading ' + fix_text(yt.title) + ' video | ' + str(convertToMegs(video[0].filesize)) + 'MB')
		video[0].download(filename=fix_text(yt.title) + '.mp4')		
		print('Video download finished')

		print('Downloading ' + fix_text(yt.title) + ' audio | ' + str(convertToMegs(audio[0].filesize)) + 'MB')
		audio[0].download(filename=(fix_text(yt.title) + ' audio' + '.mp4'))
		print('Audio download finished')
	else:
		print('Could not find the video in the resolution you were looking for, downlading the next highest resolution avaliable')
		video = yt.streams.filter(only_video = True, adaptive=True, file_extension='mp4').order_by('resolution').desc()
		#orders the video streams by resolution in descencing order so that the highest resolution is at index 0
		print('Downloading ' + fix_text(yt.title) + ' video | ' + str(convertToMegs(video[0].filesize)) + 'MB')
		video[0].download(filename=fix_text(yt.title) + '.mp4')
		print('Video download finished')
		out = yt.title + ' audio' + '.mp4'
		out = fix_text(out)
		print('Downloading ' + fix_text(yt.title) + ' audio | ' + str(convertToMegs(audio[0].filesize)) + 'MB')
		audio[0].download(filename=out)
		print('Audio download finished')

#displays and downloads the captions (srt file)
def cap(yt, path):
	data = open(path, 'rb')
	config = pickle.load(data)

	select = config.cap
	if select == '2':
		return select
	elif select == '1':
		subs = yt.captions
		name = fix_text(yt.title)
		name = name + ' subs.srt'
		name = fix_text(name)
		print('Captions: ')
		
		code = config.lang_code

		try:
			subs = yt.captions[code]
			subs = subs.generate_srt_captions()
			print(name)
			f = open(name, 'w+', encoding='utf-8')
			f.write(subs)
			f.close()
			return select
		except( AttributeError, KeyError):
			print('No subtitles found')
			return '2'
	else:
		cap(yt)

#Uses ffmpeg and command prompt to mux the video, audio, and subs together into an mkv file
def mux(yt,prog, cap_true, ffmpegPath):
	vid_name = yt.title +'.mp4'
	audio_name = yt.title + ' audio.mp4'
	subs_name = yt.title + ' subs.srt'
	output_name = yt.title +'.mkv'

	video = fix_text(vid_name)
	audio = fix_text(audio_name)
	output = fix_text(output_name)
	subs = fix_text(subs_name)

	video = '"' + video + '"'
	audio = '"' + audio + '"'
	subs = '"' + subs + '"'
	output = '"' + output + '"'


	print(video)
	print(subs)
	print(output)

#if the video is adaptive and captions were downloaded
	if prog == False and cap_true == '1':
		
		cmd = ffmpegPath + ' -i ' + video + ' -i ' + audio + ' -i ' + subs + ' -c copy ' + output

		os.system(cmd)
		delete = 'del ' + video + ' ' + audio + ' ' + subs
		os.system(delete)

#if the video is adaptive and captions were not downloaded
	elif prog == False and cap_true == '2':

		cmd = ffmpegPath + ' -i ' + video + ' -i ' + audio +  ' -c copy ' + output
		os.system(cmd)
		delete = 'del ' + video + ' ' + audio
		os.system(delete)

#if the video is progressive and captions were downloaded
	elif prog == True and cap_true == '1':

		cmd = ffmpegPath + ' -i ' + video + ' -i ' + subs + ' -c copy ' + output

		os.system(cmd)
		delete = 'del ' + video + ' ' + subs
		os.system(delete)

	elif prog == True and cap_true == '2':
		return


#uses a playlist object that is created in main, creates a directory for the videos and downloads to it 
def pl(playlist, pklPath, ffmpegPath):
	p = playlist
	title = fix_text(p.title)

	print('\nPlaylist found - ' + title)
	#Creates Directories
	try:
		os.mkdir('Output')
	except OSError as error:
		print('Output folder already exists')
	os.chdir('Output')

	try:
		os.mkdir(title)
	except OSError as error:
		print(title + ' folder already exists')
	os.chdir(title)
#downloads the videos
	for url in p.video_urls:
		#print('\n')
		yt = YouTube(url, on_progress_callback=on_progress)
		adapt(yt, pklPath)
		cap_true = cap(yt, pklPath)
		mux(yt, False, cap_true, ffmpegPath)
#goes back to the root directory
	try:
		os.chdir('..')
		os.chdir('..')
	except OSError as error:
		print('You should not see this')

#fixes filenames for the audio and video files
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

#conversion function
def convertToMegs(num):
	return round(num / 1000000, 2)

def printStream(stream):
	audio = stream.includes_audio_track
	video = stream.includes_video_track
	adapt = stream.is_adaptive
	if adapt == True:
		if video == True:
			print(f'Type: {stream.mime_type}, Resolution: {stream.resolution}, fps: {stream.fps}, Video Codec: {stream.video_codec}, Size: {convertToMegs(stream.filesize)}MB')
		else:
			print(f'Type: {stream.mime_type}, Bitrate: {stream.abr}, Audio Codec: {stream.audio_codec}, Size: {convertToMegs(stream.filesize)}MB')
	else:
		print(f'Type: {stream.mime_type}, Resolution: {stream.resolution}, fps: {stream.fps}, Video Codec: {stream.video_codec}, Audio Codec: {stream.audio_codec}, Size: {convertToMegs(stream.filesize)}MB')


main()
