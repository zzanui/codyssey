import traceback

#1. 지름(diameter)을 입력받아 전체 면적을 구하는 식을 세워보고 sphere_area()라는 함수로 제작
#2. 함수에 재질을 material, 두께는 thickness라는 파라메터로 입력가능하게 제작
def sphere_area(diameter, material, thickness):
    #제질의 무게
    density = {
        '유리' :  2.4,
        '알루미늄' : 2.7,
        '탄소강' : 7.85,
    }
    #전역변수 설정
    global area, weight 

    #공식의 경우 chat gpt를 사용해서 알아보았습니다.
    #면적을 구하는 공식3⋅π⋅반지름 2
    radius = diameter / 2
    #6. 소수점 이하 세 자리까지만 출력해서 결과가 지나치게 길어지는 것을 피한다.
    area = round(3 * 3.14 * (radius ** 2), 3)

    volume = area * thickness  # cm³
    mass_earth = volume * density[material]  # g
    #5. 화성의 중력을 반영해서 다시 수식에 반영 
    #6. 소수점 이하 세 자리까지만 출력해서 결과가 지나치게 길어지는 것을 피한다.
    weight = round((mass_earth * 0.38) / 1000, 3)



while(True):
    #3. 함수의 입력되는 재질과 지름은 input()을 사용해서 사용자로 부터 입력을 받아야 한다.
    try:
        # #4. sphere_area() 함수에서 파라메터 중 material은 기본값이 유리 그리고 두께는 기본값이 1cm가 되게 한다.
        material = input('"유리", "알루미늄", "탄소강" 중 재질을 입력하세요(기본값 : 유리) / "종료" 입력시 종료됩니다.: ') or "유리"

        #종료가 값으로 들어왔을 경우 해당 반복을 종료
        if material == "종료":
            break
        elif(not(material in ["유리", "알루미늄", "탄소강"])):
            print('정상적이지 않는 값이 입력 되었습니다 기본값으로 진행됩니다.')
            material = '유리'

        thickness = (input('두께를 입력하세요 단위 = cm (기본값 : 1cm) : ') or 1)
        try:
            thickness = float(thickness)
        #보너스 : 파라메터에 숫자가 아닌 문자가 들어갔을 때 오류가 발생하지 않도록 처리
        except ValueError:
            print('정상적이지 않는 값이 입력 되었습니다 기본값으로 진행됩니다.')
            thickness = 1.0
        diameter = 1000 #cm


        #1차 코드
        # user_input = input('재질과 두께를 입력하세요(기본값: 유리, 1cm) / 한가지만 입력 시 종료 됩니다.')
        # diameter = 1000 #cm

        # #4. sphere_area() 함수에서 파라메터 중 material은 기본값이 유리 그리고 두께는 기본값이 1cm가 되게 한다.
        # #입력값이 없을경우를 산정하여 값이 없을 경우 기본값 지정
        # if not user_input:
        #     material = '유리'
        #     thickness = 1
        
            
        # else:
        #     parts = user_input.split()
            
        #     if len(parts) == 2:
        #         #보너스 : 파라메터에 숫자가 아닌 문자가 들어갔을 때 오류가 발생하지 않도록 처리
        #         if(isinstance(user_input[1],str)):
        #             print('두께에 문자가 입력되어 기본값으로 지정합니다.')
        #             material, thickness = parts[0], float(1)
        #         else:
        #             material, thickness = parts[0], float(parts[1])
        #     elif(len(parts) == 1):#종료
        #         print('종료합니다.')
        #         break

        sphere_area(diameter=diameter, material=material, thickness=thickness)
    except Exception as e:
        print(traceback.format_exc())

    #7. 계산 결과가 나오면 전역변수에 계산한 값을 저장하고 다음과 같은 형태로 출력
    print(f'재질 =⇒ {material}, 지름 =⇒ {diameter}, 두께 =⇒ {thickness}, 면적 =⇒ {area} cm, 무게 =⇒ {weight} kg')
        