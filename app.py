from flask import Flask, jsonify, render_template
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ 允許所有來源的 CORS 請求

def scrape_exchange_rate():
    options = Options()
    options.add_argument("--headless")  # ✅ 必須啟用 headless，Render 無法顯示 UI
    options.add_argument("--no-sandbox")  # ✅ 避免 Render 權限錯誤
    options.add_argument("--disable-dev-shm-usage")  # ✅ 防止 Render 內存不足
    options.binary_location = "/usr/bin/google-chrome"  # ✅ 使用 Render 預設的 Chrome 位置

    # ✅ 這裡不使用 `ChromeDriverManager`，改用 Render 內建的 chromedriver
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.huilv.vip/Visa/")
    
    time.sleep(8)  # ✅ 避免網站尚未載入完成

    try:
        wait = WebDriverWait(driver, 20)
        rate_container = wait.until(EC.presence_of_element_located((By.ID, "tbl_fx_scnytwd")))
        rate_element = rate_container.find_element(By.TAG_NAME, "span")
        exchange_rate = rate_element.text.strip()
        print(f"獲取匯率成功: {exchange_rate}")  # ✅ 顯示在 Render Logs
    except Exception as e:
        print("Error in scrape_exchange_rate:", e)  # ✅ 顯示錯誤
        exchange_rate = "N/A"  # 如果出錯，返回 N/A
    
    driver.quit()
    return exchange_rate

# ✅ 讓 Flask 正確讀取 `templates/index.html`
@app.route('/')
def home():
    return render_template("index.html")  # Flask 會從 `templates/` 找 `index.html`

# ✅ API 端點
@app.route('/api/exchange-rate')
def get_exchange_rate():
    try:
        rate = scrape_exchange_rate()
        return jsonify({'exchange_rate': rate})
    except Exception as e:
        print("Error in get_exchange_rate:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # ✅ Render 會自動設定 PORT
    app.run(host='0.0.0.0', port=port)
