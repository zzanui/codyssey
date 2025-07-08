import time 
import threading
from multiprocessing import Process
import sys, os
#해당코드를 사용했을 경우 경로가 추가되는 구조를 물어보는게 좋을 것 같다.
#/workspaces/codyssey/chepter_1
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from question8.mars_mission_computer import MissionComputer_2

#1. MissionComputer 클래스에 있는 get_mission_computer_info(), get_mission_computer_load() 
# 두 개의 메소드를 time 라이브러리를 사용해서 
# 각각 20초에 한번씩 결과를 출력 할 수 있게 수정한다.
class MissionComputer_3(MissionComputer_2):
    def get_mission_computer_info(self):
        while(True):
            print(super().get_mission_computer_info())
            time.sleep(20)

    def get_mission_computer_load(self):
        while(True):
            print(super().get_mission_computer_load())
            time.sleep(20)




if __name__ == "__main__":
    #2. MissionComputer 클래스를 runComputer 라는 이름으로 인스턴스화 한다.
    runComputer = MissionComputer_3()

    #3. runComputer 인스턴스의 get_mission_computer_info(), get_mission_computer_load(), get_sensor_data() 메소드를 각각 멀티 쓰레드로 실행 시킨다.
    t1 = threading.Thread(target=runComputer.get_mission_computer_info)
    t2 = threading.Thread(target=runComputer.get_mission_computer_load)
    t3 = threading.Thread(target=runComputer.get_sensor_data)
    t1.start()
    t2.start()
    t3.start()


    #4. 다시 코드를 수정해서 MissionComputer 클래스를 
    # runComputer1, runComputer2, runComputer3 이렇게 3개의 인스턴스를 만든다.
    runComputer1 = MissionComputer_3()
    runComputer2 = MissionComputer_3()
    runComputer3 = MissionComputer_3()

    #5. 3개의 인스턴스를 멀티 프로세스로 실행시켜서 각각 
    # get_mission_computer_info(), get_mission_computer_load(), get_sensor_data()를 실행시키고 출력을 확인한다.
    p1 = Process(target=runComputer1.get_mission_computer_info)
    p2 = Process(target=runComputer2.get_mission_computer_load)
    p3 = Process(target=runComputer3.get_sensor_data)
    p1.start()
    p2.start()
    p3.start()

# 메인 스레드가 두 작업을 기다림
    try:
        t1.join()
        t2.join()
        t3.join()
        p1.join()
        p2.join()
        p3.join()
    #보너스:반복적으로 출력되는 중간에 특정한 키를 입력 받아 출력을 멈출 수 있게 코드를 작성한다.
    except KeyboardInterrupt:
        t1.terminate()
        t2.terminate()
        t3.terminate()
        p1.terminate()
        p2.terminate()
        p3.terminate()
        print("사용자 종료 요청으로 프로그램을 종료합니다.")
    #6. 최종적으로 결과를 mars_mission_computer.py 에 저장한다.
