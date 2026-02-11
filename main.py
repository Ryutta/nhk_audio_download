from time import sleep

# import requests
# from bs4 import BeautifulSoup
import dl
from selenium import webdriver
from selenium.webdriver.common.by import By
 
options = webdriver.ChromeOptions()
# options.add_argument('--headless=new')
options.add_argument('--incognito')
driver = webdriver.Chrome(options=options)

# URL, 名称の取得

# # ラジオ英会話
# url="https://www.nhk.or.jp/radio/ondemand/detail.html?p=PMMJ59J6N2_01"
# # 英会話タイムトライアル
# url = "https://www.nhk.or.jp/radio/ondemand/detail.html?p=8Z6XJ6J415_01"
# # 現代英語
# url = "https://www.nhk.or.jp/radio/ondemand/detail.html?p=77RQWQX1L6_01"
# ラジオビジネス英語
url = "https://www.nhk.or.jp/radio/ondemand/detail.html?p=368315KKP8_01"
# # # 特別番組
# url = "https://www.nhk.or.jp/radio/ondemand/detail.html?p=9P21KNR8GG_01"

# fname="sample.mp3"p

driver.implicitly_wait(10)

driver.get(url)
sleep(3)

targets = driver.find_elements(By.CSS_SELECTOR, "section.section-detail div.program-archive-item")

for target in targets:
    s = target.find_element(By.CSS_SELECTOR, ".program-archive-link span.d1").text
    index = s.find("日")
    fname = s[:index+1]
    print(fname)
    target2 = target.find_element(By.CSS_SELECTOR,"div.nol_audio_player_base")
    target_url = target2.get_attribute('data-hlsurl')
    print(target_url)    
    dl.dlm3u8(target_url,fname+'.mp3')



# html = driver.page_source
# print(html)
# driver.quit


# r = requests.get(url)
# r.raise_for_status()

# soup = BeautifulSoup(r.content, 'lxml')
# # soup = BeautifulSoup(r.content)

# items = soup.select('section.section-detail div.contents-inner div.program-archive-list div.program-archive-item')
# print(items)

