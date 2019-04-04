import os
import urllib.request
from gevent import monkey
from gevent.pool import Pool
import shutil
import sys
import time
import config


dir = "tmp"

monkey.patch_all()

links = []
fn = []

def download(link, attempt=config.maxRetries):
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
			time.sleep(abs(attempt - config.maxRetries)*5/config.maxRetries)
			return download(link, attempt-1)


def start():
	if len(sys.argv) < 2:
		sys.exit("no url provided")
		
		
	if not sys.argv[1].endswith(".m3u8"):
		sys.exit("invalid url")
		

	opener = urllib.request.build_opener()
	opener.addheaders = [("Referer", sys.argv[2] if sys.argv[2:] else config.defaultReferer)]
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


	pool = Pool(config.maxSimultaneous)
	for link in links:
		pool.spawn(download, link)
	pool.join()

	export = tmpDownload[:tmpDownload.rfind(".")] + config.outExt
	with open(export, "wb+") as f:
		for filename in fn:
			with open(dir + "/" + filename, "rb") as h:
				shutil.copyfileobj(h, f)

	shutil.rmtree(dir)
	print("done")
	
	return export 

	
if __name__ == "__main__":
	start()