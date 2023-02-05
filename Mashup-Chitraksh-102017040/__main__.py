from pytube import YouTube
from pydub import AudioSegment
import urllib.request
import re
import os
import sys


def main():
    delete_after_use = True

    if len(sys.argv) < 2:
        x = "marshmello" + "songs"
        output_name = '102017040-output.mp3'
        n = 5
        y = 20
    else:
        x = sys.argv[1]
        x = x.replace(' ','') + "songs"
        n = int(sys.argv[2])
        y = int(sys.argv[3])
        output_name = sys.argv[4]

    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    for i in range(n):
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i]) 
        mp4files = yt.streams.filter(only_audio=True).first().download(filename='tempaudio-'+str(i)+'.mp3')

    if os.path.isfile("tempaudio-0.mp3"):
        fin_sound = AudioSegment.from_file("tempaudio-0.mp3")[0:y*1000]
    for i in range(1,n):
        aud_file = str(os.getcwd()) + "/tempaudio-"+str(i)+".mp3"
        fin_sound = fin_sound.append(AudioSegment.from_file(aud_file)[0:y*1000],crossfade=1000)
  
    fin_sound.export(output_name, format="mp3")
    if delete_after_use:
        for i in range(n):
            os.remove("tempaudio-"+str(i)+".mp3")


if __name__ == '__main__':
	main()