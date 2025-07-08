#다른폴더에 존재하는 DummySensor 클래스를 가져오기 위해 sys.path에 경로를 추가합니다.('/workspaces/codyssey/chepter_1')
import sys, os, time, json
#해당코드를 사용했을 경우 경로가 추가되는 구조를 물어보는게 좋을 것 같다.
#/workspaces/codyssey/chepter_1
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from question6.mars_mission_computer import DummySensor

#1. 미션 컴퓨터에 해당하는 클래스를 생성한다. 클래스의 이름은 MissionComputer로 정의한다.
class MissionComputer:
    #2 미션 컴퓨터에는 화성 기지의 환경에 대한 값을 저장할 수 있는 사전(Dict) 객체가 env_values라는 속성으로 포함되어야 한다.
    env_values={
        
    }

    #3 .env_values라는 속성 안에는 다음과 같은 내용들이 구현 되어야 한다.
        # 화성 기지 내부 온도 (mars_base_internal_temperature)
        # 화성 기지 외부 온도 (mars_base_external_temperature)
        # 화성 기지 내부 습도 (mars_base_internal_humidity)
        # 회성 기지 외부 광량 (mars_base_external_illuminance)
        # 화성 기지 내부 이산화탄소 농도 (mars_base_internal_co2)
        # 화성 기지 내부 산소 농도 (mars_base_internal_oxygen)
    def __init__(self):
        env_values = self.env_values
        env_values={
            'mars_base_internal_temperature' : 0.0,
            'mars_base_external_temperature' : 0.0,
            'mars_base_internal_humidity' : 0.0,
            'mars_base_external_illuminance' : 0.0,
            'mars_base_internal_co2' : 0.0,
            'mars_base_internal_oxygen' : 0.0
        }

    #4. 문제 3에서 제작한 DummySensor 클래스를 ds라는 이름으로 인스턴스화 시킨다.(문제 3은 오타로 문제 6이 맞는 것 같다.)
    ds = DummySensor()

    #5. MissionComputer에 get_sensor_data() 메소드를 추가한다.
    def get_sensor_data(self):
        ds = self.ds
        env_values = self.env_values

        # 5분(300초) 동안의 값을 저장할 리스트
        history = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': []
        }
        count = 0


        #6. get_sensor_data() 메소드에 다음과 같은 세 가지 기능을 추가한다.
        try:
            while(True):
                # 센서의 값을 가져와서 env_values에 담는다.
                ds.set_env()
                for key, value in ds.get_env().items():
                    env_values[key] = value
                    history[key].append(value)
                # env_values의 값을 출력한다. 이때 환경 정보의 값은 json 형태로 화면에 출력한다.
                json_env_values = json.dumps(env_values)
                print(json_env_values)
                print("\n종료하려면 Ctrl+C")
                # 위의 두 가지 동작을 5초에 한번씩 반복한다.
                time.sleep(5)
                count += 1

                #보너스2. 5분에 한번씩 각 환경값에 대한 5분 평균 값을 별도로 출력한다.
                # 5분(300초)마다 평균 출력 (5초 * 60 = 300초)
                # if count == 60:
                #테스트를 위해 1분(60초)로 조정(5초 * 12 = 60초)
                if count == 12:
                    avg_values = {}
                    for key, values in history.items():
                        avg_values[key] = sum(values) / len(values) if values else 0.0
                    #count // 12 == n분
                    print(f"\n{count//12}분 평균값:", json.dumps(avg_values,ensure_ascii=False, indent=4))
                    # 리스트 초기화
                    for key in history:
                        history[key] = []
                    count = 0

        #보너스1. 특정 키를 입력할 경우 반복적으로 출력되던 화성 기지의 환경에 대한 출력을 멈추고 ‘Sytem stoped….’ 를 출력 할 수 있어야 한다.
        except KeyboardInterrupt:#컨트롤 + c 입력시
            print("\nSytem stoped….")



        



if __name__ == "__main__":
    #7. MissionComputer 클래스를 RunComputer 라는 이름으로 인스턴스화 한다.
    RunComputer  = MissionComputer()

    #8. RunComputer 인스턴스의 get_sensor_data() 메소드를 호출해서 지속적으로 환경에 대한 값을 출력 할 수 있도록 한다.
    RunComputer.get_sensor_data()

    #9. 전체 코드를 mars_mission_computer.py 파일로 저장한다.

