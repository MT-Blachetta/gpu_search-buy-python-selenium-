"""Mindfactory GPU purchasing bot using Selenium and web scraping.

The script searches the German retailer mindfactory.de for specific GPU models
and tries to add matching products to the cart. When a potential offer is found
it opens the browser, logs in and alerts the user with a sound. Only comments
and documentation were added to clarify the intent of the original script.
"""

import requests
from bs4 import BeautifulSoup as scrape
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from playsound import playsound

qrtx3070 = "geforce+rtx+3070"
qrtx3060tiA = "geforce+rtx+3060+ti"
qrtx3060tiB = "geforce+rtx+3060ti"
qrtx3080 = "geforce+rtx+3080"
qrtx3090 = "geforce+rtx+3090"
qrxRadeon67 = "Radeon+RX+6700"
qrxRadeon68 = "Radeon+RX+6800"
qrxRadeon69 = "Radeon+RX+6900"

Krtx3070 = ["geforce","rtx","3070"]
Krtx3060tiA = ["geforce","rtx","3060","ti"]
Krtx3060tiB = ["geforce","rtx","3060ti"]
Krtx3080 = ["geforce","rtx","3080"]
Krtx3090 = ["geforce","rtx","3090"]
KrxRadeon67 = ["Radeon","RX","6700"]
KrxRadeon68 = ["Radeon","RX","6800"]
KrxRadeon69 = ["Radeon","RX","6900"]


pidlist =     [ 'rtx3060tiA','rtx3060tiB','rtx3070','rtx3080','rtx3090' ]                  
querylist =   [ qrtx3060tiA, qrtx3060tiB, qrtx3070, qrtx3080, qrtx3090  ] # qrxRadeon67, qrxRadeon68, qrxRadeon69 ]
keywordlist = [ Krtx3060tiA, Krtx3060tiB, Krtx3070, Krtx3080, Krtx3090  ] # KrxRadeon67, KrxRadeon68, KrxRadeon69 ]
keywordsbook = { 'rtx3060tiA': Krtx3060tiA, 'rtx3060tiB': Krtx3060tiB, 'rtx3070': Krtx3070, 'rtx3080': Krtx3080, 'rtx3090': Krtx3090 } # KrxRadeon67, KrxRadeon68, KrxRadeon69 ] 

upper_price =  {  'rtx3060tiA': 1000, 'rtx3060tiB': 1000, 'rtx3070': 1000, 'rtx3080': 1550, 'rtx3090': 2500 }
identityPrice = { 'rtx3060tiA': 600, 'rtx3060tiB': 600 ,'rtx3070': 600, 'rtx3080':  700, 'rtx3090': 1650 } # product verification criterion

def alert_mindfactory(hyperlink):  # driver = webdriver.Firefox('./geckodriver/geckodriver')
    """Open the given product link and prepare checkout."""

    # Load chrome
    driver = webdriver.Chrome('./chromedriver/chromedriver')
    # driver = webdriver.Firefox('./geckodriver/geckodriver')
    # driver.get("https://www.mindfactory.de/")
    # driver.find_element_by_id("checkcookie").click()
    # driver.maximize_window()

    driver.get(hyperlink)
    driver.find_element_by_id("checkcookie").click()
    driver.maximize_window()
    driver.find_element_by_id("btn-buy-productInfo").click()
    driver.get("https://mindfactory.de/shopping_cart.php")
    driver.get("https://www.mindfactory.de/order_login.php")

    mail = driver.find_element_by_id("login_email_address")
    mail.send_keys("michaelblachetta@gmail.com")
    psw = driver.find_element_by_id("login_password")
    psw.send_keys("M#yxcvbnm123")
    form = driver.find_element_by_id("login_form")
    form.submit()

    driver.find_element_by_name("conditions").click()
    driver.find_element_by_name("privacy").click()
    driver.find_element_by_name("disclaimer").click()
    # autobuy function
    # driver.find_element_by_css_selector('div.col-sm-8:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > button:nth-child(1)').click()

    playsound('alert.mp3')
    answer = input("press any key to continue... ")

    # if answer == 'y':
    #     bl.append(pname)
    # root = tk.Tk()
    # MsgBox = tk.messagebox.askquestion ('addBlcklist','Do you want to add the item to the blacklist ?',icon = 'warning')
    # if MsgBox == 'yes':
    #     bl.append(pname)

    # root.destroy()

    return

