from selenium import webdriver
import time
paht = r'C:\\Users\\carlos\\Desktop\\p\\chromedriver.exe'

driver = webdriver.Chrome(paht)

driver.get("https://www.selenium.dev/downloads/")

time.sleep(10)

driver.quit()
