# 📝 開發歷程與對話紀錄摘要

本專案從需求確認到最終優化經歷了以下幾個主要階段，這份摘要記錄了開發過程中的技術選擇與問題解決：

## 階段 1：基礎建設與資料抓取 (Initial Setup)
*   **任務**：建立抓取 CWA API `F-A0010-001` 的基礎 Python 腳本。
*   **挑戰**：解決網路環境中的 SSL 驗證問題。
*   **解決**：使用 `urllib3.disable_warnings` 並在 `requests.get` 中設定 `verify=False`。

## 階段 2：API 端點與路徑修正 (API Troubleshooting)
*   **問題**：原先的 `rest/datastore` 端點回傳 404 錯誤。
*   **修正**：根據使用者提供的正確路徑更換為 `fileapi` 端點，並重新設計 JSON 解析邏輯以符合 `cwaopendata` 的層級結構。
*   **區域名稱優化**：經由測試腳本 `check_names.py` 確認 API 的確切回傳名稱為「地區」而非「區域」，並修正「東南部地區」的關鍵字匹配。

## 階段 3：SQLite3 資料庫整合 (Database Integration)
*   **需求**：將資料儲存由純 CSV 升級為 SQLite3 查詢，以符合學術/專案評分標準。
*   **實作**：在 `fetch_weather.py` 中加入 `sqlite3` 與 `pandas.to_sql` 邏輯，建立 `weather.db`。

## 階段 4：Streamlit UI 優化與圖表功能 (UI/UX Enhancement)
*   **功能**：加入地區下拉選單、日期滑動拉桿。
*   **數據可視化**：
    *   整合 **Folium** 地圖進行空間分布展示。
    *   使用 **Altair** 繪製互動式折線圖，展示最高溫與最低溫的 7 天趨勢。
*   **套件修正**：發現 Pandas 的 `background_gradient` 功能需要 `matplotlib` 支持，隨即進行安裝與補強。

## 階段 5：專案交付 (Final Delivery)
*   **產出**：建立完整的 `README.md`，總結安裝步驟、執行方式與功能亮點。

---
**開發者筆記**：此專案展現了從原始資料 (Raw Data) 到結構化存儲 (SQLite)，最後到互動式分析 (Web App) 的完整數據處理流程 (Data Pipeline)。
