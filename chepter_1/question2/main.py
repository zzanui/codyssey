import json

timestamp = []
event = []
message = []

#1. 리스트 객채로 변환
#######################################################
"""
mission_computer_maint.log 파일을 읽어들여 첫째 줄의 컬럼행을 넘긴 후 
# ','를 기준으로 나누어 준 리스트를 imestamp, event, message를 기준으로 나누어 저장
"""
try:
  with open('chepter_1/question2/mission_computer_main.log', 'r', encoding='utf8' ) as file_data:
    next(file_data)  
    for line in file_data:
      parts = line.strip().split(',')
      if len(parts) >= 3:
        timestamp.append(parts[0])
        event.append(parts[1])
        message.append(parts[2])
except Exception as e:
  print(e)




#2. 전환된 리스트 객체를 화면에 출력      
######################################################
print("Timestamp:", timestamp)
print("Event:", event)
print("Message:", message)




#3. 리스트 객체를 시간의 역순으로 정렬(sort)
######################################################
#통합하여 정렬하기 위해 zip 사용
combined = list(zip(timestamp, event, message))
# 첫번째 요소(timestamp)를 기준으로 내림차순 정렬
combined.sort(key=lambda x: x[0], reverse=True)
#zip파일은 tuple을 사용하므로 분해 하여 리스트로 변경
timestamp, event, message = zip(*combined)
timestamp = list(timestamp)
event = list(event)
message = list(message)


#4. 리스트 객체를 사전(Dict) 객체로 전환
######################################################
#사전 객체로 변환하는데 하나하나 넣어주는 과정을 리스트의 길이만큼 반복한다.
loc_dic = {timestamp[i]: {'event': event[i], 'message': message[i]} for i in range(len(timestamp))}


#5. 사전 객체로 전환된 내용을 mission_computer_main.json 파일로 저장하는데 파일 포멧은 JSON(JavaScript Ontation)으로 저장한다.
######################################################
file_path = 'chepter_1/question2/mission_computer_main.json'
try:
  with open(file_path,'w', encoding='UTF-8') as f:
    json.dump(loc_dic, f)
except Exception as e:
  print(e)


#보너스: 사전 객체로 전환된 내용에서 특정 문자열 (예를 들어 Oxygen)을 입력하면 해당 내용을 출력하는 코드를 추가한다.
search_value = input("검색하실 문자열을 입력해주세요 예)Oxygen: ")
for timestamp, info in loc_dic.items():
    message = info.get("message", "")
    if search_value in message:
        print(f"{timestamp} => {message}")