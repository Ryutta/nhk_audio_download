import re
from time import sleep
import dl
from selenium import webdriver
from selenium.webdriver.common.by import By
 
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--incognito')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=options)

# 4つの番組のURLと名称のリスト
programs = [
    {"name": "ラジオ英会話", "url": "https://www.nhk.or.jp/radio/ondemand/detail.html?p=PMMJ59J6N2_01"},
    {"name": "英会話タイムトライアル", "url": "https://www.nhk.or.jp/radio/ondemand/detail.html?p=8Z6XJ6J415_01"},
    {"name": "現代英語", "url": "https://www.nhk.or.jp/radio/ondemand/detail.html?p=77RQWQX1L6_01"},
    {"name": "ラジオビジネス英語", "url": "https://www.nhk.or.jp/radio/ondemand/detail.html?p=368315KKP8_01"}
]

driver.implicitly_wait(10)

for program in programs:
    name = program["name"]
    url = program["url"]
    print(f"=== {name} のダウンロードを開始します ===")
    
    driver.get(url)
    sleep(3)

    targets = driver.find_elements(By.CSS_SELECTOR, "section.section-detail div.program-archive-item")

    for target in targets:
        try:
            s = target.find_element(By.CSS_SELECTOR, ".program-archive-link span.d1").text
            index = s.find("日")
            if index != -1:
                date_str = s[:index+1].strip()
            else:
                date_str = s.strip()
            
            # 放映回数を取得する
            episode_str = ""
            try:
                title_elem = target.find_element(By.CSS_SELECTOR, "h2.title")
                m = re.search(r'\(\d+\)', title_elem.text)
                if m:
                    episode_str = m.group(0)
            except Exception:
                pass

            # ファイル名を「番組名_日付_放映回数.mp3」にする
            if episode_str:
                fname = f"{name}_{date_str}_{episode_str}"
            else:
                fname = f"{name}_{date_str}"

            print(f"ダウンロード中: {fname}.mp3")
            
            target2 = target.find_element(By.CSS_SELECTOR,"div.nol_audio_player_base")
            target_url = target2.get_attribute('data-hlsurl')
            
            if target_url:
                dl.dlm3u8(target_url, fname + '.mp3')
            else:
                print(f"音声URLが取得できませんでした: {fname}")
        except Exception as e:
            print(f"処理中にエラーが発生しました: {e}")

driver.quit()
