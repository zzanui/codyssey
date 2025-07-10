import traceback#에러를 찾기 위해 추가로 사용
import zipfile
import itertools
import string
import time
import zlib 
# import psutil
from multiprocessing import Pool, Manager, current_process

#1. emergency_storage_key.zip 의 암호를 풀 수 있는 코드를 작성한다.
# 단 암호는 특수 문자없이 숫자와 소문자 알파벳으로 구성된 6자리 문자로 되어 있다.
#2. 암호를 푸는 코드를 unlock_zip() 이라는 이름으로 함수로 만든다.
def unlock_zip(args):
    zip_file_path, password, found_flag = args
    if found_flag.value:#found_flag가 ture이면 비밀번호를 찾은 시점이므로 코드를 실행하지않고 나감
        return None 
    try:
        with zipfile.ZipFile(zip_file_path) as zf:
            #비밀번호가 틀렸을 경우 에러가 발생하여 예외처리 넘어감
            # zf.extractall(path='chepter_2/question1' ,pwd=password.encode('utf-8')) #더미파일이 생성되어 I/O과정으로 인해 속도가 느려지므로 open으로 변경
            # 실제 파일 생성 없이 검증만 수행 | 첫번째 파일{zf.namelist()[0]}을 1바이트{read(1)}만 읽음
            zf.open(zf.namelist()[0], pwd=password.encode('utf-8')).read(1)#
            print(f"\n[성공] 비밀번호를 찾았습니다: {password}")
            with open('chepter_2/question1/password.txt', 'w', encoding='utf-8') as f:
                f.write(f'password = {password}')
            found_flag.value = True
            return password
    except (RuntimeError, zipfile.BadZipFile, zlib.error):
        return False
    except Exception as e:
        print(traceback.format_exc())
        print(f"\n[오류] {e}")
        return False


if __name__ == '__main__':
    # ZIP 파일 경로
    zip_file_path = 'chepter_2/question1/emergency_storage_key.zip'
    # zip_file_path = 'chepter_2/question1/test.zip' #테스트1
    # zip_file_path = 'chepter_2/question1/test2.zip' #테스트2

    # 브루트포스 공격 설정
    characters = string.ascii_lowercase + string.digits  # 소문자, 숫자
    password_length = 6
    
    #3. 암호를 푸는 과정을 출력하는데 시작 시간과 반복 회수 그리고 진행 시간등을 출력한다.
    start_time = time.time()#시작시간
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))#사람이 보기 좋은 형태

    print(f"=== 브루트포스 시작 ===")
    manager = Manager()
    found_flag = manager.Value('b', False) #실행결과 변수 프로세스간 공유
    pool = Pool(processes=2)  # CPU 코어 수만큼 병렬화
    # pool = Pool(psutil.cpu_count(logical=True))  # CPU 코어 수만큼 자동 병렬화


    # ZIP 파일 열기
    try:
        combinations = itertools.product(characters, repeat=password_length)#길이가 6자리인 모든 문자, 숫자의 조합 완성
        tasks = ((zip_file_path, ''.join(pw), found_flag) for pw in combinations) #필요한 인수를 튜플로 조합함

        #보너스1. 반순반복으로만 실행시 최대 21억회의 시도로 인해 시간이 너무 오래소요되어 멀티프로세싱 시도
        for i, result in enumerate(pool.imap_unordered(unlock_zip, tasks, chunksize=1000)):# imap_unordered() 순서없이 빠르게 반환되는데로 처리, chunksize 한번에 n개의 작업을 각 워커에 전달
            if result:#result에 password가 반환되었을 경우 password 출력
                print('\n[완료] 비밀번호:', result)
                pool.terminate()#비정상 종료
                break
            else:
                #3. 암호를 푸는 과정을 출력하는데 시작 시간과 반복 회수 그리고 진행 시간등을 출력한다.
                if(i % 10000 == 0):#출력하는데도 시간이 소요되므로 1만 단위로 현재상황을 출력한다. |  manager를 사용하여count를 프로세스 공유로 진행하려 하였지만 속도가 느려 enumerate()를 사용해 count를 대신함
                    print(f'\r시작시간 : {time_str} | 반복횟수 : {i} | 소요시간 {time.time() - start_time:.2f}초', end='')#해당 줄을 덮어씌우기 위해 \r(캐리지 리턴)사용
        pool.close()#정상종
        pool.join()

        print(f'총 소요 시간: {time.time() - start_time:.2f}초')

    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        print('\n[중단] 사용자에 의해 종료됨')
    except Exception as e:
        print(traceback.format_exc())
        print('[오류]', e)



#5. 암호를 풀 수 있는 전체 코드는 door_hacking.py로 저장


 


