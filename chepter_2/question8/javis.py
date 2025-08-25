


import os
import speech_recognition as sr
import csv
import wave

#1. 문제 7에서 녹음된 음성파일들의 목록을 불러온다.
def save_directory_listing(directory_path):
    return [f for f in os.listdir(directory_path) if f.endswith(".wav")]#wav파일만 불러옴

#2. 음성파일을 가져오면 음성 파일에서 텍스트를 추출하는 STT(Speech to Text) 기능을 구현하고 음성이 텍스트로 잘 인식되는지 확인 한다.
def stt(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)  # 전체 오디오 로드
            record = recognizer.recognize_google(audio_data, language='ko-KR')
            print(f"[STT 성공] {audio_path} → {record}")
            return record
    except sr.UnknownValueError:
        print(f"[STT 실패] 음성을 인식하지 못했습니다: {audio_path}")
        return ""
    except sr.RequestError as e:
        print(f"[STT 오류] Google API 요청 실패: {e}")
        return ""
    except Exception as e:
        print(f"[오류] {audio_path} 처리 중 에러 발생: {e}")
        return ""

#음성파일 길이 측정
def get_wav_duration(file_path):
    with wave.open(file_path, 'rb') as wf:
        frames = wf.getnframes()       # 전체 프레임 수
        rate = wf.getframerate()       # 초당 프레임(샘플) 수
        duration = frames / float(rate) # 총 길이(초)
        return duration
    
# 3. STT로 구현된 텍스트 인식 정보를 다음과 같은 CSV 파일로 저장한다.(음성 파일내에서의 시간, 인식된 텍스트)
def audio_to_csv(directory_path, audio_name, duration_record):
    #4. 파일의 이름은 음성 파일의 이름과 같은 이름으로 저장하되 확장자는 .CSV로 저장한다.
    csv_name = os.path.splitext(audio_name)[0] + ".csv"
    csv_path = os.path.join(directory_path, csv_name)

    try:
        with open(csv_path, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["시간", "인식된 텍스트"])
            writer.writerow([duration_record[0], duration_record[1]])
        print(f"[저장 완료] {csv_path}")
    except Exception as e:
        print(f"[CSV 저장 오류] {csv_path}: {e}")

# 실행 부분
if __name__ == '__main__':
    directory_path = os.path.join(os.getcwd(), "records")
    files = save_directory_listing(directory_path)

    for audio_name in files:
        audio_path = os.path.join(directory_path, audio_name)
        duration = get_wav_duration(audio_path)  # 파일 길이(초)
        record = stt(audio_path)
        duration_record= (duration, record)
        if record:  # 인식된 텍스트가 있을 때만 CSV 저장
            audio_to_csv(directory_path, audio_name, duration_record)


#5. 전체 내용이 구현되면 javis.py 파일에 추가한다.
