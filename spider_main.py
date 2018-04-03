#引进4个模块，这4个模块是按功能来的
# from baike_spider import url_manager   
# from baike_spider import url_downloader
# from baike_spider import url_parser
# from baike_spider import url_outputer
import url_manager   
import html_downloader
import html_parser
import html_outputer

class SpiderMain(object):
	def __init__(self):
		#分别对4个模块中的类进行实例化创建对象
		self.urls = url_manager.UrlManager()
		self.downloader = html_downloader.HtmlDownloader()
		self.parser = html_parser.HtmlParser()
		self.outputer = html_outputer.HtmlOutputer()

	def craw(self,root_url):
		count = 1
		self.urls.add_new_url(root_url)
		while self.urls.has_new_url():
			try:
				new_url = self.urls.get_new_url()
				html_content = self.downloader.download(new_url)
				new_urls,new_data = self.parser.parse(new_url,html_content)
				self.urls.add_new_urls(new_urls)
				self.outputer.collect_data(new_data)

				if count == 1000:
					break
				count = count + 1

			except Exception as f:
				print('craw failed',f)

		self.outputer.output_html()

if __name__ == '__main__':
	root_url = "http://baike.baidu.com/view/21087.htm"
	obj_spider = SpiderMain()
	obj_spider.craw(root_url)













































