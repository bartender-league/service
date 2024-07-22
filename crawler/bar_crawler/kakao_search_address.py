from difflib import SequenceMatcher

import pandas as pd
import requests
import os

print(os.getcwd())

# Kakao API 키
API_KEY = '23dbc33ecc3cc990e2b300e4ce862773'  # 여기서 YOUR_KAKAO_API_KEY를 발급받은 키로 대체하세요


# Bar 클래스 정의
class Bar:
    def __init__(self, title, sido, sigungu, address, phone):
        self.title = title
        self.sido = sido
        self.sigungu = sigungu
        self.address = address
        self.phone = phone
        self.isChecked = False

    def __str__(self):
        return f"Title: {self.title}, Sido: {self.sido}, Sigungu: {self.sigungu}, Address: {self.address}, Phone: {self.phone}, isChecked: {self.isChecked}"


# 공백 제거 및 최소 연속 글자 길이 확인 함수
def remove_spaces_and_check_continuous_chars(str1, str2, min_length=2):
    str1 = str(str1).replace(" ", "")
    str2 = str(str2).replace(" ", "")

    # Check for minimum continuous matching characters
    for i in range(len(str1) - min_length + 1):
        substring = str1[i:i + min_length]
        if substring in str2:
            return True
    return False


# 특정 좌표 근처의 장소 목록을 검색하는 함수
def search_places(address):
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={address}&page=1&size=15"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    response = requests.get(url, headers=headers)
    result = response.json()

    places = []
    if result['documents']:
        for document in result['documents']:
            place = {
                'name': document['place_name'],
                'address': document['road_address_name'],
                'phone': document['phone'],
                'category': document['category_name']
            }
            places.append(place)
    return places


# 파일 읽기 및 검색 실행 함수
def process_csv_files(file_index):
    try:
        # CSV 파일을 DataFrame으로 읽기
        csv_file_path = f'bar_result_{file_index}.csv'
        df = pd.read_csv(csv_file_path, header=None, names=["Title", "Sido", "Sigungu", "Address", "Phone"])

        # DataFrame의 각 행을 Bar 객체로 변환
        bars = [Bar(row['Title'], row['Sido'], row['Sigungu'], row['Address'], row['Phone']) for index, row in df.iterrows()]

        # 각 Bar 객체의 주소를 사용해 장소 검색
        # 각 Bar 객체의 주소를 사용해 장소 검색
        for bar in bars:
            print(f"Searching places near: {bar.address}")
            places = search_places(bar.address)
            for place in places:
                if remove_spaces_and_check_continuous_chars(bar.title, place['name']):
                    bar.isChecked = True
                    break

            print(f"bar info: {bar}")

        # 체크 완료된 결과를 새로운 CSV 파일로 저장
        checked_file_path = f'bar_result_{file_index}_checked.csv'
        with open(checked_file_path, 'w', encoding='utf-8-sig') as f:
            for bar in bars:
                f.write(f"{bar.title},{bar.sido},{bar.sigungu},{bar.address},{bar.phone},{bar.isChecked}\n")

        print(f"Checked results saved to {checked_file_path}")

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")


start_file_index = 0
end_file_index = 22

# 각 파일에 대해 검색 실행
for file_index in range(start_file_index, end_file_index):
    process_csv_files(file_index)


