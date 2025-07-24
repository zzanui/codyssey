import sys
from PyQt5.QtWidgets import QApplication
from calculator_ui import CalculatorUI

#1. Calculator 클래스를 만든다.
class Calculator(CalculatorUI):
    comma_count = False

    def __init__(self):
        super().__init__()
        self.connect_buttons()

    #7. UI의 각 버튼과 Calculator 클래스를 연결해서 완전한 동작을 구현한다.
    def connect_buttons(self):
        for label, button in self.buttons.items():
            button.clicked.connect(lambda _, t=label: self.on_button_clicked(t))

    #2. Calculator 클래스에 사칙 연산을 담당할 메소드인 add(), subtract(), multiply(), divide() 를 추가하고 동작할 수 있게 기능을 구현한다.
    def add(self, x, y):
        return x + y
    def subtract(self, x, y):
        return x - y
    def multiply(self, x, y):
        return x * y
    def divide(self, x, y):
        return x / y

    #3. Calculator 클래스에 추가로 초기화 및 음수양수, 퍼센트 등을 담당할 reset(), negative-positive(), percent() 메소드를 추가하고 기능을 구현한다.
    def reset(self):
        self.display.setText('')
    def negative_positive(self):
        value = eval(self.display.text())
        self.display.setText(str(-value))
    def percent(self):
        value = eval(self.display.text())
        self.display.setText(str(value / 100))

    #6. Calculator 클래스에 결과를 출력할 equal() 메소드를 추가하고 기능을 구현한다.
    def equal(self):
        expression = self.display.text()
        try:
            # 연산자와 피연산자를 분리 (한 연산자만 있다고 가정)
            if '+' in expression:
                x, y = map(float, expression.split('+'))
                result = self.add(x, y)
            elif '-' in expression:
                x, y = map(float, expression.split('-'))
                result = self.subtract(x, y)
            elif 'X' in expression:
                x, y = map(float, expression.split('X'))
                result = self.multiply(x, y)
            elif '÷' in expression:
                x, y = map(float, expression.split('÷'))
                result = self.divide(x, y)
            else:
                result = eval(expression)  # 연산자가 없으면 그대로 계산

            #보너스2. 소수점 6자리 이하의 경우 반올림한 결과로 줄여서 출력한다.
            if isinstance(result, float):
                result = round(result, 6)

            #보너스1. 계산 결과가 출력될 때 출력되는 값의 길이에 따라서 폰트의 크기를 조정해서 전체 내용이 한번에 출력될 수 있도록 한다.
            result_str = str(result)
            if len(result_str) > 20:
                self.display.setStyleSheet("font-size: 20px; padding: 15px; background-color: black; color: white; border: none;")
            else:
                self.display.setStyleSheet("font-size: 32px; padding: 15px; background-color: black; color: white; border: none;")

            self.display.setText(result_str)

        except Exception as e:
            self.display.setText("Error")

    def on_button_clicked(self, text):
        if text == 'AC':
            self.reset()
        elif text == '=':
            self.equal()
        elif text == '±':
            self.negative_positive()
        elif text == '%':
            self.percent()
        #5. 소수점 키를 누르면 소수점이 입력된다. 단 이미 소수점이 입력되어 있는 상태에서는 추가로 입력되지 않는다.
        elif text == '.':
            if self.comma_count:
                self.display.setText(self.display.text() + text)
                self.comma_count = False
        else:
            #4. 숫자키를 누를 때 마다 화면에 숫자가 누적된다.
            self.display.setText(self.display.text() + text)
            self.comma_count = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())

#8. 완성된 코드는 calculator.py 로 저장한다.
