#! python3

"""this is ck101 module for comiccrawler

Ex:
	http://comic.ck101.com/comic/8373
	
"""

import re

from urllib.parse import urljoin

from ..core import Episode
from ..error import SkipEpisodeError

domain = ["comic.ck101.com"]
name = "卡提諾"

def get_title(html, url):
	return re.search("<h1 itemprop=\"name\">(.+?)</h1>", html).group(1)
	
def get_episodes(html, url):
	s = []
	i = html.index("漫畫列表")
	j = html.index("<!--new upsdate-->")
	
	for match in re.finditer('href="(.+?)" title="(.+?)"', html[i:j]):
		ep_url, title = match.groups()
		s.append(Episode(title, urljoin(url, ep_url)))
	return s[::-1]
			
def get_images(html, url):
	"""
	Since ck101 has lots of bugs, something like this: 
		http://comic.ck101.com/vols/9206635/1
	or this:
		http://comic.ck101.com/vols/9285077/15
	we raise SkipEpisodeError if getting losted page
	"""
	try:
		pic = re.search("'defualtPagePic' src=\"(.+?)\"", html).group(1)
		return pic
	except AttributeError:
		ex = re.search("李組長眉頭一皺，快翻下一頁→", html)
		if ex:
			raise SkipEpisodeError
		else:
			raise
			
def get_next_page(html, url):
	base = re.search("(https?://[^/]+)", url).group(1)
	
	un = re.search("ref=\"([^\"]+?)\" title='下一頁'", html)
	if un:
		return base + un.group(1)

	r = re.search("<a href=\"(.+?)\" class=\"nextPageButton\" title=\"下一頁\">", html)
	if r:
		return base + r.group(1)
