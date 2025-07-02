#1. numpy를 사용하기 위해서 import를 한다.
#pip install numpy
import numpy as np


#2. 파일들을 모두 numpy를 사용해서 읽어들여서 각각 arr1, arr2, arr3 과 같이 ndarray 타입으로 가져온다.
#csv는 ,을 기준으로 나누어져 있기 때문에 delimiter=','를 설정
arr1 = np.loadtxt('chepter_1/question5/mars_base_main_parts-001.csv', delimiter=',')

print(arr1)