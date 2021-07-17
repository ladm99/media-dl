from pytube import YouTube
from pytube import Playlist
import os
import subprocess


def adapt(yt):
	video = yt.streams.filter(only_video = True, adaptive=True, file_extension='mp4')
	audio = yt.streams.filter(only_audio=True,file_extension='mp4')

	count = 0
	print('Video: ' + fix_text(yt.title))
	for x in video:
		print(str(count) + ': ',end='')
		print(x)
		print()
		count+=1
	vIndex = input('Select which video to download: \n')
	vIndex = int(vIndex)

	count = 0
	print('Audio: ' + fix_text(yt.title))
	for x in audio:
		print(str(count) + ': ',end='')
		print(x)
		print()
		count+=1
	aIndex = input('Select which Audio to download: ')
	aIndex = int(aIndex)
	print('Downloading ' + fix_text(yt.title) + ' video')
	video[vIndex].download(filename=fix_text(yt.title))
	print('Video download finished')
	out = yt.title + ' audio'
	out = fix_text(out)
	print('Downloading ' + fix_text(yt.title) + ' audio')
	audio[aIndex].download(filename=out)
	print('Audio download finished')

def cap(yt):
	print('\nDownload subtitles?\n-------------------\n1. Yes\n2. No')
	select = input('Enter Selection: ')
	if select == '2':
		return select
	elif select == '1':
		subs = yt.captions
		name = yt.title
		name = name + ' subs.srt'
		name = fix_text(name)
		print('Captions: ')
		count = 0
		for x in subs:
			print(str(count) + ': ',end='')
			print(x)
			print()
			count+=1

		code = input('Select which languge to download via the languge code (if nothing appears then just push enter, there are no captions for the video): ')
		code = code.strip()

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

def mux(yt,prog, cap_true):
	input('\nPush Enter to mux (muxing will delete the original files after createing the mkv) or ctrl c to quit')

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
		
		cmd = 'ffmpeg -i ' + video + ' -i ' + audio + ' -i ' + subs + ' -c copy ' + output

		os.system(cmd)
		delete = 'del ' + video + ' ' + audio + ' ' + subs
		os.system(delete)

#if the video is adaptive and captions were not downloaded
	elif prog == False and cap_true == '2':

		cmd = 'ffmpeg -i ' + video + ' -i ' + audio +  ' -c copy ' + output
		os.system(cmd)
		delete = 'del ' + video + ' ' + audio
		os.system(delete)

#if the video is progressive and captions were downloaded
	elif prog == True and cap_true == '1':

		cmd = 'ffmpeg -i ' + video + ' -i ' + subs + ' -c copy ' + output

		os.system(cmd)
		delete = 'del ' + video + ' ' + subs
		os.system(delete)

	elif prog == True and cap_true == '2':
		return

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

def pl(playlist):
	p = playlist
	title = fix_text(p.title)
	try:
		os.mkdir(title)
	except OSError as error:
		print('Output folder already exists')
	os.chdir(title)
	for url in p.video_urls:
		print('\n')
		yt = YouTube(url)
		adapt(yt)
		cap_true = cap(yt)
		mux(yt, False, cap_true)


def main():
	url = ''
	url = input('url: ')

	playlist = Playlist(url)
	pl(playlist)

main()