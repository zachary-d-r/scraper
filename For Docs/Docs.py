from __future__ import print_function
import json
from time import sleep

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class docs:

    h2Request = [
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': 100,
                    'endIndex': 120
                },
                'textStyle': {
                    'weightedFontFamily': {
                        'fontFamily': 'Arial'
                    },
                    'fontSize': {
                        'magnitude': 20,
                        'unit': 'PT'
                    },
                    'foregroundColor': {
                        'color': {
                            'rgbColor': {
                                'blue': 0.0,
                                'green': 0.0,
                                'red': 0.0
                            }
                        }
                    }
                },
                'fields': 'foregroundColor,weightedFontFamily,fontSize'
            }
        }
    ]

    h3Request = [
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': 6,
                    'endIndex': 10
                },
                'textStyle': {
                    'weightedFontFamily': {
                        'fontFamily': 'Arial'
                    },
                    'fontSize': {
                        'magnitude': 16,
                        'unit': 'PT'
                    },
                    'foregroundColor': {
                        'color': {
                            'rgbColor': {
                                'blue': 0.0,
                                'green': 0.0,
                                'red': 0.0
                            }
                        }
                    }
                },
                'fields': 'foregroundColor,weightedFontFamily,fontSize'
            }
        }
    ]

    pRequest = [
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': 6,
                    'endIndex': 10
                },
                'textStyle': {
                    'weightedFontFamily': {
                        'fontFamily': 'Arial'
                    },
                    'fontSize': {
                        'magnitude': 11,
                        'unit': 'PT'
                    },
                    'foregroundColor': {
                        'color': {
                            'rgbColor': {
                                'blue': 0.0,
                                'green': 0.0,
                                'red': 0.0
                            }
                        }
                    }
                },
                'fields': 'foregroundColor,weightedFontFamily,fontSize'
            }
        }
    ]


    def __init__(self, documentID, scopes):
        self.SCOPES = scopes  # Permisions
        self.DOCUMENT_ID = documentID  # Document ID of the document you want to edit

        self.connectToGoogle()

    def connectToGoogle(self):
        """
        Connect to users google account and print the title of the document along with some other information
        Code from: https://developers.google.com/docs/api/quickstart/python

        Returns:
        ========
            service : i have no idea
                The variable used for editing the doc. It is like the instance of the api
        """

        creds = None

        """
        The file token.json stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.
        """
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            self.service = build('docs', 'v1', credentials=creds)

            # Retrieve the documents contents from the Docs service.
            self.document = self.service.documents().get(documentId=self.DOCUMENT_ID).execute()

            print('The title of the document is: {}'.format(self.document.get('title')))
        except HttpError as err:
            print(err)

            print(type(self.service))


    def insertText(self, text:str, index):
        """
        Insert text into the document that you want to edit

        Parameters:
        ===========
            text : str
                The text you want to put into the file
            index : int
                The index you want to insert the text into

        Returns:
        ========
            result : also have no idea
                It just seemed right to return it
        """

        # JSON of text to insert
        requests = [
                {
                    'insertText': {
                        'location': {
                            'index': index,
                        },
                        'text': text
                    }
                }
            ]

        result = self.service.documents().batchUpdate(documentId=self.DOCUMENT_ID, body={'requests': requests}).execute()
        return result

    # Return the google doc as a json
    def getDocJson(self):
        return self.document.get('body').get('content')

    # Return all the cells of the table
    def getTableCells(self):
        totalCells = []
        for value in self.document.get('body').get('content'):

            table = value.get('table') if 'table' in value else 0
            if table == 0:
                continue

            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    totalCells.append(cell)

        return totalCells


    def insertFormattedContent(self, index, content):
        """
        Function to insert and format the content

        Parameters:
        ===========
            index : int
                Start index of the row you want to insert into

            content : soup.find_all()
                The content with the tag label.
        """

        # creating a list of all common heading tags
        i = 0
        for tag in content:

            print(tag.name + ' -> ' + tag.text.strip())

            tagName = tag.name
            text = tag.text

            if tagName == "h2": 

                self.insertText(f"{text}", index=index)

                self.h2Request[0]["updateTextStyle"]["range"]["startIndex"] = index
                self.h2Request[0]["updateTextStyle"]["range"]["endIndex"] = index + len(f"{text}\n\n")

                self.insertText("\n\n", index)

                index += len(f"{text}\n\n")

                result = self.service.documents().batchUpdate(
                    documentId=self.DOCUMENT_ID, body={'requests': self.h2Request}).execute()

            elif tagName == "h3": 

                self.insertText(f"{text}", index=index)

                self.h3Request[0]["updateTextStyle"]["range"]["startIndex"] = index
                self.h3Request[0]["updateTextStyle"]["range"]["endIndex"] = index + len(f"{text}\n\n")

                self.insertText("\n\n", index)

                index += len(f"{text}\n\n")

                result = self.service.documents().batchUpdate(
                    documentId=self.DOCUMENT_ID, body={'requests': self.h3Request}).execute()

            elif tagName == "p": 

                self.insertText(f"{text}", index=index)

                self.pRequest[0]["updateTextStyle"]["range"]["startIndex"] = index
                self.pRequest[0]["updateTextStyle"]["range"]["endIndex"] = index + len(f"{text}\n\n")

                self.insertText("\n\n", index)

                index += len(f"{text}\n\n")

                result = self.service.documents().batchUpdate(
                    documentId=self.DOCUMENT_ID, body={'requests': self.pRequest}).execute()

            if i >= 40:
                sleep(20)
            
            i += 1