#2. 시스템의 마이크를 인식하고 음성을 녹음하는 부분은 외부 라이브러리를 사용하는 것이 가능하다.
import pyaudio
import wave
from datetime import datetime

chunk = 1024 # 한 번에 읽어올 데이터 크기
FORMAT = pyaudio.paInt16 # 오디오 포맷
CHANNELS = 1 # 모노 채널
RATE = 44100 # 샘플링 레이트
RECORD_SECONDS = 5 # 녹음할 시간 (초)
#3. 파일들은 파이썬 앱이 실행되고 있는 하위에 records 폴더에 모두 저장된다.
#4. 파일의 이름은 녹음 날짜와 시간을 참조해서 ‘년월일-시간분초’와 같은 형태로 저장한다.
WAVE_OUTPUT_FILENAME = 'records/' + datetime.now().strftime('%Y.%m.%d-%H-%M-%S')+'.wav'# 저장할 파일 이름

audio = pyaudio.PyAudio()

#1. 시스템의 마이크를 인식하고 음성을 녹음하는 부분을 완성한다.
#마이크 열기
stream = audio.open(format=FORMAT, channels=CHANNELS,
rate=RATE, input=True,
frames_per_buffer=chunk)
print("Start Recording...")

frames = []

#약 5초간 녹음을 진행
for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
    data = stream.read(chunk)
    frames.append(data)

print("녹음 종료")

# 녹음 종료
stream.stop_stream()
stream.close()
audio.terminate()

# WAV 파일 저장
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

#5. 작성한 코드는 javis.py로 저장한다.