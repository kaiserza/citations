#!/usr/bin/python
import sys
import time
import traceback
import os
import Tkinter
from Tkinter import *
import tkMessageBox
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

top=Tkinter.Tk()
top.geometry("700x500")


var = StringVar()
textbox = Entry(top, textvariable=var)
textbox.focus_set()
textbox.pack(pady=10, padx=10)

def helloCallBack():
    global var, Text

    #THIS USES PYHTHON 2.X NOT 3.X

    querier = scholar.ScholarQuerier()
    settings = scholar.ScholarSettings()
    settings._is_configured = True
    settings.citform = 4
    querier.apply_settings(settings)

    user_input = str(var.get())
    user_input_formatted = '"' + user_input + '"'
    Text.insert(END, "The article you entered is " + user_input_formatted + "\n")

    try:
        
        query = scholar.SearchScholarQuery()

        query.set_phrase("'" + user_input_formatted + "'")
        query.set_num_page_results(10)

        Text.insert(END, "\n\n" + query.get_url() + "\n\n")

        Text.insert(END, "Cert location: " + requests.certs.where() + "\n")

        querier.send_query(query)
        Text.insert(END, querier.get_status() + "\n")

        Text.insert(END, "querier = " + str(querier) + "\n")
        Text.insert(END, "querier.articles length = " + str(len(querier.articles)) + "\n")
        Text.insert(END, "querier.articles.attrs['url_versions'] length = " + str(len(querier.articles[0].attrs['url_versions'])) + "\n")

        page = querier.articles[0].attrs['url_versions'][0]
        page_request = requests.get(page)

        tree = lxml.html.fromstring(page_request.content)
        
        authors_time = tree.xpath('//div[@class="gs_a:nth-child(1)"]/text()')

        sel2 = CSSSelector('div.gs_fl a:nth-child(4)')
        sel_results_2 = sel2(tree)
        match2 = sel_results_2[0]
        match2_href = match2.get('href')
 
        google_intro = "http://scholar.google.com/"
        related_query = google_intro + match2_href
        Text.insert(END, "the query URL of related articles is " + related_query + "\n")

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

        for x in range(2,10):

          #make strings from all elements

          match = all_divs[x]
          match_string = lxml.html.tostring(match)

          title_match = title_div_S[x]
          title_match_string = lxml.html.tostring(title_match) 

          cleantext_title = BeautifulSoup(title_match_string)
          basetext_title = cleantext_title.get_text()
          
          try:
            encoded_title = basetext_title.encode('utf-8')
          # print(basetext_title)
          except Exception, e: 
            continue

          cleantext = BeautifulSoup(match_string)
          basetext = cleantext.get_text()
          Text.insert(END, basetext.encode('utf-8'))

          if '[BOOK][B]' in encoded_title:
            book_title = encoded_title.replace('[BOOK][B]', '')
            Text.insert(END, book_title + "\n")
          elif '[CITATION][C]' in encoded_title:
              citation_title = encoded_title.replace('[CITATION][C]', '')
              Text.insert(END, citation_title + "\n")
          elif '[HTML]' in encoded_title:
              html_title = encoded_title.replace('[HTML]', '')
              Text.insert(END, html_title + "\n")
          elif '[PDF]' in encoded_title:
            pdf_title = encoded_title.replace('[PDF]', '')
            Text.insert(END, pdf_title + "\n")
          else:
              Text.insert(END, encoded_title + "\n")
    except IndexError:
        if len(querier.articles) == 0:
            Text.insert(END, "Sorry, no results. Please try again.")
        else:
            e = sys.exc_info()
            Text.insert(END, str(e[0]) + "\n")
            Text.insert(END, str(e[1]) + "\n")
            t = ''.join(traceback.format_tb(e[2]))
            Text.insert(END, t + "\n")
    except:
        e = sys.exc_info()
        Text.insert(END, str(e[0]) + "\n")
        Text.insert(END, str(e[1]) + "\n")
        t = ''.join(traceback.format_tb(e[2]))
        Text.insert(END, t + "\n")

  
    Text.insert(END, "----------------------------" + "\n")

    Text.insert(END, "Open the word document that has been saved to this folder and copy the text from it, paste it into your paper, and you will have invisibly added 8 citations, which will be indexed in Google Scholar. Overflowing the citation databases will devalue the citation as a commodity and force a reckoning with how scholarship is evaluated today. Thank you!")


    # sel_related_authors = CSSSelector('div.gs_a > a')
    # sel_related_authors_no_link = CSSSelector('div.gs_a')
    # if not sel_related_authors(tree2):
    #   sel_related_authors_result = sel_related_authors_no_link(tree2)
    #   print("nope")
    # else:
    #   sel_related_authors_result = sel_related_authors(tree2)
    # match_related_authors_first = sel_related_authors_result[0].text
    # print("the authors of the first related article are " + match_related_authors_first + "\n")

    # for x in range(2, 10):
    #   match_related_authors_first_inc = sel_related_authors_result[x].text
    #   print(match_related_authors_first_inc)



    #if it returns a cluster, we have to do something




    #print(scholar.citation_export(query2))
    #page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
    #tree = html.fromstring(page.content)





    #below this line is word doc creator
    # document = Document()
    # run = document.add_paragraph().add_run(authors_time)
    # font = run.font
    # font.name = 'Calibri'
    # font.size = Pt(12)
    # document.save('demo.docx')
    


B=Tkinter.Button(top,text="run",command= helloCallBack)
B.pack()
Text=Tkinter.Text(top,height=50)
Text.pack()

Text.insert(END, "Version 1.0.25\n")


top.mainloop()