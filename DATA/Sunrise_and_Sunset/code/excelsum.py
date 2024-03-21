import pandas as pd
import os

# 기본 파일 이름과 확장자 정의
base_filename = 'excel'
extension = '.xlsx'
combined_data = None

# 첫 번째 파일 불러오기
try:
    combined_data = pd.read_excel(f'{base_filename}{extension}')
except FileNotFoundError:
    print(f'File not found: {base_filename}{extension}')

# 뒤이은 파일들 불러오기 (1부터 시작)
i = 1
while True:
    try:
        next_filename = f'{base_filename} ({i}){extension}'
        next_data = pd.read_excel(next_filename)
        combined_data = pd.concat([combined_data, next_data], ignore_index=True)
        i += 1
    except FileNotFoundError:
        print(f'No more files found. Last file checked: {next_filename}')
        break

# 결합된 데이터를 새 파일에 저장
if combined_data is not None:
    output_filename = 'combined_excel.xlsx'
    combined_data.to_excel(output_filename, index=False)
    print(f'Combined data saved to {output_filename}')
else:
    print('No data to save.')