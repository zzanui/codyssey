import zipfile
import string
from multiprocessing import Pool, cpu_count
import time

# 설정
zip_path = "emergency_storage_key.zip"  # 같은 디렉토리에 파일 위치
charset = string.ascii_lowercase + string.digits
password_length = 6

def try_password(index):
    base = len(charset)
    password = []
    for _ in range(password_length):
        password.append(charset[index % base])
        index //= base
    pwd_str = ''.join(reversed(password)).rjust(password_length, charset[0])
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(pwd=pwd_str.encode('utf-8'))
            print(f"[✓] Password Found: {pwd_str}")
            return pwd_str
    except:
        return None

def run_bruteforce(start, end):
    start_time = time.time()
    with Pool(processes=cpu_count()) as pool:
        for result in pool.imap_unordered(try_password, range(start, end), chunksize=1000):
            if result:
                pool.terminate()
                elapsed = time.time() - start_time
                print(f"Time Taken: {elapsed:.2f} seconds")
                return result
    print("Password not found in given range.")
    return None

if __name__ == "__main__":
    # 전체 범위: 36^6 = 2176782336
    found = run_bruteforce(0, 1000000)  # 먼저 테스트로 100만개