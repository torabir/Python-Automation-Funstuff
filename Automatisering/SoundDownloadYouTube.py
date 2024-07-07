#!/usr/bin/python3.5

#example usage: mp3ytclipper.py "https://www.youtube.com/watch?v=MgxK5vm6lvk" later 44.3 46.3

import sys, re, subprocess, youtube_dl, os

if len(sys.argv) != 5:
	print("usage: mp3ytclipper.py <youtubeurl> <outfilename> <starttime> <endtime>")
	exit()

def gettime(timestr):
	parts = timestr.split(":")
	if len(parts) == 2:
		return (int(parts[0]) * 60) + float(parts[1])
	if len(parts) == 1:
		return float(parts[0])
	raise ValueError("Only minutes:seconds supported")

def runcommand(commandarray):
	return subprocess.check_output(commandarray, stderr=subprocess.STDOUT).decode("utf-8")

url = sys.argv[1]
outfile = sys.argv[2] + ".mp3"
start = gettime(sys.argv[3])
duration = gettime(sys.argv[4]) - start

options = {
	'format': 'bestaudio/best',
	'extractaudio' : True,
	'audioformat' : "mp3",
	'outtmpl': 'yt_audio/%(id)s.mp3',
	'noplaylist' : True,
	'nooverwrites': True,
}
with youtube_dl.YoutubeDL(options) as ydl:
	video_id = ydl.extract_info(url, download=False).get("id", None)
	video_file = "yt_audio/{}.mp3".format(video_id)
	if not os.path.exists(video_file):
		ydl.download([url])

fadeduration = 0.25
fadefilter = "afade=t=in:ss=0:d={0},afade=t=out:st={1}:d={0}".format(fadeduration, duration - fadeduration)

print("converting/cropping")
runcommand(["ffmpeg", "-ss", str(start), "-t", str(duration), "-y", "-i", video_file, "-af", fadefilter, outfile ])

print("playing...")
runcommand(["open", outfile])