def checkNameList(name, keylist):
    """Return True if all keywords are contained in the name."""

    target = name.upper()

    for key in keylist:
        if key.upper() not in target:
            return False

    return True

"""
def connect_url(url):
    while True:
        try:
            r = requests.get(url, timeout=9)
            break
        except requests.exceptions.Timeout:
            print("ERROR: The request timed out, try again... "+url)
            time.sleep(0.1)
        except requests.exceptions.HTTPError:
            print("ERROR: An HTTP error occurred, try again... "+url)
            time.sleep(0.1)
        except requests.exceptions.ConnectionError:
            print("ERROR: A Connection error occurred, try again... "+url)
            time.sleep(0.1)
        except requests.exceptions.SSLError:
            print("ERROR: An SSL error occurred, try again... "+url)
            time.sleep(0.1)
        except requests.exceptions.StreamConsumedError: 
            print("ERROR: The content for this response was already consumed, try again... "+url)
            time.sleep(0.1)
        except requests.exceptions.RetryError: 
            print("ERROR: Custom retries logic failed, try again... "+url)
            time.sleep(0.1)

    if r.status_code == requests.codes.ok:
        return scrape(r.content, 'lxml')
    else: 
        return False
"""

def initSearch_mindfactory(pid, query):
    """Initial search that builds a blacklist of already seen products."""

    driver.get("https://www.mindfactory.de/search_result.php?search_query=" + query)
    blacklist = []

    titelinfo = driver.title

    if titelinfo.startswith("Suche nach"):
        if ":" in titelinfo:
            sresult = driver.find_element_by_id("bProducts")
            itemlist = sresult.find_elements_by_class_name("p")

            for i in itemlist:
                pname = i.find_element_by_class_name("pname").text
                prc = i.find_element_by_class_name("pprice").text
                prc = prc[2:].replace('.', '').split(',')[0]
                pprice = float(prc)

                if checkNameList(pname, keywordsbook[pid]) and (upper_price[pid] > pprice > identityPrice[pid]):
                    link = i.find_element_by_tag_name("a").get_attribute("href")
                    # print(f"name: {pname}\npreis: {prc} €\nlink: {link}")
                    alert_mindfactory(link)

                blacklist.append(pname)

    return blacklist
                    
def search_mindfactory(pid, query, blacklist):
    """Repeatedly search Mindfactory and alert on new matching products."""

    blacklist_ = blacklist

    if doc:
        titelinfo = doc.title.text

        if titelinfo.startswith("Suche nach"):
            if ":" in titelinfo:
                itemlist = doc.find(id='bProducts').find_all(_class='p')

                for i in itemlist:
                    # check item
                    pname = i.find(class_="pname").text

                    if pname not in blacklist:
                        prc = i.find(class_="pprice").text
                        prc = prc[2:-1].replace('.', '').replace(',', '.')
                        print("new product found: " + pname + " , " + prc + " €")
                        pprice = float(prc)

                        if checkNameList(pname, keywordsbook[pid]) and (upper_price[pid] > pprice > identityPrice[pid]):
                            print("FOUND - product is matching, connecting to URL... ")
                            link = i.find('a').get("href")
                            doc = connect_url(link)  # no content check !

                            # Liefercheck
                            lieferbarkeit = doc.find(id="priceCol")
                            ok = lieferbarkeit.find(id="btn-buy-productInfo")
                            if ok:
                                print('connected and avaible, start buying... ')
                                alert_mindfactory(link)

                        blacklist_.append(pname)

    return blacklist_



if __name__ == '__main__':
    
    blist = []

    for i, q in enumerate(querylist):
        blist.append( initSearch_mindfactory(pidlist[i],q) )

    print('initialisation successfull, start surveillance...')

    # Endless monitoring loop
    while(True):
        for i, q in enumerate(querylist):
            #print('\niteration '+str(i))
            blist[i] = search_mindfactory(pidlist[i],q,blist[i])