import requests
from bs4 import BeautifulSoup

url = "https://www.huilv.vip/"  # 你的目標網站
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# 取得網頁內容
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 檢查 HTML 內容
print(soup.prettify())  # 輸出 HTML 來檢查是否有 "tbl_fx_scnytwd"
