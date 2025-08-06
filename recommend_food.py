import requests
import random
import os
from dotenv import load_dotenv
from datetime import datetime

README_PATH = "README.md"

# .env 파일에서 API 키를 로드합니다.
load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API 키가 .env 파일에 설정되어 있지 않습니다.")

# 현재 위치를 설정합니다. (예: 서울)
location = "37.581662478729505, 126.88620960317084"  # 위도, 경도 형식

def get_store_list():
    """google place api 를 호출하여 음식점 리스트를 가져옵니다."""
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    #메뉴 리스트
    food_list=['불고기','비빔밥','보쌈정식','전골','쌈밥','낙지볶음','간장게장','닭갈비','생선구이','된장찌개','순두부찌개','부대찌개','동태찌개','김치찌개','갈비탕','삼계탕','추어탕','청국장','짜장면','짬뽕','볶음밥','우동','간짜장','마라탕','중화비빔밥','굴짬뽕','잡채밥','초밥','일본라멘','덮밥','돈까스','우동','메밀소바','치즈돈까스','카레라이스','주먹밥','스파게티','함박스테이크','피자','수제햄버거','크림파스타','샐러드','필라프','부리또','타코','선지해장국','뼈해장국','우거지해장국','육개장','북어국','순대국','콩나물국밥','복국','쌀국수','샌드위치','토스트','편의점도시락','샐러드','김밥','밥버거','떡볶이','빵','와플','조각케익','칼국수','햄버거','본죽','잔치국수','월남쌈','수제비','타코야끼','핫도그','팟타이']

    # 1부터 100까지의 정수 중 72개 랜덤 생성 (중복 가능)
    random_numbers = random.randint(0, len(food_list)-1)
    rmd_food = food_list[random_numbers]

    radius = 1000  # 미터 단위 반경(예: 1km 내)

    params = {
        "query": rmd_food,
        "location": location,
        "radius": radius,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    content = ""
    content += f"오늘의 추천 음식 : {rmd_food}\n\n"
    if response.status_code == 200:
        results = response.json().get("results", [])

        if not results:
            content += "주변에 음식점이 없습니다.\n"
            return content

        for index, place in enumerate(results):
            if index >= 5:  # 상위 5개 음식점만 표시
                break
            content += f"\t이름: {place.get('name')}\n"
            content += f"\t주소: {place.get('formatted_address')}\n"
            content += f"\t위치: {place.get('geometry', {}).get('location')}\n"
            content += "\t" + "-" * 30 + "\n"
    else:
        content += f"Error {response.status_code}: {response.text}\n"

    return content


def update_readme():
    """README.md 파일을 업데이트"""
    store_info = get_store_list()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
    # Food Recommendation Status

    이 리포지토리는 Google Places API를 사용하여 서울의 음식점 정보를 자동으로 업데이트합니다.

    ## 상위 5개 이하의 음식점 정보
    > {store_info}

    ⏳ 업데이트 시간: {now} (UTC)

    ---
    자동 업데이트 봇에 의해 관리됩니다.
    """
    
    with open(README_PATH, "w", encoding="utf-8") as file:
            file.write(readme_content)

if __name__ == "__main__":
    update_readme()
