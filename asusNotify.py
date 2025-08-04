"""Notification script for ASUS GPU availability.

This script periodically checks a list of ASUS product pages and sends an SMS
when a GPU becomes available. It uses ``clx.xms`` to send the message and is
configured with hard coded credentials and phone numbers. Only explanatory
comments were added; the functional behaviour stays the same.
"""

import requests
import time
from bs4 import BeautifulSoup as scrape
import clx.xms


def notify(url, ptitle, pprice):
    """Send an SMS containing product information."""

    message = "product: " + str(ptitle) + "\nprice: " + str(pprice) + " €\n" + str(url)
    client = clx.xms.Client('2f70139a045b49bda73198693be5db46', 'fa5b002cc9d344b889d9ba71b06679d0')
    client.create_text_message(sender='123456789', recipient='491706554198', body=message)
    print('\n' + message + '\n')

def connect_url(url):
    """Retrieve a URL with retry handling."""

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


def lieferbar_asus(bsoup):
    """Check ASUS page for the presence of the buy button."""

    # negative criteria (commented):
    # doc.select("div.product--buybox.block div.alert.is--error")
    # doc.select(".detail-error")
    if bsoup.select(".buybox--button"):
        return True
    else:
        return False
    
def extract_asus(bsoup):
    """Extract title and price from an ASUS product page."""

    name = bsoup.find('h1', class_="product--title").text.strip()

    prc = bsoup.select('.price--content')
    pstr = prc[0].text
    pstr = pstr.strip().replace(',', '.')[:-2]

    preis = float(pstr)

    return name, preis


url_3060tiA = "https://webshop.asus.com/de/komponenten/grafikkarten/rtx-30-serie/2991/asus-rog-strix-rtx3060ti-o8g-gaming"
url_3070_rog = "https://webshop.asus.com/de/rog-/rog-republic-of-gamers/grafikkarten/3025/asus-rog-strix-rtx3070-o8g-white"
url_3070_dual = "https://webshop.asus.com/de/komponenten/grafikkarten/nvidia-serie/2845/asus-dual-rtx3070-o8g"
url_3080_A = "https://webshop.asus.com/de/komponenten/grafikkarten/nvidia-serie/2824/asus-tuf-rtx3080-10g-gaming"
url_3080_B = "https://webshop.asus.com/de/komponenten/grafikkarten/nvidia-serie/2825/asus-tuf-rtx3080-o10g-gaming"

url_list_asus = { 'rtx3060ti': [url_3060tiA], 'rtx3070': [url_3070_rog,url_3070_dual], 'rtx3080': [url_3080_A, url_3080_B], 'rtx3090': []  }

'''
url_list_mindfactory
url_list_alternate
'''

gcount = 0

print('starting surveillance loop...')

# Endless monitoring loop
while True:

    for k in url_list_asus.keys():
        pid = k
        linklist = url_list_asus[k]
        for link in linklist:
            doc = connect_url(link)
            if doc:
                print("URL aktiv: " + link)
                if lieferbar_asus(doc):
                    print("Lieferbarkeit erfolgreich geprueft !")
                    pname, pprice = extract_asus(doc)
                    notify(link, pname, pprice)
                    filename = 'asus_' + pid + "_" + str(gcount) + ".html"
                    open(filename, 'w').write(str(doc))
                    close(filename)
                    gcount += 1
                
#if gcount > 9999999999999998:







"""
def lieferbar_mindfactory():
def lieferbar_saturn():
def lieferbar_mediamarkt():
def lieferbar_alternate():

def extract_mindfactory():
def extract_mediamarkt():
def extract_saturn():
"""


#filename = 'asus_'+pid+"_"+str(gcount)+".html"
#open(filename, 'wb').write(r.content)