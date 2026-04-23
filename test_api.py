import requests, json

url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-E5510A11-13B3-4E4B-B90B-B413719E16E5&format=JSON"
r = requests.get(url, verify=False)
data = r.json()

with open("temp_output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
