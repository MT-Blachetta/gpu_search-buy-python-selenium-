"""Automation script for buying GPUs from the ASUS webshop.

The script repeatedly checks product pages for availability. Once an item is
available it uses Selenium to place it in the cart, navigates to the checkout
and logs in with predefined credentials. The script is tailored to the German
ASUS store and makes heavy use of hard coded selectors and credentials. It is
intended purely for demonstrational purposes.

Only comments and documentation were added – the behaviour of the original
script remains unchanged.
"""

import requests
import time
from bs4 import BeautifulSoup as scrape
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from playsound import playsound

def checkout_asus(productURL):  # driver = webdriver.Firefox(PATH)
    """Automate the checkout process for a given product URL.

    The function opens the given product page, accepts cookies, adds the item
    to the cart and proceeds to the checkout. After logging in it prepares a
    PayPal checkout and plays a sound so that the user can manually complete
    the purchase.

    Args:
        productURL: Direct link to the ASUS product page.
    """

    # Launch browser and open product page
    driver = webdriver.Chrome('./chromedriver/chromedriver')
    driver.get(productURL)
    driver.maximize_window()

    # Wait until the cookie banner is available and accept all cookies
    while True:
        try:
            cookie = driver.find_element_by_id("CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection")
            break
        except NoSuchElementException:
            pass
    cookie.click()

    # Add item to cart and navigate to checkout page
    driver.find_element_by_css_selector(".buybox--button").click()
    driver.get("https://webshop.asus.com/de/checkout/confirm")

    # Log into ASUS account
    mail = driver.find_element_by_id("email")
    mail.send_keys("hexproofcommander@gmail.com")
    psw = driver.find_element_by_id("passwort")
    psw.send_keys("Asus#yxcvbnm123")
    form = driver.find_element_by_name("sLogin")
    form.submit()

    # Accept terms and proceed
    driver.find_element_by_id("sAGB").click()
    driver.find_element_by_css_selector(
        "body > div:nth-child(6) > div > section > div > div > div > div.product--table > div.table--actions.actions--bottom > div > button"
    ).click()

    # Wait for PayPal login page and enter credentials
    while True:
        try:
            paypalmail = driver.find_element_by_id("email")
            break
        except NoSuchElementException:
            pass

    paypalmail.send_keys("michaelblachetta@googlemail.com")
    driver.find_element_by_id("btnNext").click()

    # Audible alert so the user can finish the purchase manually
    playsound('alert.mp3')

    input("press any key to continue... ")
    return

def connect_url(url):
    """Fetch a URL with basic retry logic.

    Args:
        url: Web address to request.

    Returns:
        Parsed ``BeautifulSoup`` object if the request succeeded, otherwise
        ``False``.
    """

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
    """Check if the product is available."""

    # negative criteria (commented):
    #   doc.select("div.product--buybox.block div.alert.is--error")
    #   doc.select(".detail-error")
    # positive criterion – buy button present
    if bsoup.select(".buybox--button"):
        return True
    else:
        return False
    
def extract_asus(bsoup):
    """Extract product name and price from an ASUS product page."""

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
                    print("product: " + str(pname) + "\nprice: " + str(pprice) + " €\n" + link)
                    checkout_asus(link)
                    filename = 'asus_' + pid + "_" + str(gcount) + ".html"
                    open(filename, 'w').write(str(doc))
                    close(filename)
                    gcount += 1