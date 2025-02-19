import requests
from bs4 import BeautifulSoup

# 目標網址
url = "https://www.huilv.vip/Visa/"

# 設定 headers（模擬瀏覽器）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

# 發送請求
response = requests.get(url, headers=headers)

# 確保請求成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到人民幣刷卡匯率（例如：人民幣對台幣）
    exchange_rate = soup.find("span", {"id": "tbl_fx_scnytwd"}).find("span").text.strip()


    if exchange_rate:
        print("人民幣刷卡匯率（對台幣）：", exchange_rate.text)
    else:
        print("未找到人民幣刷卡匯率")
else:
    print("無法訪問該網站，請稍後再試")
