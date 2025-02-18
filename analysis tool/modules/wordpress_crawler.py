from bs4 import BeautifulSoup
import requests


wordpress_plugin_main_url = 'https://ko.wordpress.org/plugins/browse/'


class WPCrawlerByBlocks:
    def __init__(self):
        self.url = wordpress_plugin_main_url + 'blocks/'

class WPCralwerByBeta:
    def __init__(self):
        self.url = wordpress_plugin_main_url + 'beta/'

class WPCrawlerByPopular:
    def __init__(self):
        self.url = wordpress_plugin_main_url + 'popular/'