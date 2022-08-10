from copy import deepcopy
from urllib.parse import urldefrag
from docx import Document
from docx.shared import Pt
import imports.Scrape as Scrape
import imports.Doc as Doc
from flask import Flask, render_template

def getURLs(file):
    URLs = []
    with open(file, 'r') as f:
        for URL in f.readlines(): URLs.append(URL.split("\n")[0])
    
    return URLs

def getContent(urls):
    content = []
    for url in urls:
        s = Scrape.scrape(url)
        content.append([s.h1, s.URL, s.title, s.metaDescription])
    
    return content

        
def main():

    urlFile = r"URL.txt"
    URLS = getURLs(urlFile)
    content = getContent(URLS)

    doc = Doc.document(len(URLS))

    doc.insertContent(content)

    doc.save("test.docx")

main()