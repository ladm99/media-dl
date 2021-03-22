from pytube import YouTube
import os
import subprocess
"""
- Pulls a youtube video from a url
- Gives opteion to downald progressive videos or adaptive videos (video + audio, usually higher quality)
- Can download captions
- Will mux the audio, video, and captions into an mkv file while deleteing the original files
- Might add playlist support
"""

def main():
	url = ''
	url = input('Enter a YouTube url: ')
	yt = YouTube(url)
	title = yt.title
	print('YouTube video found - ' + title)
	dash = '\n--------------------'
	for s in range(len(title)):
		dash = dash + '-'
	while True:
		print('\nEnter Selection for ' + yt.title + dash)
		print('1. Display Progressive video\n2. Display Adaptive Video + Audio\n3. Display all streams\n4. Enter a new url\n5. Quit')
		select = input('Enter: ')
		if select == '1':
			prog = True
			pro(yt)
			cap_true = cap(yt)
			mux(yt, prog, cap_true)
		elif select == '2':
			prog = False
			adapt(yt)
			cap_true = cap(yt)
			mux(yt, prog, cap_true)
		elif select == '3':
			streams = yt.streams
			for x in streams:
				print(x, end='\n\n')
		elif select == '4':
			main()
		elif select == '5':
			exit()


def pro(yt):
	video = yt.streams.filter(progressive=True, file_extension='mp4')
	count = 0
	print('Video:')
	for x in video:
		print(str(count) + ': ',end='')
		print(x)
		print()
		count+=1
	dl = input('Select which video to download: ')
	dl = int(dl)
	print('Downloading...')
	video[dl].download(filename=yt.title.replace('-',''))
	print('Download finished')

def adapt(yt):
	video = yt.streams.filter(adaptive=True, file_extension='mp4')
	audio = yt.streams.filter(only_audio=True,file_extension='mp4')

	count = 0
	print('Video:')
	for x in video:
		print(str(count) + ': ',end='')
		print(x)
		print()
		count+=1
	vIndex = input('Select which video to download: ')
	vIndex = int(vIndex)

	count = 0
	print('Audio:')
	for x in audio:
		print(str(count) + ': ',end='')
		print(x)
		print()
		count+=1
	aIndex = input('Select which Audio to download: ')
	aIndex = int(aIndex)
	print('Downloading Video...')
	video[vIndex].download(filename=yt.title.replace('-',''))
	print('Video download finished')
	out = yt.title + ' audio'
	out = out.replace('-' , '')
	print('Downloading Audio...')
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
		name = name.replace('"','')
		name = name.replace('-','')
		name = name.replace("'",'')
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
	video = ''
	audio = ''
	subs = ''
	output = ''

	if prog == False and cap_true == '1':
		
		for i in range(0,len(vid_name)):																		#add characters to these loops if they cause an issue
			if vid_name[i] != '"' and vid_name[i] != "'" and vid_name[i] != '-' and vid_name[i] != ':':
				video = video + vid_name[i]

		for i in range(0,len(audio_name)):
			if audio_name[i] != '"' and audio_name[i] != "'" and audio_name[i] != '-'and audio_name[i] != ':':
				audio = audio + audio_name[i]

		for i in range(0,len(subs_name)):
			if subs_name[i] != '"' and subs_name[i] != "'" and subs_name[i] != '-'and subs_name[i] != ':':
				subs = subs + subs_name[i]

		for i in range(0,len(output_name)):
			if output_name[i] != '"' and output_name[i] != "'" and output_name[i] != '-'and output_name[i] != ':':
				output = output + output_name[i]

		video = '"' + video + '"'
		audio = '"' + audio + '"'
		subs = '"' + subs + '"'
		output = '"' + output + '"'
		cmd = 'ffmpeg -i ' + video + ' -i ' + audio + ' -i ' + subs + ' -c copy ' + output

		os.system(cmd)
		delete = 'del ' + video + ' ' + audio + ' ' + subs
		os.system(delete)

	elif prog == False and cap_true == '2':
		for i in range(0,len(vid_name)):
			if vid_name[i] != '"' and vid_name[i] != "'" and vid_name[i] != '-' and vid_name[i] != ':':
				video = video+vid_name[i]

		for i in range(0,len(audio_name)):
			if audio_name[i] != '"' and audio_name[i] != "'" and audio_name[i] != '-'and audio_name[i] != ':':
				audio = audio + audio_name[i]

		for i in range(0,len(output_name)):
			if output_name[i] != '"' and output_name[i] != "'" and output_name[i] != '-'and output_name[i] != ':':
				output = output + output_name[i]

		video = '"' + video + '"'
		audio = '"' + audio + '"'
		output = '"' + output + '"'

		cmd = 'ffmpeg -i ' + video + ' -i ' + audio +  ' -c copy ' + output
		os.system(cmd)
		delete = 'del ' + video + ' ' + audio
		os.system(delete)

	elif prog == True and cap_true == '1':
		for i in range(0,len(vid_name)):
			if vid_name[i] != '"' and vid_name[i] != "'" and vid_name[i] != '-' and vid_name[i] != ':':
				video = video+vid_name[i]

		for i in range(0,len(subs_name)):
			if subs_name[i] != '"' and subs_name[i] != "'" and subs_name[i] != '-'and subs_name[i] != ':':
				subs = subs + subs_name[i]

		for i in range(0,len(output_name)):
			if output_name[i] != '"' and output_name[i] != "'" and output_name[i] != '-'and output_name[i] != ':':
				output = output + output_name[i]

		video = '"' + video + '"'
		subs = '"' + subs + '"'
		output = '"' + output + '"'
		cmd = 'ffmpeg -i ' + video + ' -i ' + subs + ' -c copy ' + output

		os.system(cmd)
		delete = 'del ' + video + ' ' + subs
		os.system(delete)

	elif prog == True and cap_true == '2':
		return
main()
