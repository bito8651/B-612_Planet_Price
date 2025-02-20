import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# ✅ 使用 Render 內建的 Chrome & Chromedriver
CHROME_PATH = "/usr/bin/chromium-browser"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ 允許所有來源的 CORS 請求

def scrape_exchange_rate():
    options = Options()
    options.add_argument("--headless")  # ✅ Render 必須使用 headless 模式
    options.add_argument("--no-sandbox")  # ✅ 防止權限問題
    options.add_argument("--disable-dev-shm-usage")  # ✅ 防止記憶體錯誤
    options.binary_location = CHROME_PATH  # ✅ Render 內建的 Chromium 位置

    # ✅ 使用 Render 內建的 chromedriver
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    driver.get("https://www.huilv.vip/Visa/")
    
    time.sleep(8)

    try:
        wait = WebDriverWait(driver, 20)
        rate_container = wait.until(EC.presence_of_element_located((By.ID, "tbl_fx_scnytwd")))
        rate_element = rate_container.find_element(By.TAG_NAME, "span")
        exchange_rate = rate_element.text.strip()
        print(f"✅ 獲取匯率成功: {exchange_rate}")  # ✅ 顯示在 Render Logs
    except Exception as e:
        print("❌ Error in scrape_exchange_rate:", e)  # ✅ 顯示錯誤
        exchange_rate = "N/A"
    
    driver.quit()
    return exchange_rate

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/exchange-rate')
def get_exchange_rate():
    try:
        rate = scrape_exchange_rate()
        return jsonify({'exchange_rate': rate})
    except Exception as e:
        print("❌ Error in get_exchange_rate:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # ✅ Render 會自動設定 PORT
    app.run(host='0.0.0.0', port=port)
