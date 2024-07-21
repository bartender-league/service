from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Bar 클래스 정의
class Bar:
    def __init__(self, title, sido, sigungu, address, phone):
        self.title = title
        self.sido = sido
        self.sigungu = sigungu
        self.address = address
        self.phone = phone

    def __str__(self):
        return f"Title: {self.title}, Sido: {self.sido}, Sigungu: {self.sigungu}, Address: {self.address}, Phone: {self.phone}"


# 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL로 접속
url = 'https://www.google.com/maps/d/u/0/viewer?hl=ko&mid=1wJjYUyUGwC6e9CLTkGPkB9FNIfTkw1vD&ll=37.52621780000002%2C127.04111329999999&z=8'
driver.get(url)

# 페이지가 로딩될 때까지 기다림
time.sleep(3)  # 페이지 로딩 시간에 따라 조정 필요

bar_result = []
file_index = 14

# 시작할 요소의 인덱스를 지정
start_index = 279

def save_to_csv(data, index):
    df = pd.DataFrame(data)
    csv_file_path = f'bar_result_{index}.csv'
    df.to_csv(csv_file_path, index=False, header=False, encoding='utf-8-sig')
    print(f"Data saved to {csv_file_path}")

try:
    # 지정된 class를 가진 첫 번째 요소를 찾고 클릭
    first_element = driver.find_element(By.CLASS_NAME, 'HzV7m-pbTTYe-KoToPc-ornU0b')
    actions = ActionChains(driver)
    actions.move_to_element(first_element).click().perform()
    print("First element clicked")

    # 모든 HzV7m-pbTTYe-ibnC6b pbTTYe-ibnC6b-d6wfac 요소를 찾음
    elements = driver.find_elements(By.CLASS_NAME, 'HzV7m-pbTTYe-ibnC6b')

    # 지정된 인덱스에서부터 크롤링 시작
    for element in elements[start_index:]:
        try:
            time.sleep(1)
            # 각 요소를 클릭
            actions.move_to_element(element).click().perform()

            # 클릭 후 페이지 로드 대기
            time.sleep(3)  # 페이지 로딩 시간에 따라 조정 필요

            # 원하는 텍스트를 추출
            title_elements = driver.find_elements(By.CLASS_NAME, 'qqvbed-p83tee-V1ur5d')
            content_elements = driver.find_elements(By.CLASS_NAME, 'qqvbed-p83tee-lTBxed')

            # title_element 와 content_element 의 길이는 동일
            bar_data = {
                "title": None,
                "sido": None,
                "sigungu": None,
                "address": None,
                "phone": None
            }

            # Title과 Content의 텍스트 매칭
            for i, title_element in enumerate(title_elements):
                title_text = title_element.text
                if i < len(content_elements):
                    content_text = content_elements[i].text
                    if title_text == '바 이름':
                        bar_data["title"] = content_text
                    elif title_text == '시도':
                        bar_data["sido"] = content_text
                    elif title_text == '시군구':
                        bar_data["sigungu"] = content_text
                    elif title_text == '주소':
                        bar_data["address"] = content_text
                    elif title_text == '전화 번호':
                        bar_data["phone"] = content_text

            # Bar 객체 생성
            bar = Bar(
                bar_data["title"],
                bar_data["sido"],
                bar_data["sigungu"],
                bar_data["address"],
                bar_data["phone"]
            )

            print(f"bar info: {bar}")

            bar_result.append(bar)

            # 20개의 Bar 객체마다 CSV 파일로 저장
            if len(bar_result) >= 20:
                data = {
                    "Title": [bar.title for bar in bar_result],
                    "Sido": [bar.sido for bar in bar_result],
                    "Sigungu": [bar.sigungu for bar in bar_result],
                    "Address": [bar.address for bar in bar_result],
                    "Phone": [bar.phone for bar in bar_result]
                }
                save_to_csv(data, file_index)
                file_index += 1
                bar_result = []

            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'U26fgb'))
            )
            if bar_data["title"] is not None:
                actions.move_to_element(next_button).click().perform()
                print("Next button clicked")

        except Exception as e:
            print(f"An error occurred while processing an element: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

# 남아 있는 데이터를 저장
if bar_result:
    data = {
        "Title": [bar.title for bar in bar_result],
        "Sido": [bar.sido for bar in bar_result],
        "Sigungu": [bar.sigungu for bar in bar_result],
        "Address": [bar.address for bar in bar_result],
        "Phone": [bar.phone for bar in bar_result]
    }
    save_to_csv(data, file_index)

# 브라우저를 닫음
driver.quit()
