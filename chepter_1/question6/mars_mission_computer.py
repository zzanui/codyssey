import random
from datetime import datetime
#1 더미 센서에 해당하는 클래스를 생성한다. 클래스의 이름은 DummySensor로 정의한다.
class DummySensor:
    
    # 2.DummySensor의 멤버로 env_values라는 사전 객체를 추가한다. 사전 객체에는 다음과 같은 항목들이 추가 되어 있어야 한다.
    # 화성 기지 내부 온도 (mars_base_internal_temperature)
    # 화성 기지 외부 온도 (mars_base_external_temperature)
    # 화성 기지 내부 습도 (mars_base_internal_humidity)
    # 회성 기지 외부 광량 (mars_base_external_illuminance)
    # 화성 기지 내부 이산화탄소 농도 (mars_base_internal_co2)
    # 화성 기지 내부 산소 농도 (mars_base_internal_oxygen)
    
    env_values = {
        "mars_base_internal_temperature": 0.0,
        "mars_base_external_temperature": 0.0,
        "mars_base_internal_humidity":0.0,
        "mars_base_external_illuminance":0.0,
        "mars_base_internal_co2":0.0,
        "mars_base_internal_oxygen":0.0,
    }

    #3 DummySensor는 테스트를 위한 객체이므로 데이터를 램덤으로 생성한다.
    def __init__(self):
        env_values = self.env_values
        for key, value in env_values.items():
            env_values[key] = random.random()#언제 초기화 하라는 명시가 안되어 있어 그냥 생성자에 집어넣음


    #4.DummySensor 클래스에 set_env() 메소드를 추가한다. set_env() 메소드는 random으로 주어진 범위 안의 값을 생성해서 env_values 항목에 채워주는 역할을 한다. 
    # 각 항목의 값의 범위는 다음과 같다.
    # 화성 기지 내부 온도 (18~30도)
    # 화성 기지 외부 온도 (0~21도)
    # 화성 기지 내부 습도 (50~60%)
    # 화성 기지 외부 광량 (500~715 W/m2)
    # 화성 기지 내부 이산화탄소 농도 (0.02~0.1%)
    # 화성 기지 내부 산소 농도 (4%~7%)
    def set_env(self):
        env_values = self.env_values
        set_values = [#랜덤 범위들
                        [18.0,30.0],
                        [0.0,20.0],
                        [50.0,60.0],
                        [500.0,715.0],
                        [0.02,0.1],
                        [4.0,7.0]
                    ]
        for key, values in zip(env_values.keys(), set_values): #키값과 랜덤에 필요한 범위들을 반복문으로 제어
            env_values[key] = random.uniform(values[0],values[1])

    
    def get_env(self):
        env_values = self.env_values

        #보너스1. 파일에 log를 남기는 부분을 get_env()에 추가 한다.
        try:
## datetime.now()는 위의 time과 같은 기능.
            tm = datetime.now().strftime('%Y.%m.%d-%H:%M:%S') # 년.월.일 - 시간
            with open('chepter_1/question6/DummySensor.log', 'w', encoding='utf-8') as f:
                for key, value in env_values.items():
                    f.write(f"{tm} : {key} : {value}\n")
        except Exception as e:
            print(e)



        #5. DummySensor 클래스는 get_env() 메소드를 추가하는데 get_env() 메소드는 env_values를 return 한다.
        return env_values



#6. ds라는 이름으로 인스턴스(Instance)로 만든다.
ds = DummySensor()

#7. 인스턴스화 한 DummySensor 클래스에서 set_env()와 get_env()를 차례로 호출해서 값을 확인한다.
ds.set_env()
print(ds.get_env())

#8. 전체 코드를 mars_mission_computer.py 파일로 저장한다.