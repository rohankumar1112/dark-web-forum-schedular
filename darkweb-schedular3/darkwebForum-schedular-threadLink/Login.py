import time
from selenium import webdriver
from tbselenium.tbdriver import TorBrowserDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
from databaseConnection import login_credential

def is_continuous(arr, sub_arr):
    n = len(sub_arr)
    for i in range(len(arr) - n + 1):
        if arr[i:i+n] == sub_arr:
            return True
    return False

def detect_login(driver,url):
    driver.get(url)

    time.sleep(2)
    my_title = driver.title
    # print(my_title)
    LOwer_Title=my_title.lower()
    List_char_Title=list(LOwer_Title)
    WOrd_list=["log","sign","to be come"]
    x="false"
    for word in WOrd_list:
        Word_lower=word.lower()
    
        word_list= list(Word_lower)

        if is_continuous(List_char_Title,word_list ):
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
            domain=currentUrl.split('.')[0]
            print(domain)
            loginData=login_credential.find_one({'site':{'$regex':domain}})
            try:
                loginId=loginData['loginId']
                password=loginData['password']
            except:
                loginId=None
                password=None
                print('Id and Password not exixt for this site in database.')
            try:    
                username=f.find_elements(By.TAG_NAME,'input')
                for i in username:
                    if(i.get_attribute('name').lower())in (user_list):
                        i.send_keys(loginId) 
            
                    if(i.get_attribute('type')=='password'):
                        i.send_keys(password)

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

            except:
                pass
        
            time.sleep(4)
            
    return driver,currentUrl

def login_button_detect(driver,url):
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
        currentUrl=driver.current_url
                    
    except :
        driver.get(login_button.get_attribute("href"))
        currentUrl=driver.current_url
                    
    return currentUrl,driver
    
    
 