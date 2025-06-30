import json

timestamp = []
event = []
message = []

#리스트 객채로 변환
#######################################################
#timestamp, event, message리스트에 나누어 저장
with open('chepter_1/question2/mission_computer_main.log', 'r', encoding='utf8' ) as file_data:
  next(file_data)  
  for line in file_data:
    parts = line.strip().split(',')
    if len(parts) >= 3:
      timestamp.append(parts[0])
      event.append(parts[1])
      message.append(parts[2])




# 전환된 리스트 객체를 화면에 출력      
######################################################
print("Timestamp:", timestamp)
print("Event:", event)
print("Message:", message)




# 리스트 객체를 시간의 역순으로 정렬(sort)
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


#리스트 객체를 사전(Dict) 객체로 전환
######################################################
#사전 객체로 변환하는데 하나하나 넣어주는 과정을 리스트의 길이만큼 반복한다.
loc_dic = {timestamp[i]: {'event': event[i], 'message': message[i]} for i in range(len(timestamp))}


#사전 객체로 전환된 내용을 mission_computer_main.json 파일로 저장하는데 파일 포멧은 JSON(JavaScript Ontation)으로 저장한다.
######################################################
file_path = 'mission_computer_main.json'
with open(file_path,'w', encoding='UTF-8') as f:
  json.dump(loc_dic, f)
