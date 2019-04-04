Fast m3u8 downloader with concurrent download and custom http referer support


Usage:
```
python m3u8down.py m3u8Url refererUrl
```
Arguments:
- m3u8Url: direct url to m3u8 file (eg. https://example.com/test.m3u8)
- refererUrl (optional): url to website of origin or url referrer described in captured network traffic (eg. https://example.com)  

Dependencies:
- gevent

Play around with the ```maxSimultaneous``` variable if too many downloads at once causes errors