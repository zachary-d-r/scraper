import json
from readline import insert_text
import Docs
from time import sleep

doc = Docs.docs(r'1EFAPk_6h6yyO8OsY736bdwS3Kg25RU-D3xx7b4Xc5jw', ['https://www.googleapis.com/auth/documents'])

#doc.insertText("Texas Sheet Metal", i)

key = {"Page Name" : "PN", "Page Title" : "PT", "Meta Description" : "MD", "Live URL" : "LURL", "Content" : "CN"}
keys = list(key)
whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def changeText(n):
    change = False
    i = 0
    cells = doc.getTableCells()
    for cell in cells:
        cellContent = ''.join(filter(whitelist.__contains__, cell["content"][0]["paragraph"]["elements"][0]["textRun"]["content"].split("\n")[0]))
            
        if change == True:
            print(i)
            print(n)
            index = cell["content"][0]["paragraph"]["elements"][0]["startIndex"]

            if i == n: 
                print(f'{cellContent} : {index}')
                
                doc.insertText("Test", index)
                return
            i += 1

        if cellContent in keys: change = True
            
changeText(0)

cells = doc.getTableCells()
content = json.dumps(cells[4], indent=4, sort_keys=True)

with open("test.json", 'w') as f: f.write(content)