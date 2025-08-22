from typing import Callable, Union
import math
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QApplication
from PyQt5.QtCore import Qt

# 기존 기본 계산기 클래스를 불러옵니다.
# - calculator.py 안에는 CalculatorUI(화면) + Calculator(기능/입력처리)가 정의되어 있습니다.
# - 본 파일에서는 Calculator를 상속하여 공학용 기능을 확장합니다.
from calculator import Calculator  # 같은 폴더에 calculator.py가 있어야 함


Number = Union[int, float]#숫자 판별

#1. Calculator 클래스를 상속받아서 EngineeringCalculator 클래스를 만든다.
class EngineeringCalculator(Calculator):
    """
       1)  괄호()                         
       2)  mc (메모리 클리어)              
       3)  m+ (메모리 더하기)              
       4)  m- (메모리 빼기)                
       5)  mr (메모리 불러오기)            
       6)  C  (클리어)                     
       7)  ±  (부호 변경)                  
       8)  %  (퍼센트)                     
       9)  2nd (보조 기능 전환)            
       10) ★ x² (제곱)                     
       11) ★ x³ (세제곱)                   
       12) xʸ (거듭제곱: x의 y승)          
       13) eˣ (지수함수)                   
       14) 10ˣ (10의 거듭제곱)             
       15) 1/x (역수)                      
       16) ²√x (제곱근)                    
       17) ³√x (세제곱근)                  
       18) ʸ√x (y제곱근)                   
       19) ln  (자연로그)                  
       20) log₁₀ (상용로그)                
       21) x! (팩토리얼)                   
       22) ★ sin (사인)                    
       23) ★ cos (코사인)                  
       24) ★ tan (탄젠트)                  
       25) ★ sinh (하이퍼볼릭 사인)        
       26) ★ cosh (하이퍼볼릭 코사인)      
       27) ★ tanh (하이퍼볼릭 탄젠트)      
       28)  e  (자연상수)                  
       29)  EE (지수 표기 입력 도움)       
       30)  Rad (라디안/도 전환 토글)      
    """

    def __init__(self):
        # 부모의 __init__에서는 CalculatorUI를 호출하여 self.init_ui()를 부르므로 오버라이드.
        super().__init__()
        for label, button in self.buttons.items():
            try:
                button.clicked.disconnect()
            except TypeError:
                # 연결이 안 되어있을 수도 있으므로 무시
                pass

        # 공학용 계산기의 화면/창 속성
        self.setWindowTitle("iPhone ENCalc")
        self.setFixedSize(900, 480)

        # 각종 상태값
        self.use_radians: bool = True  # True=라디안, False=도(degree)

        # 버튼 시그널 재연결(부모의 connect_buttons는 기본형 버튼용이므로 재정의)
        self._connect_engineering_buttons()


    # UI 구성
    def init_ui(self):
        """
        이 메소드는 부모(CalculatorUI.__init__) 호출 시 자동 실행
        """
        self.main_layout = QVBoxLayout()
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet(
            "font-size: 32px; padding: 15px; background-color: black; color: white; border: none;"
        )
        self.main_layout.addWidget(self.display)

        self.grid_layout = QGridLayout()
        self.buttons = {}

        # 아이폰 공학용 레이아웃(가로형)과 유사한 버튼 배열
        buttons = [
            ["(", ")", "mc", "m+", "m-", "mr", "C", "±", "%", "÷"],
            ["2nd", "x²", "x³", "xʸ", "eˣ", "10ˣ", "7", "8", "9", "×"],
            ["1/x", "²√x", "³√x", "ʸ√x", "ln", "log₁₀", "4", "5", "6", "−"],
            ["x!", "sin", "cos", "tan", "e", "EE", "1", "2", "3", "+"],
            ["Rad", "sinh", "cosh", "tanh", "π", "Rand", "0", ".", "="]
        ]

        for row_idx, row in enumerate(buttons):
            col_offset = 0
            for col_idx, label in enumerate(row):
                btn = QPushButton(label)
                self.buttons[label] = btn

                # '0' 버튼은 가로로 2칸
                if label == '0':
                    btn.setFixedSize(170, 70)
                    self.grid_layout.addWidget(btn, row_idx + 1, col_idx, 1, 2)
                    col_offset = 1
                else:
                    btn.setFixedSize(80, 70)
                    self.grid_layout.addWidget(btn, row_idx + 1, col_idx + col_offset)

                # 색상 스타일: 연산자/기능키와 숫자키를 구분
                if label in ['÷', '×', '−', '+', '=']:
                    btn.setStyleSheet(self._style_button("#ff9500", "white"))
                elif label in ['C', '±', '%']:
                    btn.setStyleSheet(self._style_button("#a5a5a5", "black"))
                else:
                    btn.setStyleSheet(self._style_button("#333333", "white"))

        self.main_layout.addLayout(self.grid_layout)
        self.setLayout(self.main_layout)

    def _style_button(self, bg_color: str, text_color: str) -> str:
        """버튼 둥근 스타일(아이폰 유사)"""
        return f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            font-size: 20px;
            border: none;
            border-radius: 35px;
        }}
        QPushButton:pressed {{
            background-color: #666666;
        }}
        """

    # 버튼-핸들러 연결
    def _connect_engineering_buttons(self):
        for label, button in self.buttons.items():
            button.clicked.connect(lambda _, t=label: self.on_engineering_button_clicked(t))

    # 폰트 크기 자동 조절, 반올림)
    def _format_and_set_result(self, value: Number):
        if isinstance(value, float):
            #실수는 소수점 6자리 반올림
            value = round(value, 6)
            if value.is_integer():
                value = int(value)

        s = str(value)
        #너무 긴 결과는 폰트 크기 축소
        if len(s) > 20:
            self.display.setStyleSheet("font-size: 20px; padding: 15px; background-color: black; color: white; border: none;")
        else:
            self.display.setStyleSheet("font-size: 32px; padding: 15px; background-color: black; color: white; border: none;")
        self.display.setText(s)

    #2. 공학용 계산기에서 추가된 30가지 기능을 정리하고 이 중에서 삼각함수 관련 기능인 sin, cos, tan, sinh, cosh, tanh와 원주율 과 x의 제곱 그리고 x의 세제곱 등을 담당할 메소드의 이름을 짓고 그 내용을 구현
    #문자열을 부동소수로 변환
    def _get_current_value(self) -> float:
        # 빈 문자열이면 0.0 반환
        # 사칙연산 수식(예: '12+3')처럼 숫자 하나가 아니면 ValueError 발생 가능
        txt = self.display.text().strip()
        if txt == "":
            return 0.0
        return float(txt)

    #제곱
    def op_square(self):
        """현재 값의 제곱(x²)을 계산"""
        try:
            x = self._get_current_value()
            self._format_and_set_result(x * x)
        except Exception:
            self.display.setText("Error")

    #세제곱
    def op_cube(self):
        """현재 값의 세제곱(x³)을 계산"""
        try:
            x = self._get_current_value()
            self._format_and_set_result(x * x * x)
        except Exception:
            self.display.setText("Error")

    #원주율(상수)
    def op_pi(self):
        pi_str = repr(math.pi)  # 최대한 정밀한 문자열 표현
        #값이 이미 있으면 뒤에 π 값을 이어붙임
        if self.display.text():
            self.display.setText(self.display.text() + pi_str)
        #표시창이 비어 있으면 π로 설정
        else:
            self.display.setText(pi_str)

    # 각종 삼각함수
    def _apply_trig(self, func: Callable[[float], float], x: float) -> float:
        return func(x)

    # sin
    def op_sin(self):
        #현재 값을 (라디안/도 설정에 맞춰) sin에 적용
        try:
            x = self._get_current_value()
            rad = x if self.use_radians else math.radians(x)
            self._format_and_set_result(self._apply_trig(math.sin, rad))
        except Exception:
            self.display.setText("Error")

    # cos
    def op_cos(self):
        #현재 값을 (라디안/도 설정에 맞춰) cos에 적용
        try:
            x = self._get_current_value()
            rad = x if self.use_radians else math.radians(x)
            self._format_and_set_result(self._apply_trig(math.cos, rad))
        except Exception:
            self.display.setText("Error")

    # tan
    def op_tan(self):
        #현재 값을 (라디안/도 설정에 맞춰) tan에 적용
        try:
            x = self._get_current_value()
            rad = x if self.use_radians else math.radians(x)
            self._format_and_set_result(self._apply_trig(math.tan, rad))
        except Exception:
            self.display.setText("Error")

    # sinh
    def op_sinh(self):
        #현재 값을 하이퍼볼릭 사인(sinh)에 적용
        try:
            x = self._get_current_value()
            self._format_and_set_result(self._apply_trig(math.sinh, x))
        except Exception:
            self.display.setText("Error")

    # cosh
    def op_cosh(self):
        #현재 값을 하이퍼볼릭 코사인(cosh)에 적용
        try:
            x = self._get_current_value()
            self._format_and_set_result(self._apply_trig(math.cosh, x))
        except Exception:
            self.display.setText("Error")

    # tanh
    def op_tanh(self):
        #현재 값을 하이퍼볼릭 탄젠트(tanh)에 적용
        try:
            x = self._get_current_value()
            self._format_and_set_result(self._apply_trig(math.tanh, x))
        except Exception:
            self.display.setText("Error")



    # 4. 완성된 클래스의 기능들과 UI의 버튼들을 매칭 시킨다.
    def on_engineering_button_clicked(self, text: str):
        #sin, cos, tan, sinh, cosh, tanh, π, x², x³, 
        #구현한 공학용 기능 매핑
        op_map = {
            "sin": self.op_sin,
            "cos": self.op_cos,
            "tan": self.op_tan,
            "sinh": self.op_sinh,
            "cosh": self.op_cosh,
            "tanh": self.op_tanh,
            "x²": self.op_square,
            "x³": self.op_cube,
            "π": self.op_pi,
            "C": self.reset,               # 기본기의 reset 재사용
        }
        if text in op_map:
            op_map[text]()  # 해당 연산 수행
            return

        # 2) 연산자 기호 치환(아이폰은 ×/−를 사용하지만 기본 계산기는 X/-)
        if text == "×":
            self.display.setText(self.display.text() + "X")
            return
        if text == "−":
            self.display.setText(self.display.text() + "-")
            return

        # 3) 괄호/메모리/로그 등: 여기서는 '표시'만 수행(실제 계산은 미구현)
        display_only = {"(", ")", "mc", "m+", "m-", "mr", "2nd", "xʸ", "eˣ", "10ˣ",
                        "1/x", "²√x", "³√x", "ʸ√x", "ln", "log₁₀", "x!", "e", "EE", "Rand"}
        if text in display_only:
            # 괄호 등은 단순히 붙여넣기만 함(평가 엔진은 과제 범위 밖)
            self.display.setText(self.display.text() + text)
            return

        # 4) 그 외(숫자/점/+, ÷, =, %, ± 등)는 기본 동작으로 처리
        super().on_button_clicked(text)


# 단독 실행(테스트용)
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = EngineeringCalculator()
    window.show()
    sys.exit(app.exec_())



#5. 완성된 코드는 engineering_calculator.py 로 저장한다.