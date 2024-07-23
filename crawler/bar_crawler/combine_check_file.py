import pandas as pd
import os

# Bar 클래스 정의
class Bar:
    def __init__(self, title, sido, sigungu, address, phone, isChecked):
        self.title = title
        self.sido = sido
        self.sigungu = sigungu
        self.address = address
        self.phone = phone
        self.isChecked = isChecked

    def __str__(self):
        return f"Title: {self.title}, Sido: {self.sido}, Sigungu: {self.sigungu}, Address: {self.address}, Phone: {self.phone}, Checked: {self.isChecked}"

# _checked 파일들을 하나로 합치는 함수
def combine_checked_files(file_count):
    combined_df = pd.DataFrame(columns=["Title", "Sido", "Sigungu", "Address", "Phone", "isChecked"])

    for index in range(file_count):
        checked_file_path = f'bar_result_{index}_checked.csv'
        if os.path.exists(checked_file_path):
            df = pd.read_csv(checked_file_path, header=None, names=["Title", "Sido", "Sigungu", "Address", "Phone", "isChecked"])
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    combined_file_path = 'combined_checked.csv'
    combined_df.to_csv(combined_file_path, index=False, header=False, encoding='utf-8-sig')
    print(f"Combined results saved to {combined_file_path}")

    return combined_df

# True와 False로 분리하여 저장하는 함수
def split_checked_file(df):
    true_df = df[df['isChecked'] == True]
    false_df = df[df['isChecked'] == False]

    true_file_path = 'checked_true.csv'
    false_file_path = 'checked_false.csv'

    true_df.to_csv(true_file_path, index=False, header=False, encoding='utf-8-sig')
    false_df.to_csv(false_file_path, index=False, header=False, encoding='utf-8-sig')

    print(f"True results saved to {true_file_path}")
    print(f"False results saved to {false_file_path}")

# 파일 합치기 및 분리 실행
file_count = 22  # _checked 파일의 개수 (이 값을 실제 파일 개수로 변경하세요)
combined_df = combine_checked_files(file_count)
split_checked_file(combined_df)
