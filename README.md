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

```
def get_projectnames():
    projectnames = []
    time.sleep(0.01)
    responsedata = requests.get('url from CRM method>',verify=False, allow_redirects=True, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    if responsedata.status_code == 200:
        responsedata = responsedata.json()
        for elem in responsedata['result']:
            projectnames.append(elem)
    return projectnames
```
The script works with a list of notification (projectname). In this code the list of projectnames is taken from customer's CRM system. <br />
You can used simple array without requests.get if you know a number of notification. <br />

```
data_frame = {
            'projectname': projectname,
            'order_status': order_status,
            'start_amount': start_amount,
            'date_sign': date_sign,
            'date_off': date_off,
            'date_registr': date_registr,
            'update_registr': update_registr,
            'customer_name': customer_name,
            'contract_number': contract_number,
            'contract_status': contract_status,
            'contract_amount': contract_amount,
            'amount_executed': amount_executed,
            'amount_actually_paid': amount_actually_paid
        }

        header = {
            'Content-Type': 'application/json'
        }
        try:
            requests.post(<'url from CRM>', headers=header, json=data_frame)
        except Exception as ex:
            print(ex)
```

The result of the script is a dataframe, which in my case is sent using a post request<br />
