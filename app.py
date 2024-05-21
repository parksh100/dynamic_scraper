from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)
page = browser.new_page()

page.goto("https://www.pkic.kr/kic/module/kicMovein/index.do?menu_idx=57")

time.sleep(5)

content = page.content()

# page.click("span:has-text(\"입주기업\")")

# time.sleep(5)
p.stop()

soup = BeautifulSoup(content, 'html.parser')

rows = soup.find('tbody').find_all('tr')

print(rows)

company_db = []

for row in rows:
    # 각 tr 요소에서 th 및 td 요소 추출
    room = row.find('th').text.strip()
    company_name = row.find_all('td')[0].text.strip()
    ceo = row.find_all('td')[1].text.strip()
    product = row.find_all('td')[2].text.strip()
    tel = row.find_all('td')[3].text.strip()
    
    # 홈페이지 링크와 상세보기 링크 추출
    homepage_link = row.find('a', class_='home-btn')
    detail_link = row.find('a', class_='more-btn')

    company = {
        'room': room,
        'company_name': company_name,
        'ceo': ceo,
        'product': product,
        'tel': tel,
        'homepage_link': homepage_link['href'] if homepage_link else None,
        'detail_link': detail_link['href'] if detail_link else None
    }

    company_db.append(company)

    # print(company_db)
    # print(len(company_db))

file = open("company_db.csv", "w")
writer = csv.writer(file)
writer.writerow(["room", "company_name", "ceo", "product", "tel", "homepage_link", "detail_link"])
for company in company_db:
    writer.writerow(list(company.values())) # values() 메서드로 딕셔너리의 값만 추출