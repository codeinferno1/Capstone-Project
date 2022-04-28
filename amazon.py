from flask import Flask,request, url_for, redirect, render_template
import requests
from bs4 import BeautifulSoup
import pprint
import smtplib
from email.message import EmailMessage
import csv       ### For storing all the information of name,price,desired price,links and email in a csv file
import schedule
import time


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")  ## Homepage
x = 1
@app.route('/price',methods=['POST','GET'])     ## When the form is get submitted
def input():
    
    url = request.form['1']   ## requesting each field one bye one ## Product url
    req_price = int(request.form['2'])   ## Desired price
    email_user = request.form['3']  ## EMail of user
    #print(url)
    #print(req_price)
    #print(email_user)
    
    def check():
        global x      ## Global X for making the email send only one time
        if "flipkart" in url.lower() :           ### If 'flipkart'  is in url then it will run otherwise else will run
            res = requests.get(f'{url}')         ### Sending a request and receiving response
            soup = BeautifulSoup(res.text,'html.parser') ## Fetching whole source code
            name = soup.select('._35KyD6')[0].getText()  ## Product name
            print("\n"+name)
            price = soup.select('._3qQ9m1')[0].getText()  ## Product price
            price = int(price[1:].replace(",",""))  ## Price Cleaning and converting it into int
            print(price)
        elif "amazon" in url.lower():
            res = requests.get(url,headers=headers)
            soup = BeautifulSoup(res.text,'html.parser')
            name = soup.select("#title")[0].getText().strip()
            try:
                price = soup.select("#priceblock_ourprice")[0].getText().strip()  ## Original Price
            except:
                price = soup.select("#priceblock_dealprice")[0].getText().strip()  ## Deal Price
            price_num = price.replace("₹","")  ## Removing rupee symbol
            price_num = price_num.replace(",","") ## Replacing ' , ' with ""
            price = int(float(price_num))  ## COnvertion to int
            #print(f"{name} with a price of {price}")
            print(f"\n{name}\n {price}")
        if (price <= req_price) :         ## CHecking if the price is lesser than or equal to the desired price if yes then it will run otherwise else will run
                email = EmailMessage()   
                email['from'] = 'Price tracker'  ## Heading
                email['to'] = email_user
                email['subject'] = 'The price of product is drop down to your requirment... GO check out'   ## Subject

                email.set_content(f'Product Name: {name}\nPrice:{price}\n Link: "{url}"')  ## Link and content(name,price)
                with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(YOUR_EMAIL,PASSWORD)  ## Insert your email and password 
                    smtp.send_message(email) 
                    print("Email Send!")
                    
                fields=[name,price,req_price,email_user,url]
                with open(r'data_user.csv', 'a',newline="") as f: 
                    writer = csv.writer(f)               ### Saving all the information to a csv file for future checking
                    writer.writerow(fields)
                x=x+1
        else:
            print("\nEmail not send! price is still larger then the desired price..")  ## Else message

        
    schedule.every(3).seconds.do(check)
    while x == 1:
        schedule.run_pending()
        time.sleep(1)
    return render_template("index.html")
  
if __name__ == '__main__': 
    app.run(debug=True)  ## Running the flask app