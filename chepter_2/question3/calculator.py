#1. Python으로 UI를 만들 수 있는 PyQT 라이브러리를 설치한다.
# pip install PyQt5
#2. 아이폰 계산기와 최대한 유사하게 계산기 UI를 만든다. 출력 형태 및 버튼의 배치는 동일하게 해야한다. 색상이나 버튼의 모양까지 동일할 필요는 없다.
#3. 각각의 버튼을 누를 때 마다 숫자가 입력 될 수 있게 이벤트를 처리한다.

import sys
from PyQt5.QtWidgets import QApplication
from calculator_ui import CalculatorUI

class Calculator(CalculatorUI):
    def __init__(self):
        super().__init__()
        self.connect_buttons()

    def connect_buttons(self):
        for label, button in self.buttons.items():
            button.clicked.connect(lambda _, t=label: self.on_button_clicked(t))

    def on_button_clicked(self, text):
        if text == 'AC':
            self.display.setText('')
        #추후 작성
        elif text == '=':
            try:
                #보너스1. 사칙연산 계산
                #self.display에 있는 계산식을 계산 후 문자열로 전환하여 다시 출력
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except:
                self.display.setText("Error")
        elif text == '±':
            pass
        elif text == '%':
            pass
        else:
            self.display.setText(self.display.text() + text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())

#4. 이번 과제에서는 실제로 계산 기능까지 구현된 필요는 없다.
#5. 완성된 코드는 calculator.py 로 저장한다.
