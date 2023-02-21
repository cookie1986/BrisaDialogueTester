import os
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# load settings
script_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(script_dir, 'config', 'settings.json')
with open(settings_path, 'r') as f:
    settings = json.load(f)

# setup web driver
options = Options()
options.add_experimental_option("detach",True)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),options=options)

# navigate to chatbot prototype
driver.get(settings['CHATBOT_URL'])
# wait for chatbot to load
time.sleep(settings['INITIAL_APP_LOAD_TIME'])

def run_test_dialogue():
    # start chatbot and send the first message
    start_chat = input_element = driver.find_element("xpath", "//*[@id='vf-prototype__start']") # start chat button
    start_chat.click()

    chat_input = driver.find_element("xpath", "//*[@id='vf-prototype-user-input']") # input text
    chat_input.send_keys("Hi, Brisa!")

    send_message = driver.find_element("xpath","//*[@id='root']/div[1]/div/div/div/div[2]/div/div/div/div/div[2]/button") # send text
    send_message.click()

    # wait for response
    time.sleep(settings['BETWEEN_MSG_LOAD_TIME'])

    # verify response
    response_element = driver.find_element("xpath", "//div[@class='sc-fFZlpY gUxiel']//div//span")
    try:
        assert response_element.text == "Hi!"
    except:
        print("error found")

    # Close the web driver
    driver.quit()