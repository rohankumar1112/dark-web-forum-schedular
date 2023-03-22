import time
from selenium import webdriver
from tbselenium.tbdriver import TorBrowserDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
import time
# from driverpath import *


def is_continuous(arr, sub_arr):
    n = len(sub_arr)
    for i in range(len(arr) - n + 1):
        if arr[i:i+n] == sub_arr:
            return True
    return False

# def Driver():
#     with TorBrowserDriver("/home/rohan/Downloads/tor-browser-linux64-12.0.1_ALL/tor-browser") as driver:
#          driver.get('http://rampjcdlqvgkoz5oywutpo6ggl7g6tvddysustfl6qzhr5osr24xxqqd.onion')
#         return driver


def detect_login(driver,url):
    driver.get(url)
    # with TorBrowserDriver("/home/rohan/Downloads/tor-browser-linux64-12.0.1_ALL/tor-browser") as driver:
    #     # driver.get('http://rampjcdlqvgkoz5oywutpo6ggl7g6tvddysustfl6qzhr5osr24xxqqd.onion')
    #     # driver.get('http://ezdhgsy2aw7zg54z6dqsutrduhl22moami5zv2zt6urr6vub7gs6wfad.onion')
    #     # driver.get('http://cryptbbtg65gibadeeo2awe3j7s6evg7eklserehqr4w4e2bis5tebid.onion')
    #     # driver.get('https://corsair.wtf/topic/9595-valorant-no-recoil-hack-program/')
    #     driver.get('http://cryptbbtg65gibadeeo2awe3j7s6evg7eklserehqr4w4e2bis5tebid.onion/member.php?action=login')

    # main_driver =Driver()
    time.sleep(2)
    # my_title = main_driver.title
    my_title = driver.title
    print(my_title)
    LOwer_Title=my_title.lower()
    List_char_Title=list(LOwer_Title)
    WOrd_list=["log","sign","to be come"]
    x="false"
    print(WOrd_list)
    for word in WOrd_list:
        Word_lower=word.lower()
    
        word_list= list(Word_lower)

        if is_continuous(List_char_Title,word_list ):
            print(Word_lower)
            x="true"
            print("login page")
            if x=="true":
                driver,url = login_fill(driver)
                login_button_detect(driver,url)
                
        else:
            pass
            print("not login.")               

def login_fill(driver):
    time.sleep(2)
    currentUrl=driver.current_url
    form=driver.find_elements(By.TAG_NAME,'form')
    user_list =['username','auth','name','login','email','email id']
    login_button_texts = ['LOGIN', 'LOG IN', 'LogIn', 'Log In', 'Login', 'Log in', 'login', 'log in', 'SIGNIN', 'SIGN IN', 'SignIn', 'Sign In', 'Signin', 'Sign in', 'signin', 'sign in','submit']
    
    # email_list =
    for f in form:

        if((f.get_attribute('method').lower()=='post')):
            try:    
                username=f.find_elements(By.TAG_NAME,'input')
                for i in username:
                    if(i.get_attribute('name').lower())in (user_list):
                        i.send_keys('loop45singh@gamil.com') 
            
                    if(i.get_attribute('type')=='password'):
                        i.send_keys('Loop@123')

                try:
                    if(f.find_element(By.TAG_NAME,'button').text.lower() in login_button_texts ):
                        f.find_element(By.TAG_NAME,'button').click()
                except:
                    pass

                try:
                    if(f.find_element(By.TAG_NAME,'button').get_attribute("type").lower() in login_button_texts):
                        f.find_element(By.TAG_NAME,'button').click()
                except:
                    pass

                try:
                    if(f.find_element(By.TAG_NAME,'input').get_attribute("type").lower() in login_button_texts):
                        f.find_element(By.TAG_NAME,'input').click()
                except:
                    pass

                # if(f.find_element(By.CLASS_NAME,'button')):

                #     f.find_element(By.CLASS_NAME,'button').click() 

                
                time.sleep(10)    

            except:
                pass
        
            time.sleep(10)
            # url = driver
            
    return driver,currentUrl

def login_button_detect(driver,url):
    

    # urls = ['https://cardingforum.cx/','https://forum.defcon.org/','https://breached.vc']

    login_button_texts = ['LOGIN','LOG IN','LogIn','Log In','Login','Log in','login','log in','SIGNIN','SIGN IN','SignIn','Sign In','Signin','Sign in','signin','sign in','Login or Sign Up']

    # for url in urls :
    driver.get(url)
    time.sleep(2)
            
    for login_button_text in login_button_texts :

                try :
                    login_button = driver.find_element(By.XPATH, f"//div[contains(text(),'{login_button_text}')]")
                    print('hi')
                except NoSuchElementException:

                    try :
                        login_button = driver.find_element(By.XPATH, f"//a[contains(text(),'{login_button_text}')]")

                    except NoSuchElementException:

                        try :
                            login_button = driver.find_element(By.XPATH, f"//button[contains(text(),'{login_button_text}')]")
                        
                        except NoSuchElementException:
                            continue

    try :
        login_button.click()
                    
    except :
        driver.get(login_button.get_attribute("href"))
                    
    time.sleep(10)
    
    
d =uc.Chrome()    
detect_login(d,"https://www.fb.com")    
# detect_login(d,"https://www.blackhatworld.com/forums/")    