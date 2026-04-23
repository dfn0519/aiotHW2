import streamlit as st
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium
import os

# 設定網頁標題與版面 (left-right layout)
st.set_page_config(page_title="氣溫預報 Web App", layout="wide")

st.title("🌦️ 台灣氣溫預報 Web App (一週預報)")
st.markdown("使用 CWA API 獲取農業氣象預報資料，顯示全台六大區域氣溫預測。")

# 1. 從 SQLite3 資料庫讀取資料
@st.cache_data
def load_data():
    try:
        conn = sqlite3.connect('data.db')
        df = pd.read_sql_query("SELECT * FROM TemperatureForecasts", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"無法讀取資料庫，請確定是否已執行 `fetch_weather.py` 且已正確儲存 `data.db`。\n錯誤訊息: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("⚠️ 目前沒有資料可顯示。請先設定 `.env` 檔案中的 `CWA_API_KEY`，然後執行 `python fetch_weather.py` 來抓取資料並建立資料庫。")
else:
    # --- 準備資料與輔助函數 ---
    dates = df['dataDate'].unique()
    regions = df['regionName'].unique()
    
    # 近似座標 (緯度, 經度)
    region_coords = {
        "北部": [25.0330, 121.5654],
        "中部": [24.1477, 120.6736],
        "南部": [22.9999, 120.2269],
        "東北部": [24.7525, 121.7582],
        "東部": [23.9772, 121.6062],
        "東南部": [22.7661, 121.1396]
    }
    
    # 依據平均溫度決定顏色 (blue <20°C, green 20-25°C, yellow 25-30°C, red >30°C)
    def get_color(temp):
        if temp < 20: return '#3498db'     # blue
        elif 20 <= temp < 25: return '#2ecc71' # green
        elif 25 <= temp <= 30: return '#f1c40f' # yellow
        else: return '#e74c3c'             # red

    # ==========================================
    # 版面：Left-Right Layout (左：地圖，右：該日表格)
    # ==========================================
    st.header("🗺️ 全台氣溫地圖 (依日期檢視)")
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        selected_date = st.selectbox("請選擇日期：", dates, key="date_selector")
        
        # 篩選選定日期的資料
        date_data = df[df['dataDate'] == selected_date]
        
        # 建立 Folium 地圖
        m = folium.Map(location=[23.6978, 120.9605], zoom_start=7)
        
        # 加上標記
        for _, row in date_data.iterrows():
            region = row['regionName']
            if region in region_coords:
                avg_temp = (row['mint'] + row['maxt']) / 2
                color = get_color(avg_temp)
                
                popup_content = f"<b>{region}</b><br>最低溫: {row['mint']}°C<br>最高溫: {row['maxt']}°C"
                
                folium.CircleMarker(
                    location=region_coords[region],
                    radius=15,
                    popup=folium.Popup(popup_content, max_width=200),
                    tooltip=f"{region} (平均 {avg_temp:.1f}°C)",
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.8
                ).add_to(m)
        
        # 顯示地圖
        st_folium(m, width=500, height=450)
        st.markdown("<small>圓圈顏色說明: 🟦 < 20°C | 🟩 20-25°C | 🟨 25-30°C | 🟥 > 30°C</small>", unsafe_allow_html=True)
        
    with col_right:
        st.subheader(f"📅 {selected_date} 各區氣溫資料")
        # 顯示 Data Table
        display_df = date_data[['regionName', 'mint', 'maxt']].copy()
        display_df.columns = ['地區', '最低溫 (°C)', '最高溫 (°C)']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
    st.divider()
    
    # ==========================================
    # 版面：地區一週氣溫趨勢 (折線圖 + 表格)
    # ==========================================
    st.header("📈 地區一週氣溫預報")
    selected_region = st.selectbox("請選擇地區：", regions, key="region_selector")
    
    region_data = df[df['regionName'] == selected_region]
    
    col_chart, col_table = st.columns([3, 2])
    
    with col_chart:
        st.subheader(f"{selected_region} - 一週氣溫折線圖")
        chart_data = region_data.set_index('dataDate')[['mint', 'maxt']]
        chart_data.columns = ['最低溫', '最高溫']
        # 折線圖
        st.line_chart(chart_data, color=['#3498db', '#e74c3c'])
        
    with col_table:
        st.subheader(f"{selected_region} - 一週氣溫資料表")
        table_df = region_data[['dataDate', 'mint', 'maxt']].copy()
        table_df.columns = ['日期', '最低溫 (°C)', '最高溫 (°C)']
        st.dataframe(table_df, use_container_width=True, hide_index=True)

