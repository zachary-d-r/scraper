import Docs
import imports.Scrape as Scrape
import json
from time import sleep

doc = Docs.docs(r'1EFAPk_6h6yyO8OsY736bdwS3Kg25RU-D3xx7b4Xc5jw', ['https://www.googleapis.com/auth/documents'])  # Create doc object
scraper = Scrape.scrape(r"https://github.com/")  # Create scraper object

keys = ["Page Name", "Page Title", "Meta Description", "Live URL"]  # The Rows we need to fill out (except for content)
whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')  # Used to filter garbage when reading rows


def insertInformation(content:list):
    """
    Function to insert fill out all the rows except for the content one.

    Parameters:
    ===========
        Content : list
            The content that you want to put into the cells in the form of a list. Each index corresponds to the row it will be placed in (see table below).

            0 - Page Name
            1 - Live URL
            2 - Page Title
            3 - Meta Description
    """

    i = 0  # Iterator to go through the content list
    cells = doc.getTableCells()  # Get all the cells in the table
    offset = 0  # The index offset

    # Loop through each cell, check it's content and insert text based on where it is
    for cell in range(len(cells)):
        cellContent = ''.join(filter(whitelist.__contains__, cells[cell]["content"][0]["paragraph"]["elements"][0]["textRun"]["content"].split("\n")[0]))  # Get current cell content

        # Check if the current cell content is a row I should fill out
        if cellContent in keys:
            index = cells[cell+1]["content"][0]["paragraph"]["elements"][0]["startIndex"] + offset  # Get the start index of the next cell
            toChangeContent = ''.join(filter(whitelist.__contains__, cells[cell+1]["content"][0]["paragraph"]["elements"][0]["textRun"]["content"].split("\n")[0]))  # Get content of the next cell (Used for debugging)

            print(f"{toChangeContent} : {index}")  # Print some info

            doc.insertText(content[i], index=index)  # Insert the text
            offset += len(content[i])  # Add the offset

            i += 1  # Iterate i so the next peice of content can go in the doc

    
def getContentIndex():

    doc.connectToGoogle()  # Reload doc

    # Find the index where we need to insert text
    index = 0

    cells = doc.getTableCells()  # Get all the cells in the table
    for cell in range(len(cells)):
        cellContent = ''.join(filter(whitelist.__contains__, cells[cell]["content"][0]["paragraph"]["elements"][0]["textRun"]["content"].split("\n")[0]))  # Get current cell content
        
        # Find the index
        if cellContent == "Content":
            index = cells[cell+1]["content"][0]["paragraph"]["elements"][0]["startIndex"]
            break
    
    return index


def main():          
    insertInformation([scraper.h1, scraper.URL, scraper.title, scraper.metaDescription])  # Insert the first few rows
    doc.insertFormattedContent(getContentIndex(), scraper.content)  # Insert the content row

# #  JSON dumping the google doc:
# cells = doc.getTableCells()
# content = json.dumps(cells, indent=4, sort_keys=True)

# with open("test.json", 'w') as f: f.write(content)

main()