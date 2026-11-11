from bs4 import BeautifulSoup

html = open("shop.html", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")

items = soup.select("li.item")              # ① 상품 카드 전부
sale  = soup.select("li.item .sale")        # ② SALE 배지 전부

for item in items:                          # ③ 상품마다 이름·가격
    name  = item.select_one(".name").text
    price = item.select_one(".price").contents[0]
    print(name, price)

print(f"SALE {len(sale)}개 / 전체 {len(items)}개 = {len(sale)/len(items):.0%}")
