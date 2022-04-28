import requests as r
from bs4 import BeautifulSoup as bs
import time


URL = "https://www.flipkart.com/crucial-p2-500-gb-laptop-desktop-internal-solid-state-drive-ct500p2ssd8-3d-nand/p/itm4aaa67f655e76?pid=IHDFTZ58EVPCXTCJ&lid=LSTIHDFTZ58EVPCXTCJCCXEXD&marketplace=FLIPKART&q=m.2+ssd&store=6bo%2Fjdy%2Fdus&srno=s_1_6&otracker=search&otracker1=search&fm=organic&iid=c4e5a573-1583-4b90-b068-82ab34bda70f.IHDFTZ58EVPCXTCJ.SEARCH&ppt=hp&ppn=homepage&ssid=7m325d1ae80000001650710372449&qH=ef5e8858fc8f47da"

while True:
    page = r.get(URL)
    soup = bs(page.content,"html.parser")
    title = soup.find("span",{"class","B_NuCI"}).text
    price = soup.find("div",{"class","_30jeq3 _16Jk6d"}).text
    price = price.replace("₹","")
    price = price.replace(",","") #To-Do : Write logic for if there is no ','
    print(f"The price of {title} is {price}")
    time.sleep(5)


