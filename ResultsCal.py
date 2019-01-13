from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from dateutil.parser import parse
# import datefinder
import pandas as pd
import datetime
import requests
import numpy as np
import re
import uuid
# import dateparser


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 5
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


def GetDate(title, url):

    title = title.lower()

    match = re.search(
        r'(ended \d{1,2}(st|nd|rd|th)?[\/ ]*(\d{2}|january|jan|february|feb|march|mar|april|apr|may|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec)[\/ ]*\d{2,4})', title)

    if match is not None:
        results_date = parse(match.group(), fuzzy=True)
        return results_date
    else:
        filename = str(uuid.uuid4())
        downloadPDF(url, filename)
        pdf_text = convert_pdf_to_txt("files/" + filename + ".pdf").replace(
            '\n', ' ').replace('\r', '').replace(',', '').replace('.', '')
        # print(pdf_text)
        matches = re.findall(
            r'(ended \d{1,2}(st|nd|rd|th)?[\/ ]*(\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]*\d{2,4})', pdf_text)

        # matches = datefinder.find_dates(pdf_text, source=True, strict=True)
        date_list = []
        if len(matches) > 0:
            for match in matches:
                print(match)
                date_list.append(parse(match[0], fuzzy=True))
            results_date = max(date_list)
            return results_date
        else:
            return "(error)"


def downloadPDF(URL, file_uuid):
    r = requests.get(URL, stream=True)
    with open('files/' + file_uuid + '.pdf', 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)


if __name__ == '__main__':
    results_date = GetDate(
        "", "http://www3.hkexnews.hk/listedco/listconews/GEM/2018/1218/GLN20181218027.pdf")
    print(str(results_date))
    results_date = GetDate(
        "ANNOUNCEMENT OF FIRST QUARTERLY RESULTS FOR THE THREE MONTHS ENDED 31 OCTOBER 2018", "http://www3.hkexnews.hk/listedco/listconews/GEM/2018/1213/GLN20181213029.pdf")
    print(str(results_date))
    results_date = GetDate(
        "Unaudited Results for the Nine Months Ended 30th November 2018", "http://www3.hkexnews.hk/listedco/listconews/SEHK/2018/1220/LTN20181220690.pdf")
    print(str(results_date))
