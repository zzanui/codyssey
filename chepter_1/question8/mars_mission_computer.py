#시스템 정보 및 프로세스 정보를 손쉽게 가져올 수 있게 해주는 파이썬 라이브러리
import psutil,platform
#다른폴더에 존재하는 DummySensor 클래스를 가져오기 위해 sys.path에 경로를 추가합니다.('/workspaces/codyssey/chepter_1')
import sys, os, json
#해당코드를 사용했을 경우 경로가 추가되는 구조를 물어보는게 좋을 것 같다.
#/workspaces/codyssey/chepter_1
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from question7.mars_mission_computer import MissionComputer 

# MissionComputer.get_mission_computer_info = get_mission_computer_info
# MissionComputer.get_mission_computer_load = get_mission_computer_load
#처음에는 기존 클래스를 그대로 사용하는 방법을 사용하였지만 관리 측면에서 아무리 봐도 아닌 것 같다는 생각이 들어 클래스를 계승함
class MissionComputer_2(MissionComputer):
    #1. 문제 7에서 완성한 MissionComputer 클래스에 get_mission_computer_info()를 추가한다.
    def get_mission_computer_info(self):
        mission_computer_info = {
            "운영체제": platform.system(),# 운영체계
            "운영체제 버전": platform.version(),# 운영체계 버전
            "CPU 타입": platform.processor(),# CPU의 타입
            "CPU코어 수": psutil.cpu_count(logical=True),# CPU의 코어 수
            "메모리의 크기": f'{psutil.virtual_memory().total / (1024 ** 3):.2f} GB',# 메모리의 크기(총 크기를 bytes -> gb로 표시함)
        }
        #2. get_mission_computer_info()에 가져온 시스템 정보를 JSON 형식으로 출력하는 코드를 포함한다.
        #(출력할 dic, 한글이 깨지지않게, 들여쓰기)
        return (json.dumps(mission_computer_info, ensure_ascii=False, indent=4))

    #3. 미션 컴퓨터의 부하를 가져오는 코드를 get_mission_computer_load() 메소드로 만들고 MissionComputer 클래스에 추가
    def get_mission_computer_load(self):
        #4. get_mission_computer_load() 메소드의 경우 다음과 같은 정보들을 가져 올 수 있게한다.
        mission_computer_load = {
            'CPU 실시간 사용량': psutil.cpu_percent(interval=1), # 1초간의 CPU 실시간 사용량
            '메모리 실시간 사용량' :psutil.virtual_memory().percent,# 메모리 실시간 사용량(률)
        }
        #5. get_mission_computer_load()에 해당 결과를 JSON 형식으로 출력하는 코드를 추가한다.
        #(출력할 dic, 한글이 깨지지않게, 들여쓰기)
        return (json.dumps(mission_computer_load, ensure_ascii=False, indent=4))
            



if __name__ == "__main__":
    #7. MissionComputer 클래스를 runComputer 라는 이름으로 인스턴스화 한다.
    runComputer = MissionComputer_2()

    #6. get_mission_computer_info(), get_mission_computer_load()를 호출해서 출력이 잘되는지 확인한다.
    #8. runComputer 인스턴스의 get_mission_computer_info(), get_mission_computer_load() 메소드를 호출해서 시스템 정보에 대한 값을 출력 할 수 있도록 한다.
    print(runComputer.get_mission_computer_info())
    print(runComputer.get_mission_computer_load())

    # 9. 최종적으로 결과를 mars_mission_computer.py 에 저장한다.
 
 #보너스
 #무슨 말인지 이해가 되지 않는다



