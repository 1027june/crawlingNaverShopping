import pandas as pd
import urllib.request
import json
import time

# https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md 참고
client_id = "부여받은 ID"
client_secret = "부여받은 Secret Key"

query = input("검색어를 입력하세요 : ")
searchWord = query
query = urllib.parse.quote(query)

display = "&display=40" # 1페이지당 40개 Item
# 3page 120개, 80 + 시작 81에서 40

df = pd.DataFrame()

for i in range(0,3):
    start = f"&start={1+40*i}"
    url = "https://openapi.naver.com/v1/search/shop?query=" + query + display + start
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        data = response_body.decode('utf-8')
        result = json.loads(data)
        tdf = pd.DataFrame(result['items'])
        tdf['title'] = tdf['title'].str.replace(f'<b>{searchWord}</b>', searchWord)
        print(tdf)
        df = pd.concat([df, tdf], ignore_index=True)
    else:
        print("Error Code:" + rescode)
    time.sleep(1)

try:
    df.to_excel("네이버쇼핑API.xlsx")
    print("excel write complete")
except Exception as e:
    print(e)

