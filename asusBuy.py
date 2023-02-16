import requests
import time
from bs4 import BeautifulSoup as scrape
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from playsound import playsound

def checkout_asus(productURL): # driver = webdriver.Firefox(PATH)
    driver = webdriver.Chrome('./chromedriver/chromedriver')
    driver.get(productURL)
    driver.maximize_window()
    #not_yet_loaded = True
    #while not_yet_loaded:
    while True:
        try:
            cookie = driver.find_element_by_id("CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection")
            #cookie_loaded = False
            break
        except NoSuchElementException:
            pass
            #print("Error")
    cookie.click()
    
    driver.find_element_by_css_selector(".buybox--button").click()
    driver.get("https://webshop.asus.com/de/checkout/confirm")
    mail = driver.find_element_by_id("email")
    #mail.clear()
    mail.send_keys("hexproofcommander@gmail.com")
    psw = driver.find_element_by_id("passwort")
    #psw.clear()
    psw.send_keys("Asus#yxcvbnm123")
    form = driver.find_element_by_name("sLogin")
    form.submit()
    driver.find_element_by_id("sAGB").click()
    driver.find_element_by_css_selector("body > div:nth-child(6) > div > section > div > div > div > div.product--table > div.table--actions.actions--bottom > div > button").click()
    # if payPal
    while True:
        try:
            paypalmail = driver.find_element_by_id("email")
            #cookie_loaded = False
            break
        except NoSuchElementException:
            pass
            #print("waiting for paypal")

    paypalmail.send_keys("michaelblachetta@googlemail.com")
    driver.find_element_by_id("btnNext").click()
    #time.sleep(0.5)
    #driver.find_element_by_css_selector("button.cleverpush-confirm-btn.cleverpush-confirm-btn-deny").click()
    #driver.find_element_by_css_selector(".buybox--button").click()
    playsound('alert.mp3')

    input("press any key to continue... ")
    return

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


def lieferbar_asus(bsoup):
    '''
    #negative criterion
    EXIST doc.select("div.product--buybox.block div.alert.is--error")
    or
    EXIST result = doc.select(".detail-error")
    '''
    #positive criterion
    if bsoup.select(".buybox--button"):
        return True
    else:
        return False
    
def extract_asus(bsoup):

    name = bsoup.find('h1',class_ ="product--title").text.strip()

    prc = bsoup.select('.price--content')
    pstr = prc[0].text
    pstr = pstr.strip().replace(',','.')[:-2]

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

while True:

    for k in url_list_asus.keys():
        pid = k
        linklist = url_list_asus[k]
        for link in linklist:
            doc = connect_url(link)
            if doc:
                print("URL aktiv: "+link)
                if lieferbar_asus(doc):
                    print("Lieferbarkeit erfolgreich geprueft !")
                    pname, pprice = extract_asus(doc)
                    print("product: "+str(pname)+"\nprice: "+str(pprice)+" €\n"+link)
                    checkout_asus(link)
                    filename = 'asus_'+pid+"_"+str(gcount)+".html"
                    open(filename, 'w').write(str(doc))
                    close(filename)
                    gcount += 1