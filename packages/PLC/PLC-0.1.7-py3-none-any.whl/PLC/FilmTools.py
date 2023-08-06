from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import subprocess
import os

def Trim(Filename, From, To, Output):
    ffmpeg_extract_subclip(Filename, From, To, targetname=Output)
def Concatenate(Files, Output):
    file = open('list.txt', 'w')
    Videos = []
    for File in Files:
        Videos.append("file '{}'".format(File))
    file.write('\n'.join(Videos) + '\n')
    file.close()
    command = "ffmpeg -f concat -i list.txt -c copy {}".format(Output).split(
        ' ')
    subprocess.call(command)
    os.remove('list.txt')