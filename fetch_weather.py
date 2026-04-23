import os
import requests
import json
import sqlite3
import pandas as pd
from dotenv import load_dotenv
import urllib3

# 忽略 SSL 憑證警告 (根據作業要求)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 載入 .env 檔案中的環境變數
load_dotenv()

# CWA API 相關設定
API_KEY = os.getenv("CWA_API_KEY")
URL = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization={API_KEY}&format=JSON"

def fetch_and_process_data():
    if not API_KEY or API_KEY == "your_api_key_here":
        print("警告: 請在 .env 檔案中設定您的 CWA_API_KEY。")
        return None
        
    try:
        print("開始獲取天氣預報資料...")
        # 處理 SSL verification issues (verify=False)
        response = requests.get(URL, verify=False)
        response.raise_for_status()
        data = response.json()
        
        # 作業要求: 使用 json.dumps 觀察獲得的資料 (印出前 1000 個字元避免洗版)
        print("\n--- 觀察獲得的資料 (部分預覽) ---")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
        print("...\n")
        
        # 尋找資料位置 (根據 fileapi/F-A0010-001 的 JSON 結構)
        try:
            loc_list = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
        except KeyError:
            print("錯誤: 找不到 Location 資料結構，API 回傳格式可能已變更。")
            return None

        # 需要提取的目標地區 (API 回傳為 '北部地區' 等，我們需要映射為 '北部' 以符合作業要求)
        target_regions = {"北部地區": "北部", "中部地區": "中部", "南部地區": "南部", "東北部地區": "東北部", "東部地區": "東部", "東南部地區": "東南部"}
        parsed_data = []
        
        for location in loc_list:
            api_region_name = location.get('locationName')
            
            if api_region_name in target_regions:
                region_name = target_regions[api_region_name] # 轉換為作業要求的名稱，例如 "北部"
                elements = location.get('weatherElements', {})
                
                maxt_daily = elements.get('MaxT', {}).get('daily', [])
                mint_daily = elements.get('MinT', {}).get('daily', [])
                
                if maxt_daily and mint_daily:
                    for i in range(min(len(maxt_daily), len(mint_daily))):
                        try:
                            # 提取時間與溫度值
                            date = maxt_daily[i].get('dataDate')
                            maxt_val = maxt_daily[i].get('temperature')
                            mint_val = mint_daily[i].get('temperature')
                            
                            parsed_data.append({
                                'regionName': region_name,
                                'dataDate': date,
                                'mint': int(mint_val),
                                'maxt': int(maxt_val)
                            })
                        except Exception as e:
                            print(f"解析 {region_name} 溫度資料時發生錯誤: {e}")
                            
        if not parsed_data:
            print("錯誤: 未找到符合目標地區的資料。")
            return None
            
        df = pd.DataFrame(parsed_data)
        df = df.drop_duplicates(subset=['regionName', 'dataDate'])
        
        # 作業要求: 使用 json.dumps 觀察提取的資料
        print("\n--- 觀察提取的資料 (JSON) ---")
        print(json.dumps(parsed_data[:2], indent=2, ensure_ascii=False))
        print(f"... 共提取了 {len(parsed_data)} 筆資料\n")
        
        return df

    except Exception as e:
        print(f"錯誤: 發生異常: {e}")
        return None

def save_to_db(df):
    """作業要求: 將氣溫資料儲存到 SQLite3 資料庫"""
    db_name = 'data.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 建立 Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TemperatureForecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            regionName TEXT,
            dataDate TEXT,
            mint INTEGER,
            maxt INTEGER
        )
    ''')
    
    # 清空現有資料避免重複
    cursor.execute('DELETE FROM TemperatureForecasts')
    
    # 寫入資料
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO TemperatureForecasts (regionName, dataDate, mint, maxt)
            VALUES (?, ?, ?, ?)
        ''', (row['regionName'], row['dataDate'], row['mint'], row['maxt']))
        
    conn.commit()
    conn.close()
    print(f"成功將資料存入資料庫 {db_name} (Table: TemperatureForecasts)。")

def check_db_data():
    """作業要求: 從資料庫查詢資料，來檢查資料是否正確被存入資料庫"""
    conn = sqlite3.connect('data.db')
    
    # 1. 列出所有地區名稱
    print("\n--- 資料庫檢查: 列出所有地區名稱 ---")
    regions = pd.read_sql_query("SELECT DISTINCT regionName FROM TemperatureForecasts", conn)
    print(regions.to_string(index=False))
    
    # 2. 列出中部地區的氣溫資料
    print("\n--- 資料庫檢查: 列出中部地區的氣溫資料 ---")
    central_data = pd.read_sql_query("SELECT * FROM TemperatureForecasts WHERE regionName = '中部'", conn)
    print(central_data.to_string(index=False))
    
    conn.close()

def save_to_csv(df):
    """儲存為 CSV (weather_data.csv)"""
    file_name = 'weather_data.csv'
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"成功將資料存入 CSV 檔案 {file_name}。")

if __name__ == "__main__":
    df = fetch_and_process_data()
    if df is not None and not df.empty:
        save_to_csv(df)
        save_to_db(df)
        check_db_data()
