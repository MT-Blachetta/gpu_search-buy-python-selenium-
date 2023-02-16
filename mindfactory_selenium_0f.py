import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import WebDriverException
from playsound import playsound

userName = "michaelblachetta@gmail.com" # dummy value
password = "M#yxcvbnm123" # dummy value

# queries for desired products
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
querylist =   [ qrtx3060tiA, qrtx3060tiB, qrtx3070, qrtx3080, qrtx3090  ] 
keywordlist = [ Krtx3060tiA, Krtx3060tiB, Krtx3070, Krtx3080, Krtx3090  ] # KrxRadeon67, KrxRadeon68, KrxRadeon69 ]
keywordsbook = { 'rtx3060tiA': Krtx3060tiA, 'rtx3060tiB': Krtx3060tiB, 'rtx3070': Krtx3070, 'rtx3080': Krtx3080, 'rtx3090': Krtx3090 } # KrxRadeon67, KrxRadeon68, KrxRadeon69 ] 

# price limits as a filter, identityPrice is for filtering out negative items as a criterion for identification
upper_price =  {  'rtx3060tiA': 1000, 'rtx3060tiB': 1000, 'rtx3070': 1000, 'rtx3080': 1600, 'rtx3090': 2500 }
identityPrice = { 'rtx3060tiA': 600, 'rtx3060tiB': 600 ,'rtx3070': 600, 'rtx3080':  700, 'rtx3090': 1650 } # product verification criterion

def alert_mindfactory(hyperlink): # driver = webdriver.Firefox('./geckodriver/geckodriver') does not work ?

    # Load chrome

    driver = webdriver.Chrome('./chromedriver/chromedriver')

    # accept cookies (necessary for accessing target elements)
    driver.get(hyperlink)
    #driver.maximize_window()
    driver.find_element_by_id("checkcookie").click()


    try:
        try:
            driver.find_element_by_css_selector("button[type='submit']").click()
            #driver.find_element_by_id("btn-buy-productInfo").click()
        except StaleElementReferenceException:
            time.sleep(0.3)
            driver.find_element_by_css_selector("button[type='submit']").click()
        except ElementClickInterceptedException:
            time.sleep(0.3)
            driver.find_element_by_css_selector("button[type='submit']").click()

        driver.get("https://mindfactory.de/shopping_cart.php")
        driver.get("https://www.mindfactory.de/order_login.php")

        mail = driver.find_element_by_id("login_email_address")
        #mail.clear()
        mail.send_keys(userName)
        psw = driver.find_element_by_id("login_password")
        #psw.clear()
        psw.send_keys(password)
        form = driver.find_element_by_id("login_form")
        form.submit()
        
        driver.find_element_by_name("conditions").click()
        driver.find_element_by_name("privacy").click()
        driver.find_element_by_name("disclaimer").click()
        #autobuy function here
        #driver.find_element_by_css_selector('div.col-sm-8:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > button:nth-child(1)').click()
        driver.maximize_window()
        playsound('alert.mp3')
        input("press any key to continue... ")
        return True
    except NoSuchElementException:
        #print("Cannot be bought ! - its to late")
        #driver.maximize_window()
        #playsound('error.mp3')
        return False
    except StaleElementReferenceException:
        driver.get(hyperlink)
        driver.maximize_window()
        playsound('alert.mp3')
        ##get_toChartButton##
        try:
            driver.find_element_by_css_selector("button[type='submit']").click()
            #driver.find_element_by_id("btn-buy-productInfo").click()
        except StaleElementReferenceException:
            time.sleep(0.3)
            driver.find_element_by_css_selector("button[type='submit']").click()
        except ElementClickInterceptedException:
            time.sleep(0.3)
            driver.find_element_by_css_selector("button[type='submit']").click()
        ##-----------------##
        driver.get("https://mindfactory.de/shopping_cart.php")
        driver.get("https://www.mindfactory.de/order_login.php")

        mail = driver.find_element_by_id("login_email_address")
        #mail.clear()
        mail.send_keys(userName)
        psw = driver.find_element_by_id("login_password")
        #psw.clear()
        psw.send_keys(password)
        form = driver.find_element_by_id("login_form")
        form.submit()
        
        driver.find_element_by_name("conditions").click()
        driver.find_element_by_name("privacy").click()
        driver.find_element_by_name("disclaimer").click()
        #autobuy function here
        #driver.find_element_by_css_selector('div.col-sm-8:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > button:nth-child(1)').click()
        driver.maximize_window()
        playsound('alert.mp3')
        input("press any key to continue... ")
        return True
    except ElementClickInterceptedException:
        driver.maximize_window()
        playsound('error.mp3')
        input("press any key to continue... ")
        return False
    except ElementNotInteractableException:
        driver.maximize_window()
        playsound('error.mp3')
        input("press any key to continue... ")
        return False
    except WebDriverException:
        print('ERROR: Web Driver do not work')
        playsound('error.mp3')
        input("press any key to continue... ")
        return False



