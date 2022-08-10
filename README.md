# astoundz-scrapper

This program is to fill a content dock for given urls

## Dependancies

For pip:
```shell
pip install Flask
pip install beautifulsoup4
pip install python-docx
pip install docx
```

For pip3:
```shell
pip3 install Flask
pip3 install beautifulsoup4
pip3 install python-docx
pip3 install docx
```

## Setting up the application
In order to use this, you need to change a few lines in a few files in order to use this application

### Put in your Semrush API key
1. Open the file app.py in the main directory
2. Find line 47, it looks like this:
    ```py
    semrush = Semrush.semrush("YOUR_API_KEY")
    ```
3. Change "YOUR_API_KEY" to whatever your Semrush API key is

If something goes wrong, check both the website console and the python
console.