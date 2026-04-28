import requests
import pandas as pd
import json
import urllib3

# 停用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_cwa_weather():
    api_key = "CWA-E5510A11-13B3-4E4B-B90B-B413719E16E5"
    # 使用 user 提供的正確 URL
    url = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization={api_key}&format=JSON"
    
    try:
        print(f"Fetching data from: {url}")
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()
        
        # 根據 fileapi 的結構進入資料層
        # 結構: cwaopendata -> resources -> resource -> data -> agrWeatherForecasts -> weatherForecasts -> location
        locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
        
        weather_list = []
        
        # 定義目標區域對應 (API 中是 "地區")
        target_regions = {
            "北部地區": "Northern",
            "中部地區": "Central",
            "南部地區": "Southern",
            "東北部地區": "Northeastern",
            "東部地區": "Eastern",
            "東南部地區": "Southeastern"
        }
        
        for loc in locations:
            location_name = loc['locationName']
            if location_name in target_regions:
                # 取得氣溫元素 (MinT, MaxT)
                elements = loc['weatherElements']
                
                daily_data = {}
                
                # 處理最低溫 MinT
                if 'MinT' in elements:
                    for day in elements['MinT']['daily']:
                        date = day['dataDate']
                        temp = float(day['temperature'])
                        if date not in daily_data:
                            daily_data[date] = {"Date": date, "Region": location_name, "EnglishRegion": target_regions[location_name]}
                        daily_data[date]['MinTemp'] = temp
                
                # 處理最高溫 MaxT
                if 'MaxT' in elements:
                    for day in elements['MaxT']['daily']:
                        date = day['dataDate']
                        temp = float(day['temperature'])
                        if date not in daily_data:
                            daily_data[date] = {"Date": date, "Region": location_name, "EnglishRegion": target_regions[location_name]}
                        daily_data[date]['MaxTemp'] = temp
                
                weather_list.extend(daily_data.values())
        
        # 轉換為 DataFrame
        df = pd.DataFrame(weather_list)
        
        # 計算平均溫度
        df['AvgTemp'] = (df['MinTemp'] + df['MaxTemp']) / 2
        
        # 儲存為 CSV
        df.to_csv("weather_data.csv", index=False, encoding="utf-8-sig")
        
        # --- 新增：儲存至 SQLite3 資料庫 ---
        import sqlite3
        conn = sqlite3.connect("weather.db")
        # 將資料存入 weather_forecast 表格，如果已存在則替換
        df.to_sql("weather_forecast", conn, if_exists="replace", index=False)
        conn.close()
        # -------------------------------
        
        print("Successfully saved weather data to weather_data.csv and weather.db")
        print(f"Total records saved: {len(df)}")
        return df

    except Exception as e:
        print(f"Error fetching data: {e}")
        # 如果結構不對，印出 key 幫助除錯
        if 'data' in locals():
            print("Top level keys:", data.keys())
        return None

if __name__ == "__main__":
    fetch_cwa_weather()
