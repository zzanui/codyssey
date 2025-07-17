#에러를 찾기 위해 추가로 사용
import traceback
import zipfile
import itertools
import string
import time
import zlib 
import psutil
import io

from multiprocessing import Pool, Manager


def init_worker(zip_path):
    global zf
    with open(zip_path, 'rb') as f:
        # zf를 한번만 호출해 IO 병목을 줄입니다.
        # zf = zipfile.ZipFile(zip_path)
        # 아래 코드는 그것을 메모리에 올립니다. 
        # 읽고 쓰려는 파일이 크거나, 멀티프로세스 환경에서 성능향상을 기대할 수 있습니다.
        # 다만 멀티 프로세스 환경에선 객체 공유가 불가능해 프로세스 갯수만큼 객체를 만들어내므로
        # 메모리 확보에 신경써야합니다.
        zf = zipfile.ZipFile(io.BytesIO(f.read()))
    

# 1.emergency_storage_key.zip 의 암호를 풀 수 있는 코드를 작성한다.
# 단 암호는 특수 문자없이 숫자와 소문자 알파벳으로 구성된 6자리 문자로 되어 있다.
# 2.암호를 푸는 코드를 unlock_zip() 이라는 이름으로 함수로 만든다.
def unlock_zip(args):
    password, found_flag = args
    # found_flag가 ture이면 비밀번호를 찾은 시점이므로 코드를 실행하지않고 나감
    if found_flag.value:
        return None
    
    try:
        # with open 구문 대신 global zf를 사용
        # 비밀번호가 틀렸을 경우 에러가 발생하여 예외처리 넘어감
        # zf.extractall(path='chepter_2/question1' ,pwd=password.encode('utf-8')) 
        # #더미파일이 생성되어 I/O과정으로 인해 속도가 느려지므로 open으로 변경
        # 실제 파일 생성 없이 검증만 수행 | 첫번째 파일{zf.namelist()[0]}을 1바이트{read(1)}만 읽음
        zf.open(zf.namelist()[0], pwd=password.encode('utf-8')).read(1)
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

def split_characters():
    # 브루트포스 공격 설정 : 알파벳 소문자, 숫자
    characters = string.ascii_lowercase + string.digits
    password_length = 6
    combinations = itertools.product(characters, repeat=password_length)
    return combinations



if __name__ == '__main__':
    # ZIP 파일 경로
    zip_file_path = 'chapter_2/prob1/emergency_storage_key.zip'
    # zip_file_path = 'chepter_2/question1/test.zip' #테스트1
    # zip_file_path = 'chepter_2/question1/test2.zip' #테스트2

    
    #3. 암호를 푸는 과정을 출력하는데 시작 시간과 반복 회수 그리고 진행 시간등을 출력한다.
    # 시작시간
    start_time = time.time()
    # 사람이 보기 좋은 형태
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))

    print(f"=== 브루트포스 시작 ===")
    manager = Manager()
    found_flag = manager.Value('b', False) #실행결과 변수 프로세스간 공유
    # pool = Pool(processes=2)  # CPU 코어 수만큼 병렬화
    # CPU 코어 수만큼 자동 병렬화
    pool = Pool(
        psutil.cpu_count(logical=True),
        initializer=init_worker,
        initargs=(zip_file_path,)
        )  

    # ZIP 파일 열기
    try:
        # 길이가 6자리인 모든 문자, 숫자의 조합 완성
        combinations = split_characters()
        print(combinations)

        # 필요한 인수를 튜플로 조합함
        tasks = ((''.join(pw), found_flag) for pw in combinations) 

        # 보너스1. 반순반복으로만 실행시 최대 21억회의 시도로 인해 시간이 너무 오래소요되어 멀티프로세싱 시도
        # imap_unordered() 순서없이 빠르게 반환되는데로 처리, chunksize 한번에 n개의 작업을 각 워커에 전달
        imap_iterator = pool.imap_unordered(unlock_zip, tasks, chunksize=1000)
        # for i, result in enumerate(imap_iterator):
        #     # result에 password가 반환되었을 경우 password 출력
        #     if result:
        #         print('\n[완료] 비밀번호:', result)

        #         # 비정상 종료
        #         pool.terminate()
        #         break

        #     else:
        #         # 3.암호를 푸는 과정을 출력하는데 시작 시간과 반복 회수 그리고 진행 시간등을 출력한다.
        #         # 출력하는데도 시간이 소요되므로 10만 단위로 현재상황을 출력한다.
        #         # manager를 사용하여 count를 프로세스 공유로 진행하려 하였지만 속도가 느려 enumerate()를 사용해 count를 대신함
        #         if(i % 100_000 == 0):
        #             # 해당 줄을 덮어씌우기 위해 \r(캐리지 리턴)사용
        #             print(f'\r시작시간 : {time_str} | '
        #                   f'반복횟수 : {i} | '
        #                   f'소요시간 {time.time() - start_time:.2f}초', 
        #                   end='')
        # # 정상종료
        # pool.close()
        # pool.join()

        # print(f'총 소요 시간: {time.time() - start_time:.2f}초')

    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        print('\n[중단] 사용자에 의해 종료됨')

    except Exception as e:
        print(traceback.format_exc())
        print('[오류]', e)

#5. 암호를 풀 수 있는 전체 코드는 door_hacking.py로 저장


 


