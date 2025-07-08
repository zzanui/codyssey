#암호를 푸는 코드를 unlock_zip() 이라는 이름으로 함수로 만든다.
def unlock_zip():
    while(True):
        pass



# emergency_storage_key.zip 의 암호를 풀 수 있는 코드를 작성한다.
# 단 암호는 특수 문자없이 숫자와 소문자 알파벳으로 구성된 6자리 문자로 되어 있다.
# 암호를 푸는 코드를 unlock_zip() 이라는 이름으로 함수로 만든다.
# 암호를 푸는 과정을 출력하는데 시작 시간과 반복 회수 그리고 진행 시간등을 출력한다.
# 암호를 푸는데 성공하면 암호는 password.txt로 저장한다.
# 암호를 풀 수 있는 전체 코드는 door_hacking.py로 저장한다.

if __name__ == '__main__':
    number = [i for i in range(10)]
    aList = [chr(i) for i in range(ord('a'),ord('z')+1)]
    blist = [chr(i) for i in range(ord('A'),ord('Z')+1)]