import os
import shutil
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from spot_deepfakes import clearDirectories, displayOutput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def move_files(src_folder, dest_folder):
    files = os.listdir(src_folder)
    # If there are no files, print a message and return
    if not files:
        print("No files to move.")
        return
    # Get the full paths of each file in the source folder
    file_paths = [os.path.join(src_folder, file) for file in files]
    # Find the latest file based on modification time
    latest_file = max(file_paths, key=os.path.getmtime)
    # Construct the destination path for the latest file
    dest_path = os.path.join(dest_folder, os.path.basename(latest_file))
    # Move the latest file to the destination folder
    shutil.move(latest_file, dest_path)
    print(f"Moved latest file: {os.path.basename(latest_file)}")

clearDirectories("C:/Users/mrman/OneDrive/Desktop/Hackathon/DeepFake_1/DeepFake-Spot/input", r"C:/Users/mrman/OneDrive/Desktop/Hackathon/DeepFake_1/DeepFake-Spot/src/buffer" , r"C:/Users/mrman/OneDrive/Desktop/Hackathon/DeepFake_1/DeepFake-Spot/output" )

driver = webdriver.Chrome()

driver.get("https://twitter.com")
signin_present = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//span[text()="Sign in"]'))
)

sign_in_button = driver.find_element(By.XPATH, '//span[text()="Sign in"]')
sign_in_button.click()

username_present = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'r-30o5oe'))
)
username_input = driver.find_element(By.CLASS_NAME, 'r-30o5oe')
username_input.send_keys('@AbdulMannan095')

next_button = driver.find_element(By.XPATH, '//span[text()="Next"]')
next_button.click()

pwd_present = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'password'))
)
password_input = driver.find_element(By.NAME, 'password')
password_input.send_keys('yj26fszk37gt')

login_button = driver.find_element(By.XPATH, '//span[text()="Log in"]')
login_button.click()

time.sleep(5)

notify_url = driver.find_element(By.XPATH,'//a[@href="/notifications"]')
notify_url.click()

notifs_present = WebDriverWait(driver, 10).until(
   EC.presence_of_element_located((By.XPATH,'//div[@data-testid="cellInnerDiv"]//a'))
)
notifs=driver.find_elements(By.XPATH,'//div[@data-testid="cellInnerDiv"]//a')

c=0
k=0
video_tweets=[]
for n in notifs:
    mention_url = ""
    txt = n.text
    if c==6*k+2:
        print(txt+" ",k)
        k+=1
    c+=1
    notif_html = n.get_attribute("outerHTML")
    
    soup = BeautifulSoup(notif_html, 'html.parser')
    
    status_link = soup.find('a', href=lambda href: href and 'status' in href)
    mention_urls=[]
   
    if status_link:
        mention_url="https://www.twitter.com"+str(status_link['href'])
        print(mention_url)
        
        driver.get(mention_url)
        
        link_present = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'a[href*="/status/"][dir="ltr"]'))
        )

        anchor_tag = driver.find_element(By.CSS_SELECTOR,'a[href*="/status/"][dir="ltr"]')
       
        video_tweets.append(anchor_tag.get_attribute('href'))
        print(video_tweets)
        break

driver1 = webdriver.Chrome()
driver1.get("https://savetwitter.net/en")

input_present = WebDriverWait(driver1, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@id="s_input"]')))

input_url = driver1.find_element(By.XPATH, '//input[@id="s_input"]')
input_url.send_keys(video_tweets[0])

download_btn = driver1.find_element(By.CLASS_NAME, 'btn-red')
download_btn.click()

res_present = WebDriverWait(driver1, 10).until(
    EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Download MP4")]'))
)

video_res = driver1.find_element(By.XPATH,'//a[contains(text(), "Download MP4")]') 
video_res.click()

x_coordinate = 100
y_coordinate = 100

actions = ActionChains(driver1)

actions.move_by_offset(x_coordinate, y_coordinate).click().perform()

time.sleep(5)

driver1.quit()

# #new shiz
# user_home = os.path.expanduser("~")

# # Specify the relative path from the home directory
# relative_path = "Downloads"

# # Combine the user's home directory and the relative path
# full_path = os.path.join(user_home, relative_path)

# print("Full path:", full_path)
# #end of new shiz

move_files(r"C:/Users/mrman/Downloads", r"C:/Users/mrman/OneDrive/Desktop/Hackathon/DeepFake_1/DeepFake-Spot/input")

displayOutput(False)


df = pd.read_csv(r'C:/Users/mrman/OneDrive/Desktop/Hackathon/DeepFake_1/DeepFake-Spot/src/predictions.csv')
classification = df['prediction'].iloc[-1].split()[-1]

# notify_url = driver.find_element(By.XPATH,'//a[@href="/notifications"]')
# notify_url.click()

# time.sleep(8)

# notifs=driver.find_elements(By.XPATH,'//div[@data-testid="cellInnerDiv"]//a')


# reply_button = driver.find_element(By.XPATH,'//div[@data-testid="reply"]')
# reply_button.click()

# time.sleep(1)

reply_input = driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')

reply_input.send_keys("the video posted above is ", classification)

tweet_button = driver.find_element(By.XPATH, '//span[text()="Reply"]')
tweet_button.click()

time.sleep(3)


driver.quit()


