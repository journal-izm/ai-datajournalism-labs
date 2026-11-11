from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()                      # ① 크롬 열기
driver.get("file:///C:/class/shop.html")         # ② shop.html 위치로 바꾸기

items = driver.find_elements(By.CSS_SELECTOR, "li.item")
print("처음 상품 수:", len(items))

driver.find_element(By.ID, "more").click()       # ③ 더보기 클릭

WebDriverWait(driver, 10).until(                 # ④ 버튼이 사라질 때까지
    EC.invisibility_of_element_located((By.ID, "more")))

items = driver.find_elements(By.CSS_SELECTOR, "li.item")
sale  = driver.find_elements(By.CSS_SELECTOR, "li.item .sale")
print("클릭 후 상품 수:", len(items))
print(f"SALE {len(sale)}개 / 전체 {len(items)}개 = {len(sale)/len(items):.0%}")

driver.save_screenshot("after.png")              # ⑤ 화면 저장
driver.quit()                                    # ⑥ 닫기
