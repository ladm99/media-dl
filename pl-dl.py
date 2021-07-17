from pytube import YouTube
from pytube import Playlist
import os
import subprocess
from dl import adapt, cap, mux, fix_text


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