# astoundz-scrapper

This program is to fill a content dock for given urls

## Dependancies

For pip:
```shell
pip install Flask
pip install beautifulsoup4
pip install python-docx
pip install docx
pip install html_to_json
```

For pip3:
```shell
pip3 install Flask
pip3 install beautifulsoup4
pip3 install python-docx
pip3 install docx
pip3 install html_to_json
```

## Setting up the application
In order to use this, you need to change a few lines in a few files.

### Put in your Semrush API key
1. Open the file app.py in the main directory
2. Find line 47, it looks like this:
    ```py
    semrush = Semrush.semrush("YOUR_API_KEY")
    ```
3. Change "YOUR_API_KEY" to whatever your Semrush API key is

## Running the application
1. To run the application, first open a terminal or command prompt window in the project directory and type ```flask run```.
2. Next, copy the file path of web/html/index.html and paste it into chrome.

If something goes wrong, check both the website console by hitting f2 and the python console.