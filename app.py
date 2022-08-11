from copy import deepcopy
from urllib.parse import urldefrag
from docx import Document
from docx.shared import Pt
import imports.Scrape as Scrape
import imports.Doc as Doc
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from Semrush import Semrush

app = Flask(__name__)
CORS(app)

def getURLs(urls):
    """
    Correctly format the URLS inputted from the website

    Returns:
    ========
        r : list
            A list of all the URLS
    """

    r = []

    t = urls.split(", ")
    for i in t:
        if i == '' or i == ' ': continue
        r.append(i)

    return r
    

def getContent(urls):
    """
    Get the content for all rows

    Returns:
    ========
        content : list
            correnctly formatted list of the first few rows in the content doc
        onPage : list
            correctly formatted list of the onpage content from the website.
    """

    global s
    
    with open("key.txt", "r") as f: key = f.read().strip()

    content = []
    onPage = []
    semrush = Semrush.semrush(key)

    for url in urls:
        s = Scrape.scrape(url)
        semrushContent = semrush.getContent(url)

        content.append([s.h1, s.URL, s.title, s.metaDescription, semrushContent[1], semrushContent[0]])

        onPage.append(s.getContent())
    
    return content, onPage


@app.route("/url", methods=["POST"])
def createDoc():
    """
    Create a doc with URLS given by user
    """

    global doc

    inputJson = request.get_json(force=True)  # Get the JSON from the user
    #print(dict(inputJson))     
    URLS = getURLs(inputJson["text"])  # Get the URLs from the JSON
    content, onPage = getContent(URLS)  # Get the content

    doc = Doc.document(len(URLS))  # Create our doc

    # Put content in the doc
    doc.insertContent(content) 
    doc.insertFormatedContent(onPage)

    return jsonify({"text":content})

@app.route("/path", methods=["POST"])
def saveFile():
    """
    Save the doc
    """

    inputJson = request.get_json(force=True)  # Get JSON from user
    PATH = inputJson["text"]  # Get the path

    doc.save(str(PATH))  # Save the doc

    return inputJson