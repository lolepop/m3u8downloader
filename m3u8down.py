import os
import urllib.request
from gevent import monkey
from gevent.pool import Pool
import shutil
import sys
import time

outExt = ".mp4"
defaultReferer = "" # only needed for websites that return an error if accessed externally (like error 403)
maxSimultaneous = 50 # too many will overload the filesystem
maxRetries = 5

dir = "tmp"

monkey.patch_all()

links = []
fn = []

if len(sys.argv) < 2:
	sys.exit("no url provided")
	
	
if not sys.argv[1].endswith(".m3u8"):
	sys.exit("invalid url")
	

opener = urllib.request.build_opener()
opener.addheaders = [("Referer", sys.argv[2] if sys.argv[2:] else defaultReferer)]
urllib.request.install_opener(opener)

tmpDownload = sys.argv[1][sys.argv[1].rfind('/')+1:]
urllib.request.urlretrieve(sys.argv[1], tmpDownload)

with open(tmpDownload, "r") as f:
	for line in f:
		if line.strip().endswith(".ts"):
			links.append(line.strip())

os.remove(tmpDownload)

if not os.path.isdir(dir):
	os.mkdir(dir)
	
def download(link, attempt=maxRetries):

	filename = link[link.rfind('/')+1:]
	print(filename)
	
	fn.append(filename)
	
	try:
		urllib.request.urlretrieve(link, dir + "/" + filename)
	except Exception as e:
		print(e)
		if attempt == 0:
			sys.exit("download error on: " + filename)
		else:
			time.sleep(abs(attempt - maxRetries)*5/maxRetries)
			return download(link, attempt-1)


pool = Pool(maxSimultaneous)
for link in links:
	pool.spawn(download, link)
pool.join()


with open(tmpDownload[:tmpDownload.rfind(".")] + outExt, "wb+") as f:
	for filename in fn:
		with open(dir + "/" + filename, "rb") as h:
			shutil.copyfileobj(h, f)

shutil.rmtree(dir)
print("done")
