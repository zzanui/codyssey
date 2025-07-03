#1. numpy를 사용하기 위해서 import를 한다.
#pip install numpy
import numpy as np


#2. 파일들을 모두 numpy를 사용해서 읽어들여서 각각 arr1, arr2, arr3 과 같이 ndarray 타입으로 가져온다.
arr1 = np.genfromtxt(
    'chepter_1/question5/mars_base_main_parts-001.csv', 
    delimiter=',',          #csv는 ,을 기준으로 나누어져 있기 때문
    dtype=None,             #데이터 타입은 자동으로 지정
    encoding='utf-8-sig',   #BOM파일로 인한 에러를 방지하기위해 사용
    names=True              #열이름으로 데이터에 접근이 가능하게 함
    )
arr2 = np.genfromtxt(
    'chepter_1/question5/mars_base_main_parts-002.csv', 
    delimiter=',',          #csv는 ,을 기준으로 나누어져 있기 때문
    dtype=None,             #데이터 타입은 자동으로 지정
    encoding='utf-8-sig',   #BOM파일로 인한 에러를 방지하기위해 사용
    names=True              #열이름으로 데이터에 접근이 가능하게 함
    )
arr3 = np.genfromtxt(
    'chepter_1/question5/mars_base_main_parts-003.csv', 
    delimiter=',',          #csv는 ,을 기준으로 나누어져 있기 때문
    dtype=None,             #데이터 타입은 자동으로 지정
    encoding='utf-8-sig',   #BOM파일로 인한 에러를 방지하기위해 사용
    names=True              #열이름으로 데이터에 접근이 가능하게 함
    )

#3. 3개의 배열을 하나로 합치고(merge) 이름을 parts 라는 ndarray 를 생성
parts = np.concatenate((arr1, np.concatenate((arr2,arr3))))

#4. parts를 이용해서 각 항목의 평균값을 구한다.
part_avg = []
parts_dic = dict()
for part, strength in parts:
    part = str(part)
    strength = int(strength)
    if part in parts_dic:
        parts_dic[part]['sum'] += strength
        parts_dic[part]['count'] += 1
    else:
        parts_dic[part] = {'sum': strength, 'count': 1}
part_avg = np.array(
    [
        [part, round(values['sum'] / values['count'], 3)] for part, values in parts_dic.items()
    ],
    dtype=object  # 문자열 + 숫자 혼합이므로 object
)

#5. 평균값이 50 보다 작은 값을 뽑아내서 parts_to_work_on.csv 라는 파일로 별도로 저장한다.
filtered = part_avg[np.array([float(x[1]) < 50 for x in part_avg])]
np.savetxt('chepter_1/question5/parts_to_work_on.csv', filtered, delimiter=',', fmt='%s,%.3f')


#6. 작성된 코드는 design_dome.py 라는 이름으로 저장

#보너스1. parts_to_work_on.csv를 읽어서 parts2라는 ndarray에 저장한다.
parts2 = np.genfromtxt(
    'chepter_1/question5/parts_to_work_on.csv', 
    delimiter=',',          #csv는 ,을 기준으로 나누어져 있기 때문
    dtype=None,             #데이터 타입은 자동으로 지정
    encoding='utf-8-sig',   #BOM파일로 인한 에러를 방지하기위해 사용
    names=True              #열이름으로 데이터에 접근이 가능하게 함
    )

#보너스2. parts2의 내용을 기반으로 전치행렬을 구하고 그 내용을 parts3에 저장하고 출력한다.
#넘파이 배열의 T 속성을 사용하면 배열의 전치행렬을 빠르게 구할 수 있습니다
#vstack = vertical stack = 위에서 아래로 행 방향으로 붙이기/ 문자가 포함되어있는 numpy의 구조화배열은 전치행렬을 구할 수 없으므로 일반배열로 변경한 후 전치행렬을 구한다.
parts_array = np.vstack([parts2[name] for name in parts2.dtype.names])
part3 = parts_array.T
print(part3)