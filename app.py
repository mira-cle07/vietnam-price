import streamlit as st
import requests

# 設定網頁標題與圖示
st.set_page_config(page_title="估價報價系統", page_icon="✿", layout="centered")
st.title("✿ ViệtNam揪團估價機 ✿")

# 1. 自動抓取當天時下匯率
@st.cache_data(ttl=3600)  # 暫存 1 小時，避免重複頻繁讀取
def get_vnd_to_twd_rate():
    try:
        # 查詢 1 台幣(TWD) 等於多少越南盾(VND)
        url = "https://frankfurter.dev"
        response = requests.get(url, timeout=5)
        data = response.json()
        twd_to_vnd = data["rates"]["VND"]
        return 1 / twd_to_vnd
    except Exception:
        return 0.00135  # 網路斷線時的備用匯率

# 取得並顯示匯率
exchange_rate = get_vnd_to_twd_rate()
st.metric(label="📈今日代購費率 (VND → TWD)", value=f"{exchange_rate:.6f}")
st.caption("❁ 時下匯率+12%服務+3%跨國手續")
st.caption("❁ 匯率數據由系統自動連線即時更新")

st.divider()

# 2. 動態輸入原價
st.subheader("🛒 輸入商品原價（VND）")

prices = []
count = 1

while True:
    if count == 1 or (count > 1 and prices[-1] > 0):
        val = st.number_input(
            f"ヽ(✿ﾟ▽ﾟ)ノ輸入第 {count} 筆原價：(無後續請填0)", 
            min_value=0, 
            step=1000, 
            value=0,
            key=f"price_{count}"
        )
        prices.append(val)
        
        if val == 0:
            break
        count += 1
    else:
        break

valid_prices = [p for p in prices if p > 0]
n = len(valid_prices)

st.divider()

# 3. 計算與匯出報價金額
if n > 0:
    st.subheader("📋試算結果報價單")
    
    total_individual_quote = 0.0
    
    # 逐筆計算個別報價
    for i, original_price in enumerate(valid_prices, 1):
        # 公式：原價 * 時下匯率 * 1.15
        individual_quote = int(original_price * exchange_rate * 1.15 + 0.5)
        total_individual_quote += individual_quote
        
        # 【重點標記】放大加粗個別報價金額
    st.write(f"🪙 第 {i} 筆商品（原價 {original_price:,} VND）：")
    st.write(
	f"小計(不含運)：NT$ {individual_quote:.2f} 元</span>", 
            unsafe_allow_html=True
	)

    st.write("") # 留空行
    st.markdown(
            f"<br><span style='font-size: 20px; font-weight: bold; color: #000000; background-color: #FCCFDE; padding: 2px 8px; border-radius: 4px;'>"
            f"💰 報價金額總計：**{total_individual_quote:.2f}** 元", 
            unsafe_allow_html=True
        )

else:
    st.info("請於上方輸入原價，系統將自動為您報價🤑")
