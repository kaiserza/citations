import sys
import time
import traceback
import os
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.shared import RGBColor
from pprint import pprint
import requests
import requests
import lxml
import lxml.html
from lxml import html
from lxml.cssselect import CSSSelector
import cssselect
from bs4 import SoupStrainer, BeautifulSoup
import unicodedata
from os.path import expanduser

#can we use the first two pages of google search results?
#start=0 vs. start=10


def runApp(user_input, user_input_formatted):
	print(user_input_formatted)
	print("the article you entered is: " + user_input)

	wordDoc = ""

	try:

		user_article_URL = 'http://scholar.google.se/scholar?hl=en&q='+user_input_formatted
		r = requests.get(user_article_URL)
		print(user_article_URL)
		tree = lxml.html.fromstring(r.text)

		#this is getting the link to the related articles
		sel2 = CSSSelector('div.gs_fl a:nth-child(4)')
		sel_results_2 = sel2(tree)
		match2 = sel_results_2[0]
		match2_href = match2.get('href')

		#this formats the url of the related articles to the one you cited
		google_intro = "https://scholar.google.com/"
		related_query_page1 = google_intro + match2_href
		print("the query URL of related articles is " + related_query_page1 + "\n")
		related_query_page2 = related_query_page1.replace("q=related:", "start=10&q=related:")
		print("page 2 of queries is " + related_query_page2 + "\n")

		#below is the code that grabs the page of "related articles"
		related_page_request = requests.get(related_query_page1)
		tree2 = html.fromstring(related_page_request.content)

	except IndexError:
		print("meow")
		#need to figure out new error handler because scholar was doing it by number of articles

	except:
	        e = sys.exc_info()
	        print(str(e[0]) + "\n")
	        print(str(e[1]) + "\n")
	        t = ''.join(traceback.format_tb(e[2]))
	        print(t + "\n")

if __name__ == "__main__":
    user_input = input("Search term: ")
    user_input_formatted = user_input.replace(" ", "%20")
    runApp(user_input, user_input_formatted)



