from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("file:///C:/class/login.html")          # login.html 위치로 바꾸기

driver.find_element(By.ID, "username").send_keys("reporter")
driver.find_element(By.ID, "password").send_keys(getpass("비밀번호: "))
driver.find_element(By.ID, "login").click()

WebDriverWait(driver, 10).until(                    # 회원가가 뜰 때까지
    EC.presence_of_element_located((By.CLASS_NAME, "member-price")))

for item in driver.find_elements(By.CSS_SELECTOR, "li.item"):
    name  = item.find_element(By.CLASS_NAME, "name").text
    price = item.find_element(By.CLASS_NAME, "member-price").text
    print(name, price)
driver.quit()
