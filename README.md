<h1>Script for parsing data from the website of the Unified System of Government Procurement of the Russian Federation</h1>
<br />
<br />
<h3>How to run</h3>
<br />
You need to install requirements.txt 

```

pip install -r requirements.txt

```
You also need to install a driver that will match your browser version. You can find it at this: https://developer.chrome.com/docs/chromedriver/downloads?hl=ru <br />
Add path to chromedriver to main.py. 

```
def get_data(projectname):
    try:
        service = ChromeService(executable_path='<path_for_your_chromedriver')

```
<br />
Great! You can used it

<h3>How to used it</h3>
<br />
