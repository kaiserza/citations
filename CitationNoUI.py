import sys
import time
import traceback
import os
import scholar
import lxml
from lxml import html
from lxml.cssselect import CSSSelector
import requests
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.shared import RGBColor
from pprint import pprint
from bs4 import BeautifulSoup
import unicodedata
from os.path import expanduser

def runApp(user_input):
    querier = scholar.ScholarQuerier()
    settings = scholar.ScholarSettings()
    settings._is_configured = True
    settings.citform = 4
    querier.apply_settings(settings)

    user_input_formatted = '"' + user_input + '"'
    print("The article you entered is " + user_input_formatted + "\n")

    wordDoc = ""

    try:
        
        query = scholar.SearchScholarQuery()

        query.set_phrase("'" + user_input_formatted + "'")
        query.set_num_page_results(10)

        #----DEBUGGING----
        
        print("\n\n" + query.get_url() + "\n\n")
        print("Cert location: " + requests.certs.where() + "\n")
        

        querier.send_query(query)
        
        #----DEBUGGING----
        
        print(querier.get_status() + "\n")
        print("querier = " + str(querier) + "\n")
        print("querier.articles length = " + str(len(querier.articles)) + "\n")
        print("querier.articles.attrs['url_versions'] length = " + str(len(querier.articles[0].attrs['url_versions'])) + "\n")
        

        page = querier.articles[0].attrs['url_versions'][0]
        
        print("page = " + str(page) + "\n")
        

        os.environ['REQUESTS_CA_BUNDLE'] = requests.certs.where()
        page_request = requests.get(page)

        tree = lxml.html.fromstring(page_request.content)
        
        authors_time = tree.xpath('//div[@class="gs_a:nth-child(1)"]/text()')

        sel2 = CSSSelector('div.gs_fl a:nth-child(4)')
        sel_results_2 = sel2(tree)
        match2 = sel_results_2[0]
        match2_href = match2.get('href')

        google_intro = "http://scholar.google.com/"
        related_query = google_intro + match2_href
        
        #---MORE DEBUGGING----
        
        print("the query URL of related articles is " + related_query + "\n")
        

        print("Related articles are: \n \n")

        related_page_request = requests.get(related_query)
        tree2 = html.fromstring(related_page_request.content)

        related_author_div = CSSSelector('div.gs_a')
        related_author_link_div = CSSSelector('div.gs_a > a')
        related_author_div_S = related_author_div(tree2)
        related_author_link_div_S = related_author_link_div(tree2)
        all_divs = related_author_div_S + related_author_link_div_S

        title_div = CSSSelector('.gs_rt')
        title_div_S = title_div(tree2)

        list_of_annoying_shit = ['[BOOK]', '[CITATION]', '[HTML]', '[BOOK][B]', '[CITATION][C]']

        #initialize creation of word document

        for x in range(2,10):

          #make strings from all elements

          match = all_divs[x]
          match_string = lxml.html.tostring(match)

          title_match = title_div_S[x]
          title_match_string = lxml.html.tostring(title_match) 

          cleantext_title = BeautifulSoup(title_match_string)
          basetext_title = cleantext_title.get_text()
          
          try:
            encoded_title = remove_control_characters(basetext_title).decode('utf-8').encode('utf-8')
          # print(basetext_title)
          except Exception, e: 
            continue

          cleantext = BeautifulSoup(match_string)
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
        if len(querier.articles) == 0:
            print("Sorry, no results. Please try again.")
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

    print("Open the word document that has been saved to this folder and copy the text from it, paste it into your paper, and you will have invisibly added 8 citations, which will be indexed in Google Scholar. Overflowing the citation databases will devalue the citation as a commodity and force a reckoning with how scholarship is evaluated today. Thank you! \n \n")



def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

if __name__ == "__main__":
    user_input = raw_input("Search term: ")
    runApp(user_input)
