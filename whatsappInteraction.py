import queue
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import environ
from threading import Thread

queue=[]

options = Options()
options.add_argument('--no-sandbox')
options.add_argument("--headless")
options.add_experimental_option('useAutomationExtension', False)
#options.add_argument("--disable-dev-shm-usage")
options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36")
options.add_argument("--user-data-dir=chrome-data")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

capabilities = {
    'browserName': 'chrome',
    'chromeOptions':  {
        'useAutomationExtension': False,
        'forceDevToolsScreenshot': True,
        'args': ['--start-maximized', '--disable-infobars']
        }
}   

if environ.get("GOOGLE_CHROME_BIN")!=None:
    chromeBinPath=environ.get("GOOGLE_CHROME_BIN")
    webdriverPath=environ.get("CHROMEDRIVER_PATH")
    options.binary_location=chromeBinPath
else:
    webdriverPath="/usr/bin/chromedriver"

def otpSenderLoop():
    print("[INFO] Running OTP Sender Thread")
    while True:
        if len(queue)!=0:
            try:
                phonenum, otp=queue[0]
                print("[LOG] Sending Code to {}".format(phonenum))
                driver = webdriver.Chrome(webdriverPath, options=options, desired_capabilities=capabilities)
                driver.maximize_window()
                driver.get('https://web.whatsapp.com/send?phone=91{}&text=Your%20OTP%20code%20is%20{}'.format(phonenum, otp))
                time.sleep(10)
                driver.find_element_by_xpath('//button[@class="_4sWnG"]').click()
                time.sleep(3)
                driver.close()
                queue.pop(0)
            except Exception as err:
                print(err)
        time.sleep(2)

otpSenderThread=Thread(target=otpSenderLoop)
otpSenderThread.name="OTP Sender Thread"
otpSenderThread.start()