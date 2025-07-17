import traceback
import zipfile
import itertools
import string
import time
import zlib
import psutil
import io
from multiprocessing import Pool, Manager, Process

# 비밀번호 확인 함수
#암호를 푸는 코드를 unlock_zip() 이라는 이름으로 함수로 만든다.
def unlock_zip(args):
    #인수들 넣어버리기
    zip_bytes, password, found_flag = args
    #found_flag가 ture이면 비밀번호를 찾은 시점이므로 코드를 실행하지않고 나감
    if found_flag.value:
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            zf.open(zf.namelist()[0], pwd=password.encode('utf-8')).read(1)
            print(f"\n[성공] 비밀번호를 찾았습니다: {password}")
            #4. 암호를 푸는데 성공하면 암호는 password.txt로 저장한다.
            with open('chepter_2/question1/password.txt', 'w', encoding='utf-8') as f:
                f.write(f'password = {password}')
            return password
    except (RuntimeError, zipfile.BadZipFile, zlib.error):
        return False
    except Exception as e:
        print(traceback.format_exc())
        print(f"\n[오류] {e}")
        return False

# 문자 그룹 분할 (첫 글자 기준 3등분)
def split_first_characters():
    characters = string.ascii_lowercase + string.digits  # 36개
    group_size = len(characters) // 3
    return [
        characters[:group_size],                   # 0 ~ 11 / a ~ l
        characters[group_size:group_size*2],       # 12 ~ 23 / m ~ x
        characters[group_size*2:]                  # 24 ~ 끝 / y ~ 9
    ]

# 그룹별 브루트포스 실행 함수
#(실행함수, zip파일, 실행시작단어, 사용 코어 갯수, 시작시간, 시간??)
#1. emergency_storage_key.zip 의 암호를 풀 수 있는 코드를 작성한다. 단 암호는 특수 문자없이 숫자와 소문자 알파벳으로 구성된 6자리 문자로 되어 있다.
def brute_force_group(zip_bytes, first_chars, found_flag, start_time, time_str):
    #소문자 + 숫자
    rest_chars = string.ascii_lowercase + string.digits
    #6글자의 모든조합으로 비밀번호 생성
    combinations = itertools.product(first_chars, rest_chars, rest_chars, rest_chars, rest_chars, rest_chars)
    #''.join.('m', 'a', 'r', 's', '0', '6')
    tasks = ((zip_bytes, ''.join(pw), found_flag) for pw in combinations)

    #가지고 있는 코어를 전부사용하여 Pool 객체를 생성
    pool = Pool(psutil.cpu_count(logical=True))
    #pool마다 한번에 1000개의 작업
    for i, result in enumerate(pool.imap_unordered(unlock_zip, tasks, chunksize=1000)):
        #result가 none이면 작업을 하지 않는거 아닌가?
        #다른 워커에서 이미 찾은경우
        if found_flag.value:
            pool.terminate()
            break
        #현재 워커에서 찾은 경우
        if result:
            found_flag.value = True
            pool.terminate()
            break
        if i % 10000 == 0:
            #3. 암호를 푸는 과정을 출력하는데 시작 시간과 반복 회수 그리고 진행 시간등을 출력한다.
            print(f'\r[{first_chars[0]}~] 반복: {i} | 경과: {time.time() - start_time:.2f}초', end='')
    #더 이상 작업을 추가하지 않겠다
    pool.close()
    #워커들이 종료될 때까지 대기
    pool.join()

# 메인 실행부
if __name__ == '__main__':
    #password 저장 경로
    zip_file_path = 'chepter_2/question1/emergency_storage_key.zip'
    #메모리 낭비를 방지하기 위해 미리 메모리에 적재
    with open(zip_file_path, 'rb') as f:
        zip_bytes = f.read()

    manager = Manager()
    #프로세스에서 사용할 공유변수(b = boolean)
    found_flag = manager.Value('b', False)

    #시작시간 설정
    start_time = time.time()
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    # 암호를 좀 더 빠르게 풀 수 있는 알고리즘을 제시하고 코드로 구현한다.
    print(f"=== 3개 그룹 브루트포스 시작 ===")

    #글자갯수 / 3 으로 섹션 나누기
    groups = split_first_characters()
    #멀티프로세스 관리를 위한 리스트
    processes = []

    #섹션 갯수만큼 반복
    for group in groups:
        #(실행함수, zip파일, 실행시작단어, 사용 코어 갯수, 시작시간, 시간??)
        p = Process(target=brute_force_group, args=(zip_bytes, group, found_flag, start_time, time_str))
        p.start()
        processes.append(p)

    for p in processes:
        #워커들이 종료될 때까지 대기
        p.join()

    print(f"\n[종료] 총 소요 시간: {time.time() - start_time:.2f}초")


    #5. 암호를 풀 수 있는 전체 코드는 door_hacking.py로 저장한다.