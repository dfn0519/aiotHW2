# 🌦️ 氣溫預報 Web App (HW2)

這是一個使用中央氣象署 (CWA) API 獲取氣溫預報資料的 Web App 專案，具備資料庫儲存與資料視覺化功能。

## 📝 開發日誌 (Development Log)

* **環境建置與套件安裝**：建立了 Python 虛擬環境 (`venv`) 並安裝 `requests`, `pandas`, `streamlit`, `folium`, `streamlit-folium`, `python-dotenv`。
* **HW2-1 獲取天氣預報資料**：實作 `fetch_weather.py`，使用 `requests` 向 CWA API (`F-A0010-001` 農業氣象預報) 發送請求，並忽略 SSL 憑證警告 (`verify=False`)。成功獲取 JSON 資料並使用 `json.dumps` 觀察結構。
* **HW2-2 分析與提取資料**：分析 JSON 結構，安全地提取「北部、中部、南部、東北部、東部、東南部」的 `MaxT` (最高溫) 與 `MinT` (最低溫)，整理成 `pandas.DataFrame` 並去除重複資料。
* **HW2-3 儲存至 SQLite3 資料庫**：建立 `data.db`，設計 `TemperatureForecasts` 資料表 (含 `id`, `regionName`, `dataDate`, `mint`, `maxt` 欄位)。將 Pandas DataFrame 的資料寫入資料庫，並額外儲存為 `weather_data.csv`。實作 SQL 查詢指令驗證資料寫入正確性。
* **HW2-4 實作 Streamlit Web App**：
  * **版面配置**：設定為 `layout="wide"`，分為上下兩大區塊。
  * **上方區塊 (地圖與當日表格 - Left-Right Layout)**：
    * 左側：使用 `folium` 實作全台氣溫地圖。透過下拉選單選擇日期，地圖上的標記會依據平均溫度變色 (藍 <20°C, 綠 20-25°C, 黃 25-30°C, 紅 >30°C)，點擊有詳細彈出視窗。
    * 右側：顯示該選定日期的所有地區氣溫表格。
  * **下方區塊 (一週趨勢折線圖)**：
    * 提供地區下拉選單，選定地區後，左側顯示一週氣溫折線圖，右側顯示一週氣溫表格。
* **資安與部署準備**：將 CWA API Token 移至 `.env` 檔案中，避免將金鑰寫死在程式碼裡，防範資安外洩。

---

## 🚀 如何在本地端執行 (Local Run)

1. **取得 CWA API 授權碼**：
   * 前往 [中央氣象署開放資料平台](https://opendata.cwa.gov.tw/) 註冊帳號並取得授權碼 (API Key)。
2. **設定 `.env` 檔案**：
   * 開啟專案中的 `.env` 檔案，將 `your_api_key_here` 替換為您的實際 API Key。
     ```env
     CWA_API_KEY=CWA-XXXXX-XXXXX-XXXXX-XXXXX
     ```
3. **安裝依賴套件**：
   ```bash
   pip install -r requirements.txt
   ```
4. **抓取資料並建立資料庫**：
   ```bash
   python fetch_weather.py
   ```
   * *此步驟會產生 `data.db` 與 `weather_data.csv`，終端機也會印出觀察資料。*
5. **啟動 Web App**：
   ```bash
   streamlit run app.py
   ```

---

## 🌐 如何部署到 GitHub 與 Streamlit Community Cloud

### 1. 推送到 GitHub
1. 在專案資料夾初始化 Git (若尚未初始化)：
   ```bash
   git init
   ```
2. **非常重要**：建立一個名為 `.gitignore` 的檔案，確保不會把隱私資料和資料庫推送到公開的 GitHub：
   ```text
   .env
   __pycache__/
   venv/
   .streamlit/
   data.db
   ```
3. 加入檔案並提交：
   ```bash
   git add .
   git commit -m "Initial commit for HW2 Weather App"
   ```
4. 在 GitHub 建立一個新的 Repository，並依照指示推送到遠端：
   ```bash
   git remote add origin https://github.com/您的帳號/專案名稱.git
   git branch -M main
   git push -u origin main
   ```

### 2. 部署到 Streamlit Community Cloud (Live Demo)
由於這是公開展示，且我們不能把 `.env` 上傳到 GitHub，因此需在 Streamlit 後台設定環境變數：

1. 前往 [Streamlit Community Cloud](https://share.streamlit.io/) 並登入 (可用 GitHub 帳號登入)。
2. 點擊 **"New app"**，授權連結到您的 GitHub Repository。
3. 選擇您剛剛上傳的 Repository，Branch 選擇 `main`，Main file path 輸入 `app.py`。
4. **設定環境變數 (Secrets)**：
   * 點擊右側的 "Advanced settings"。
   * 在 Secrets 區塊中輸入您的 API Key：
     ```toml
     CWA_API_KEY = "CWA-XXXXX-XXXXX-XXXXX-XXXXX"
     ```
     *(注意：Streamlit Cloud 會自動將 Secrets 注入為環境變數，因此 `os.getenv("CWA_API_KEY")` 可以成功讀取)*
5. 點擊 **"Deploy"**，等待幾分鐘，您的 Live Demo 就會成功上線！
*(注意：若在雲端環境無法自動執行 `fetch_weather.py`，可以在 `app.py` 中增加判斷，如果沒有 `data.db` 則在 Streamlit 啟動時自動呼叫 `fetch_weather.py` 裡的函式來初始化資料。)*
