const API_URL = 'http://127.0.0.1:10000/api/exchange-rate';  // ✅ 確保這個 Port 正確

document.getElementById("convertBtn").addEventListener("click", async function() {
    // 取得使用者輸入的金額，並轉為數字格式
    const amountInput = document.getElementById("amount").value;
    const amount = parseFloat(amountInput);
    
    if (isNaN(amount)) {
        alert("請輸入有效金額！");
        return;
    }
    
    // 在換算過程中顯示等待訊息
    document.getElementById("result").innerText = "換算中，請耐心等候...";
    
    try {
        // 呼叫後端 API 取得最新匯率
        const response = await fetch(API_URL);
        const data = await response.json();
        
        if (data.exchange_rate) {
            const exchangeRate = parseFloat(data.exchange_rate);
            
            // 計算【商品金額】：金額 × 匯率，並無條件進位到個位數
            const productPrice = Math.ceil(amount * exchangeRate);
            
            // 計算【代購費】：金額 × 匯率 × 0.05，無條件進位到個位數
            let proxyFee = Math.ceil(amount * exchangeRate * 0.05);
            // 若計算出的代購費小於 30，則固定代購費為 30
            if (proxyFee < 30) {
                proxyFee = 30;
            }
            
            // 計算【3% 手續費】：
            // 當輸入金額大於 200 時，針對商品金額收取 3% 手續費，並無條件進位
            let extraFee = 0;
            let feeMessage = "";
            if (amount > 200) {
                extraFee = Math.ceil(productPrice * 0.03);
                feeMessage = "超過200人民幣，支付寶另收取3%手續費";
            }
            
            // 最終換算結果 = 商品金額 + 代購費 + 額外手續費
            const finalResult = productPrice + proxyFee + extraFee;
            
            document.getElementById("result").innerText = 
                `報價為：${finalResult} 元台幣\n${feeMessage}`;
        } else {
            document.getElementById("result").innerText = "無法獲取匯率";
        }
    } catch (error) {
        document.getElementById("result").innerText = "獲取匯率出錯";
        console.error("API 請求錯誤:", error); // ✅ 顯示錯誤訊息在 Console
    }
});
