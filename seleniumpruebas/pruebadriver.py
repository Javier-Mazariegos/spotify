from selenium import webdriver
from selenium.webdriver import ActionChains
import time
paht = r'C:\\Users\\carlos\\Desktop\\spotify\\seleniumpruebas\\chromedriver.exe'
#paht = r'D:\\spotify\\seleniumpruebas\\chromedriver.exe'  #<----- Hay que cambiar el path donde esta el driver de chrome
driver = webdriver.Chrome(paht)
driver.maximize_window()

driver.get("http://127.0.0.1:5000/")

driver.find_element_by_name("play").click()
time.sleep(2)
driver.find_element_by_name("autor").send_keys("Queen")
time.sleep(1)
driver.find_element_by_name("cancion").send_keys("We are the champions")
time.sleep(1)
driver.find_element_by_name("album").send_keys("Live Killers")
time.sleep(1)
driver.find_element_by_name("añadir_cancion").click()
time.sleep(1)
driver.find_element_by_id("play We are the champions").click()
time.sleep(3)
driver.find_element_by_id("play Levitating").click()
time.sleep(3)
driver.find_element_by_name("Play Previous").click()
time.sleep(3)
driver.find_element_by_name("Play Next").click()
time.sleep(3)
driver.find_element_by_id("cola El Loco").click()
time.sleep(3)
driver.find_element_by_id("eliminar Mas").click()
time.sleep(3)
driver.find_element_by_id("cola Back In Black").click()
time.sleep(3)
driver.find_element_by_id("cola Africa").click()
time.sleep(3)
driver.find_element_by_name("Play Next").click()
time.sleep(3)
driver.find_element_by_id("eliminar cola Back In Black").click()
time.sleep(4)
driver.find_element_by_name("Play Next").click()
time.sleep(3)
driver.find_element_by_name("autor").send_keys("Bad Bunny")
time.sleep(1)
driver.find_element_by_name("cancion").send_keys("Te mudaste")
time.sleep(1)
driver.find_element_by_name("album").send_keys("El Ultimo Tour Del Mundo")
time.sleep(1)
driver.find_element_by_name("añadir_cancion").click()
time.sleep(1)
driver.find_element_by_id("play Te mudaste").click()
time.sleep(10)
driver.quit()