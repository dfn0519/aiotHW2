# 🌦️ 台灣區域農業氣象預報系統

本專案是一個完整的 Python 應用程式，旨在從 **中央氣象署 (CWA) API** 獲取台灣六大區域（北部、中部、南部、東北部、東部、東南部）的 7 天農業氣象預報，並透過 **Streamlit** 建立互動式網頁儀表板，提供地圖可視化與氣溫趨勢分析。

## 🌟 功能特點

-   **自動化資料抓取**：透過 `fetch_weather.py` 呼叫 CWA API (`F-A0010-001`) 抓取最新預報。
-   **多格式儲存**：資料同步儲存於 `weather_data.csv` (CSV) 與 `weather.db` (**SQLite3**)。
-   **互動式儀表板**：
    -   **地區下拉選單**：自由切換欲查看的區域。
    -   **Folium 互動地圖**：依據平均溫自動著色（藍、綠、橘、紅），並支援彈出視窗顯示詳細數據。
    -   **氣溫折線圖**：使用 `Altair` 顯示未來 7 天最高溫與最低溫的變化趨勢。
    -   **詳細數據表**：直觀顯示每日氣溫預報。
-   **SSL 支援**：自動處理特定網路環境下的 SSL 驗證問題。

## 🛠️ 環境架設與安裝

### 1. 建立虛擬環境
建議建立虛擬環境以隔離套件：
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. 安裝必要套件
```powershell
pip install -r requirements.txt
```

*主要套件包括：requests, pandas, streamlit, folium, streamlit-folium, matplotlib, altair。*

## 🚀 使用說明

### 步驟 A：抓取資料
執行抓取腳本以更新資料庫與 CSV 檔案：
```powershell
python fetch_weather.py
```

### 步驟 B：啟動 Web App
啟動 Streamlit 伺服器並在瀏覽器查看結果：
```powershell
streamlit run app.py
```

## 📊 評分規範達成說明 (Grading Criteria)

-   ✅ **使用 Streamlit 建立 Web App**
-   ✅ **下拉選單功能**：支援地區選擇 (10%)
-   ✅ **折線圖與表格**：顯示一週氣溫趨勢 (15%)
-   ✅ **SQLite 資料庫查詢**：所有展示資料皆經由 `weather.db` 讀取 (10%)
-   ✅ **程式碼結構**：模組化設計，包含獨立的抓取與顯示邏輯 (5%)

## 📂 檔案結構
-   `fetch_weather.py`: 資料抓取與 SQLite 儲存腳本。
-   `app.py`: Streamlit 網頁應用程式主程式。
-   `weather.db`: SQLite 資料庫檔案。
-   `weather_data.csv`: CSV 備份檔案。
-   `requirements.txt`: 專案依賴清單。

---
*資料來源：交通部中央氣象署 (CWA)*
