import os
import subprocess
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ✅ Render 環境變數
CHROME_PATH = "/usr/bin/google-chrome"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ 允許所有來源的 CORS 請求

def install_chrome():
    """ ✅ Render 環境無法使用 apt-get install，因此手動下載 Chrome 和 Chromedriver """
    if not os.path.exists(CHROME_PATH) or not os.path.exists(CHROMEDRIVER_PATH):
        try:
            print("🔹 安裝 Google Chrome & Chromedriver...")
            subprocess.run("wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", shell=True, check=True)
            subprocess.run("dpkg -i google-chrome-stable_current_amd64.deb || true", shell=True, check=True)
            subprocess.run("rm google-chrome-stable_current_amd64.deb", shell=True, check=True)
            subprocess.run("wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip", shell=True, check=True)
            subprocess.run("unzip chromedriver_linux64.zip", shell=True, check=True)
            subprocess.run("mv chromedriver /usr/bin/chromedriver", shell=True, check=True)
            subprocess.run("chmod +x /usr/bin/chromedriver", shell=True, check=True)
            print("✅ 安裝完成！")
        except subprocess.CalledProcessError as e:
            print("❌ 安裝失敗:", e)

install_chrome()  # ✅ 在 Flask 啟動時安裝 Chrome

def scrape_exchange_rate():
    options = Options()
    options.add_argument("--headless")  # ✅ Render 必須使用 headless 模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = CHROME_PATH  # ✅ 使用 Render 預設的 Chrome 位置

    # ✅ 使用 Render 內建的 chromedriver
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    driver.get("https://www.huilv.vip/Visa/")
    
    time.sleep(8)

    try:
        wait = WebDriverWait(driver, 20)
        rate_container = wait.until(EC.presence_of_element_located((By.ID, "tbl_fx_scnytwd")))
        rate_element = rate_container.find_element(By.TAG_NAME, "span")
        exchange_rate = rate_element.text.strip()
        print(f"獲取匯率成功: {exchange_rate}")  # ✅ 顯示在 Render Logs
    except Exception as e:
        print("Error in scrape_exchange_rate:", e)  # ✅ 顯示錯誤
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
        print("Error in get_exchange_rate:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # ✅ Render 會自動設定 PORT
    app.run(host='0.0.0.0', port=port)
