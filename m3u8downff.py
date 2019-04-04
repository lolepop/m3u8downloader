import config
import m3u8down
import os

config.outExt = ".ts"
concatFile = m3u8down.start()

os.system("ffmpeg -i {0}.ts -c:a copy -c:v copy {0}.mp4".format(concatFile[:concatFile.rfind(".")]))
os.remove(concatFile)
