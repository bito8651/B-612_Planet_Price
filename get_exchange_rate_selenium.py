from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 設定 Chrome 選項
options = Options()
# 指定 Chrome 可執行檔的路徑（請確認此路徑與你電腦上安裝的位置相符）
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
options.add_argument("--headless")  # 使用 headless 模式，不顯示瀏覽器視窗

# 啟動 ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 開啟目標網頁（Visa 匯率頁面）
driver.get("https://www.huilv.vip/Visa/")
# 等待足夠的時間，確保 JavaScript 載入完成
time.sleep(8)

# 印出網頁 HTML 內容供檢查
html = driver.page_source
if "tbl_fx_scnytwd" in html:
    print("在 page_source 中找到 tbl_fx_scnytwd！")
else:
    print("在 page_source 中未找到 tbl_fx_scnytwd。請檢查是否在 iframe 或網頁結構有變化。")
    # 將網頁內容輸出到檔案，方便進行調試
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(html)

# 使用明確等待等待目標元素出現
try:
    wait = WebDriverWait(driver, 20)
    rate_container = wait.until(EC.presence_of_element_located((By.ID, "tbl_fx_scnytwd")))
    # 在該元素中，尋找內部 class 為 "down" 的元素，其內含匯率數字
    rate_element = rate_container.find_element(By.CLASS_NAME, "down")
    exchange_rate = rate_element.text.strip()
    print("人民幣刷卡匯率（對台幣）：", exchange_rate)
except Exception as e:
    print("找不到匯率數據:", e)

# 關閉瀏覽器
driver.quit()
