from time import sleep
import dl
from selenium import webdriver
from selenium.webdriver.common.by import By
 
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--incognito')
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

            # ファイル名を「番組名_日付.mp3」にする
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