def checkNameList(name,keylist):
# case insensitive  string keywords checking
    target = name.upper()

    for key in keylist:
        if key.upper() not in target:
            return False

    return True


def initSearch_mindfactory(driver,pid,query):
    # example:
    #query = "rtx+3070"
    #pid = 'rtx3070'
    
    driver.get("https://www.mindfactory.de/search_result.php?search_query="+query)
    blacklist = [] # list of items that should be ignored

    titelinfo = driver.title
    # using the title information as a criterion to decide if items are found for the search query
    if titelinfo.startswith("Suche nach"):
        if ":" in titelinfo:
            sresult = driver.find_element_by_id("bProducts")
            itemlist = sresult.find_elements_by_class_name("p") # search entries

            for i in itemlist:
      # extracting item name
                pname = i.find_element_by_class_name("pname").text
      # extracting item price
                prc = i.find_element_by_class_name("pprice").text
                prc = prc[2:].replace('.','').split(',')[0]

                pprice = float(prc)


                if checkNameList(pname,keywordsbook[pid]) and (upper_price[pid] > pprice > identityPrice[pid]): # check for matching conditions
                    link = i.find_element_by_tag_name("a").get_attribute("href")
                    print(f"name: {pname}\npreis: {prc} €\nlink: {link}")
                    if alert_mindfactory(link): blacklist.append(pname)
                else:
                    blacklist.append(pname) # remember item for future search


    return blacklist
                    
def search_mindfactory(driver,pid,query,blacklist):
    # ITERATION



    driver.get("https://www.mindfactory.de/search_result.php?search_query="+query)
    titelinfo = driver.title

    if titelinfo.startswith("Suche nach"):
        if ":" in titelinfo:
            sresult = driver.find_element_by_id("bProducts")
            itemlist = sresult.find_elements_by_class_name("p")

            for i in itemlist:
                pname = i.find_element_by_class_name("pname").text
                if pname not in blacklist: # look only for new items
                    prc = i.find_element_by_class_name("pprice").text
                    prc = prc[2:].replace('.','').split(',')[0]

                    pprice = float(prc)


                    if checkNameList(pname,keywordsbook[pid]) and (upper_price[pid] > pprice > identityPrice[pid]):
                        link = i.find_element_by_tag_name("a").get_attribute("href")
                        print(f"name: {pname}\npreis: {prc} €\nlink: {link}")
                        if alert_mindfactory(link): blacklist.append(pname)
                    else:
                        blacklist.append(pname)




    return



if __name__ == '__main__':

    driver = webdriver.Chrome('./chromedriver/chromedriver')
    driver.get("https://www.mindfactory.de/")
    driver.find_element_by_id("checkcookie").click() # remove cookie dialog
    
    blist = [] # processed items

    for i, q in enumerate(querylist):
        blist.append( initSearch_mindfactory(driver,pidlist[i],q) )

    print('initialisation successfull, start searching...')

    while(True):
        for i, q in enumerate(querylist):
            search_mindfactory(driver,pidlist[i],q,blist[i])

