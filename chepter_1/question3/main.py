#에러 발생 위치를 찾기위해 사용
import traceback

Mars_Base_Inventory = []
try:
    with open("chepter_1/question3/Mars_Base_Inventory_List.csv", 'r') as mars:
        next(mars)#첫줄 스킵  
        for mar in mars:
            Mars_Base_Inventory.append(mar.strip().split(','))

except Exception as e:
    print(traceback.format_exc())
# print(Mars_Base_Inventory)


#인화성을 기준으로 인화성이 높은 순으로 정렬
Mars_Base_Inventory.sort(key=lambda x:x[4], reverse=True)


#인화성 지수가 0.7 이상인 리스트 별도로 관리 및 출력
filtered_Mars_Base_Inventory = [row for row in Mars_Base_Inventory if float(row[4]) >= 0.7]
# print(filtered_Mars_Base_Inventory)

#인화성 지수가 0.7 이상되는 목록을 CSV 포멧(Mars_Base_Inventory_danger.csv)으로 저장
try:
    with open('chepter_1/question3/Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8') as f:
        for line in filtered_Mars_Base_Inventory:
            f.write(','.join(line) + '\n')#단어마다 , 줄마다 줄넘김을 추가해 줌
except Exception as e:
    print(traceback.format_exc())


#보너스1 : 인화성 순서로 정렬된 배열의 내용을 이진 파일형태로 저장한다. 파일이름은 Mars_Base_Inventory_List.bin
try:
    with open("chepter_1/question3/Mars_Base_Inventory_List.bin", 'wb') as f:
        for line in Mars_Base_Inventory:
            bw_line = (','.join(line) + '\n').encode('utf-8')
            f.write(bw_line)
except Exception as e:
    print(traceback.format_exc())

#보너스2 : 저장된 Mars_Base_Inventory_List.bin 의 내용을 다시 읽어 들여서 화면에 내용을 출력.
try:
    with open("chepter_1/question3/Mars_Base_Inventory_List.bin", 'r') as f:
        for line in f:
            print(line)
except Exception as e:
    print(traceback.format_exc())

"""
#보너스3 : 텍스트 파일과 이진 파일 형태의 차이점과 장단점
->  텍스트파일은 사람이 볼 수 있는 형태로 저장되며 이진파일은 그와 반대로 사람이 읽지 않고 컴퓨터가 읽는것을 상정하고 저장하는 파일이다.
    사람이 읽을 수 있는 형태의 파일은 컴퓨터가 처리하기에 변환과정을 거쳐야 하기 때문에 이진파일이 텍스트 파일보다 용량이 적다는 특징을 가지고 있다.
    또한 사용처 또한 다른데 문서같은 경우는 사람이 읽을 수 있어야 하기 때문에 주로 텍스트 파일로 사용하지만 영상, 사진, 음성파일의 경우 그 자체로는 사람이 읽고 사용하기 어렵기 때문에
    주로 이진파일을 하용하여 관리한다.
"""




