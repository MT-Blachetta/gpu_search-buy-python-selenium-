"""Mindfactory GPU stock notifier.

This script periodically searches mindfactory.de for various GPU models and
sends an SMS message when a matching product is available within a specified
price range. Only comments and documentation were added; no functional
behaviour was changed.
"""

import requests
from bs4 import BeautifulSoup as scrape
import clx.xms
import time

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

def notify(url, ptitle, pprice):
    """Send an SMS with product details."""

    message = "product: " + str(ptitle) + "\nprice: " + str(pprice) + " €\n" + str(url)
    client = clx.xms.Client('2f70139a045b49bda73198693be5db46', 'fa5b002cc9d344b889d9ba71b06679d0')
    client.create_text_message(sender='123456789', recipient='491706554198', body=message)
    print('\n' + message + '\n')


def checkNameList(name, keylist):
    """Return True if all keywords are present in the name."""

    target = name.upper()

    for key in keylist:
        if key.upper() not in target:
            return False

    return True


def connect_url(url):
    """Retrieve the page content for ``url`` with retry logic."""

    while True:
        try:
            r = requests.get(url, timeout=9)
            break
        except requests.exceptions.Timeout:
            print("ERROR: The request timed out, try again... " + url)
            time.sleep(0.1)
        except requests.exceptions.HTTPError:
            print("ERROR: An HTTP error occurred, try again... " + url)
            time.sleep(0.1)
        except requests.exceptions.ConnectionError:
            print("ERROR: A Connection error occurred, try again... " + url)
            time.sleep(0.1)
        except requests.exceptions.SSLError:
            print("ERROR: An SSL error occurred, try again... " + url)
            time.sleep(0.1)
        except requests.exceptions.StreamConsumedError:
            print("ERROR: The content for this response was already consumed, try again... " + url)
            time.sleep(0.1)
        except requests.exceptions.RetryError:
            print("ERROR: Custom retries logic failed, try again... " + url)
            time.sleep(0.1)

    if r.status_code == requests.codes.ok:
        return scrape(r.content, 'lxml')
    else:
        return False


def initSearch_mindfactory(pid, query):
    """Initial search to build a blacklist of existing products."""

    doc = connect_url("https://www.mindfactory.de/search_result.php?search_query=" + query)
    blacklist = []

    if doc:
        titelinfo = doc.title.text

        if titelinfo.startswith("Suche nach"):
            if ":" in titelinfo:
                itemlist = doc.find(id='bProducts').find_all(_class='p')

                for i in itemlist:
                    # check item
                    pname = i.find(class_="pname").text
                    # if pname not in blacklist:
                    prc = i.find(class_="pprice").text
                    prc = prc[2:-1].replace('.', '').replace(',', '.')
                    pprice = float(prc)

                    if checkNameList(pname, keywordsbook[pid]) and (upper_price[pid] > pprice > identityPrice[pid]):
                        link = i.find('a').get("href")
                        # print("product: "+str(pname)+"\nprice: "+prc+" €\n"+link)
                        notify(link, pname, pprice)

                    blacklist.append(pname)

    return blacklist
                    
def search_mindfactory(pid, query, blacklist):
    """Repeatedly search and notify about new matching products."""

    doc = connect_url("https://www.mindfactory.de/search_result.php?search_query=" + query)
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
                                print('connected and avaible, start notification... ')
                                notify(link, pname, pprice)

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