import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
#from selenium.common.exceptions import WebDriverException
from playsound import playsound

userName = "michaelblachetta@gmail.com"
password = "M#yxcvbnm123"

driver = webdriver.Chrome('./chromedriver/chromedriver')
driver.get("https://www.mediamarkt.de")
#driver.maximize_window()

while True:
    try:
        driver.find_element_by_id("privacy-layer-accept-all-button").click()
        break
    except NoSuchElementException:
        pass

with open('mediamarkt_links.txt','r') as f:
    linklist = f.readlines()
    
linklist = [k.replace('\n','') for k in linklist]
    
while True:
    for url in linklist:
        driver.get(url)
        time.sleep(0.025)
        try:###checkout###
            driver.find_element_by_id("pdp-add-to-cart-button").click()
            driver.get("https://www.mediamarkt.de/checkout")
            driver.get("https://www.mediamarkt.de/checkout/login")
            mail = driver.find_element_by_id("mms-login-form__email")
            mail.send_keys(userName)
            psw = driver.find_element_by_id("mms-login-form__password")
            psw.send_keys(password)
            driver.find_element_by_id("mms-login-form__login-button").click()
            #@throws: ElementNotInteractableException
            #driver.find_element_by_css_selector("#root > div.indexstyled__StyledAppWrapper-sc-1hu9cx8-0.klAfyt > div.CheckoutPageInnerWrapper__StyledCheckoutPage-sc-1agob8d-0.jxzDpH > div.Grid__StyledGrid-fs0zc2-0.cQIsoQ.CheckoutPageInnerWrapper__StyledGrid-sc-1agob8d-1.bUTDMC > div > div:nth-child(2) > div > div.Cellstyled__StyledCell-sc-1wk5bje-0.iNYTnU.StepWrapper__StyledSummary-sc-1ory7gr-4.dRdBOA > div > div > div > div > div.BasketResume__StyledSummaryButtons-sc-1pu65vy-0.eAUgFm > div > button").click()
            driver.maximize_window()
            playsound("alert.mp3")
            input("press any key to continue... ")
        except NoSuchElementException:
            pass # buy possible criterion
        except StaleElementReferenceException:
            driver.get(url)
            time.sleep(0.1)
            driver.find_element_by_id("pdp-add-to-cart-button").click()
            driver.get("https://www.mediamarkt.de/checkout")
            driver.get("https://www.mediamarkt.de/checkout/login")
            mail = driver.find_element_by_id("mms-login-form__email")
            mail.send_keys(userName)
            psw = driver.find_element_by_id("mms-login-form__password")
            psw.send_keys(password)
            driver.find_element_by_id("mms-login-form__login-button").click()
            #@throws: ElementNotInteractableException
            #driver.find_element_by_css_selector("#root > div.indexstyled__StyledAppWrapper-sc-1hu9cx8-0.klAfyt > div.CheckoutPageInnerWrapper__StyledCheckoutPage-sc-1agob8d-0.jxzDpH > div.Grid__StyledGrid-fs0zc2-0.cQIsoQ.CheckoutPageInnerWrapper__StyledGrid-sc-1agob8d-1.bUTDMC > div > div:nth-child(2) > div > div.Cellstyled__StyledCell-sc-1wk5bje-0.iNYTnU.StepWrapper__StyledSummary-sc-1ory7gr-4.dRdBOA > div > div > div > div > div.BasketResume__StyledSummaryButtons-sc-1pu65vy-0.eAUgFm > div > button").click()
            driver.maximize_window()
            playsound("alert.mp3")
            input("press any key to continue... ")
        except ElementClickInterceptedException:
            driver.get(url)
            time.sleep(0.1)
            driver.find_element_by_id("pdp-add-to-cart-button").click()
            driver.get("https://www.mediamarkt.de/checkout")
            driver.get("https://www.mediamarkt.de/checkout/login")
            mail = driver.find_element_by_id("mms-login-form__email")
            mail.send_keys(userName)
            psw = driver.find_element_by_id("mms-login-form__password")
            psw.send_keys(password)
            driver.find_element_by_id("mms-login-form__login-button").click()
            #@throws: ElementNotInteractableException
            #driver.find_element_by_css_selector("#root > div.indexstyled__StyledAppWrapper-sc-1hu9cx8-0.klAfyt > div.CheckoutPageInnerWrapper__StyledCheckoutPage-sc-1agob8d-0.jxzDpH > div.Grid__StyledGrid-fs0zc2-0.cQIsoQ.CheckoutPageInnerWrapper__StyledGrid-sc-1agob8d-1.bUTDMC > div > div:nth-child(2) > div > div.Cellstyled__StyledCell-sc-1wk5bje-0.iNYTnU.StepWrapper__StyledSummary-sc-1ory7gr-4.dRdBOA > div > div > div > div > div.BasketResume__StyledSummaryButtons-sc-1pu65vy-0.eAUgFm > div > button").click()
            driver.maximize_window()
            playsound("alert.mp3")
            input("press any key to continue... ")
        except ElementNotInteractableException:
            driver.maximize_window()
            playsound("alert.mp3")
            input("press any key to continue... ")