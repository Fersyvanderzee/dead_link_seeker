import urllib
from openpyxl import Workbook

from urllib import request, parse
from urllib.parse import urlparse, urljoin
from urllib.request import Request
from html.parser import HTMLParser
from collections import deque

url = # url to be checked for dead links.
wb = Workbook()
ws = wb.create_sheet("Failed urls")
ws.title = "Failed urls"



search_attrs = set(['href', 'src'])
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

class LinkParser(HTMLParser):
    print('LinkParser started')
    def __init__(self, home):
        super().__init__()
        self.home = home
        self.checked_links = set()
        self.pages_to_check = deque()
        self.pages_to_check.appendleft(home)
        self.scanner()

    def scanner(self):
        while self.pages_to_check:
            page = self.pages_to_check.pop()

            req = Request(page, headers={'User-Agent': agent})
            res = request.urlopen(req)

            if 'html' in res.headers['content-type']:
                with res as f:

                    body = f.read().decode('utf-8', errors='ignore')
                    self.feed(body)

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] in search_attrs and attr[1] not in self.checked_links:
                self.checked_links.add(attr[1])
                self.handle_link(attr[1])

    def handle_link(self, link):
        if not bool(urlparse(link).netloc):
            link = urljoin(self.home, link)

        try:
            req = Request(link, headers={'User-Agent': agent})
            status = request.urlopen(req).getcode()

        except urllib.error.HTTPError as e:
            print(f'HTTPError: {e.code} - {link}')
        except urllib.error.URLError as e:
            print(f'URLError: {e.reason} - {link}')
        except ValueError as ve:
            print(f'Wrong value.')

        else:
            print(f'{status} - {link}')

        if self.home in link:
            self.pages_to_check.appendleft(link)

LinkParser(url)
print()
print('done scanning')