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
	# print(user_input_formatted)
	print("the article you entered is: " + user_input)

	wordDoc = ""

	try:

		user_article_URL = 'http://scholar.google.com/scholar?hl=en&q='+user_input_formatted
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
		#second page of results below
		related_query_page2 = related_query_page1.replace("q=related:", "start=10&q=related:")
		print("page 2 of queries is " + related_query_page2 + "\n")

		#below is the code that grabs the content of the first page of "related articles"
		related_page_request = requests.get(related_query_page1)
		tree2 = html.fromstring(related_page_request.content)

		#below is the code that grabs the content of the second page of "related articles"
		related_page2_request = requests.get(related_query_page2)
		tree3 = html.fromstring(related_page2_request.content)

		print("related articles are: \n \n")

		related_author_div = CSSSelector('div.gs_a')
		related_author_link_div = CSSSelector('div.gs_a > a')
		related_author_div_S = related_author_div(tree2)
		related_author_link_div_S = related_author_link_div(tree2)
		all_divs = related_author_div_S + related_author_link_div_S

		title_div = CSSSelector('.gs_rt')
		title_div_S = title_div(tree2)

		list_of_annoying_shit = ['[BOOK]', '[CITATION]', '[HTML]', '[BOOK][B]', '[CITATION][C]']

		for x in range(1,10):

			#make strings from all elements

			match = all_divs[x]
			match_string = lxml.html.tostring(match)
			# print(match_string)

			title_match = title_div_S[x]
			title_match_string = lxml.html.tostring(title_match)
			# print(title_match_string) 

			cleantext_title = BeautifulSoup(title_match_string, "lxml")
			basetext_title = cleantext_title.get_text()
			# print(basetext_title)

			# The try statement below is not working... my temporary workaround is below that
			# try:
			# 	encoded_title = remove_control_characters(basetext_title).decode('utf-8').encode('utf-8')
			# 	print(encoded_title)
			# except Exception as e: 
			# 	continue

			encoded_title = basetext_title

			cleantext = BeautifulSoup(match_string, "lxml")
			basetext = cleantext.get_text()
			print(basetext)

			wordDoc += basetext + "\n"

			if '[BOOK][B]' in encoded_title:
			  book_title = encoded_title.replace('[BOOK][B]', '')
			  print(book_title + "\n")
			  wordDoc += book_title + "\n"
			elif '[CITATION][C]' in encoded_title:
			  citation_title = encoded_title.replace('[CITATION][C]', '')
			  print(citation_title + "\n")
			  wordDoc += citation_title + "\n"
			elif '[HTML]' in encoded_title:
			  html_title = encoded_title.replace('[HTML]', '')
			  print(html_title + "\n")
			  wordDoc += html_title + "\n"
			elif '[PDF]' in encoded_title:
			  pdf_title = encoded_title.replace('[PDF]', '')
			  print(pdf_title + "\n")
			  wordDoc += pdf_title + "\n"
			else:
			  print(encoded_title + "\n")
			  wordDoc += encoded_title + "\n\n"

	except IndexError:
		print("meow")
		if not tree2:
			print("Sorry, no results")
			# HEY GABOOSH HELP -- need to figure out new error handler because scholar was doing it by number of articles
		else:
			e = sys.exc_info()
			print(str(e[0]) + "\n")
			print(str(e[1]) + "\n")
			t = ''.join(traceback.format_tb(e[2]))
			print(t + "\n")

	except:
	    e = sys.exc_info()
	    print(str(e[0]) + "\n")
	    print(str(e[1]) + "\n")
	    t = ''.join(traceback.format_tb(e[2]))
	    print(t + "\n")


	print("----------------------------" + "\n")


def remove_control_characters(s):
	return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

if __name__ == "__main__":
	user_input = input("Search term: ")
	user_input_formatted = user_input.replace(" ", "%20")
	runApp(user_input, user_input_formatted)



