from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8000"}})  # 啟用跨域支援

def scrape_exchange_rate():
    options = Options()
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_argument("--headless")  # 進行除錯時可先關閉 headless 模式
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.huilv.vip/Visa/")
    time.sleep(8)
    try:
        wait = WebDriverWait(driver, 20)
        rate_container = wait.until(EC.presence_of_element_located((By.ID, "tbl_fx_scnytwd")))
        # 嘗試取得該容器內第一個 span 元素
        rate_element = rate_container.find_element(By.TAG_NAME, "span")
        exchange_rate = rate_element.text.strip()
    except Exception as e:
        driver.quit()
        raise e
    driver.quit()
    return exchange_rate

@app.route('/api/exchange-rate')
def get_exchange_rate():
    try:
        rate = scrape_exchange_rate()
        return jsonify({'exchange_rate': rate})
    except Exception as e:
        print("Error in get_exchange_rate:", e)
        return jsonify({'error': str(e)}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # 讓 Render 自動設定 PORT，預設為 5000
    app.run(host='0.0.0.0', port=port)
