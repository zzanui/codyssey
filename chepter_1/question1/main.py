try:
    with open('chepter_1/mission_computer_main.log', 'r') as file_data:
      for data in file_data:
        print(data.strip())
except Exception as e:
    print(e)


        


