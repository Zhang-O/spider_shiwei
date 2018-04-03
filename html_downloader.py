import urllib.request

class HtmlDownloader(object):
	"""docstring for HtmlDownloader"""
	def download(self,url):
		if url is None:
			return None
		response = urllib.request.urlopen(url)
		if response.getcode() != 200:
			return print('request failed')

		return response.read()

			
		