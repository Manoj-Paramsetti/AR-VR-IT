from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import environ, rmdir

rmdir('chrome-data')
options = Options()
options.add_argument('--no-sandbox')
#options.add_argument("--headless")
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
driver = webdriver.Chrome(webdriverPath, options=options, desired_capabilities=capabilities)
driver.maximize_window()
driver.get('https://web.whatsapp.com/')