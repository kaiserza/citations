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
from PyQt4 import QtCore, QtGui
from mainwindow import Ui_MainWindow
import unicodedata
from os.path import expanduser

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # here connect to slots
        QtCore.QObject.connect(self.ui.run_search,QtCore.SIGNAL("clicked()"), self.run_search_script)
        self.ui.search_term.clearFocus()
        self.ui.search_term.returnPressed.connect(self.ui.run_search.click)
    def run_search_script(self):
        search_results = self.ui.search_results
        search_results.clear()

        #THIS USES PYHTHON 2.X NOT 3.X

        querier = scholar.ScholarQuerier()
        settings = scholar.ScholarSettings()
        settings._is_configured = True
        settings.citform = 4
        querier.apply_settings(settings)

        user_input = unicode(self.ui.search_term.text())
        user_input_formatted = '"' + user_input + '"'
        search_results.appendPlainText("The article you entered is " + user_input_formatted + "\n")

        wordDoc = ""

        try:
            
            query = scholar.SearchScholarQuery()

            query.set_phrase("'" + user_input_formatted + "'")
            query.set_num_page_results(10)

            #----DEBUGGING----
            """
            search_results.appendPlainText("\n\n" + query.get_url() + "\n\n")
            search_results.appendPlainText("Cert location: " + requests.certs.where() + "\n")
            """

            querier.send_query(query)
            
            #----DEBUGGING----
            """
            search_results.appendPlainText(querier.get_status() + "\n")
            search_results.appendPlainText("querier = " + str(querier) + "\n")
            search_results.appendPlainText("querier.articles length = " + str(len(querier.articles)) + "\n")
            search_results.appendPlainText("querier.articles.attrs['url_versions'] length = " + str(len(querier.articles[0].attrs['url_versions'])) + "\n")
            """

            page = querier.articles[0].attrs['url_versions'][0]
            """
            search_results.appendPlainText("page = " + str(page) + "\n")
            """

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
            """
            search_results.appendPlainText("the query URL of related articles is " + related_query + "\n")
            """

            search_results.appendPlainText("Related articles are: \n \n")

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
            document = Document()

            name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', "Demo.docx",filter ="docx (*.docx *.)")

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
              search_results.appendPlainText(basetext)

              wordDoc += basetext + "\n"

              if '[BOOK][B]' in encoded_title:
                book_title = encoded_title.replace('[BOOK][B]', '')
                search_results.appendPlainText(book_title + "\n")
                wordDoc += book_title + "\n"
              elif '[CITATION][C]' in encoded_title:
                citation_title = encoded_title.replace('[CITATION][C]', '')
                search_results.appendPlainText(citation_title + "\n")
                wordDoc += citation_title + "\n"
              elif '[HTML]' in encoded_title:
                html_title = encoded_title.replace('[HTML]', '')
                search_results.appendPlainText(html_title + "\n")
                wordDoc += html_title + "\n"
              elif '[PDF]' in encoded_title:
                pdf_title = encoded_title.replace('[PDF]', '')
                search_results.appendPlainText(pdf_title + "\n")
                wordDoc += pdf_title + "\n"
              else:
                search_results.appendPlainText(encoded_title + "\n")
                wordDoc += encoded_title + "\n\n"

            saveToWordDoc(document, wordDoc)
            document.save(str(name))
        except IndexError:
            if len(querier.articles) == 0:
                search_results.appendPlainText("Sorry, no results. Please try again.")
            else:
                e = sys.exc_info()
                search_results.appendPlainText(str(e[0]) + "\n")
                search_results.appendPlainText(str(e[1]) + "\n")
                t = ''.join(traceback.format_tb(e[2]))
                search_results.appendPlainText(t + "\n")
        except:
            e = sys.exc_info()
            search_results.appendPlainText(str(e[0]) + "\n")
            search_results.appendPlainText(str(e[1]) + "\n")
            t = ''.join(traceback.format_tb(e[2]))
            search_results.appendPlainText(t + "\n")

      
        search_results.appendPlainText("----------------------------" + "\n")

        search_results.appendPlainText("Open the word document that has been saved to this folder and copy the text from it, paste it into your paper, and you will have invisibly added 8 citations, which will be indexed in Google Scholar. Overflowing the citation databases will devalue the citation as a commodity and force a reckoning with how scholarship is evaluated today. Thank you! \n \n")

def saveToWordDoc(document, docText):
  run = document.add_paragraph().add_run(docText)
  font = run.font
  font.name = 'Calibri'
  font.size = Pt(4)
  font.color.rgb = RGBColor(0xff, 0xff, 0xff)


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())