# 1. Python으로 UI를 만들 수 있는 PyQT 라이브러리를 설치한다.
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QApplication
from PyQt5.QtCore import Qt

# 2. 아이폰을 가로로 했을 때 나타나는 공학용 계산기와 최대한 유사하게 계산기 UI를 만든다. 출력 형태 및 버튼의 배치는 동일하게 해야한다. 색상이나 버튼의 모양까지 동일할 필요는 없다.
class EngineeringCalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone ENCalc')#제목 명
        self.setFixedSize(900,480)#전체 사이즈
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.display = QLineEdit()#계산기 화면
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet(
             "font-size: 32px; padding: 15px; background-color: black; color: white; border: none;" 
        )
        self.main_layout.addWidget(self.display)

        self.grid_layout = QGridLayout()
        self.buttons = {}

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

                # 버튼 크기 조정
                if label == '0':
                    btn.setFixedSize(170,70)
                    # addWidget(widget, row, column, rowSpan, columnSpan) # 계산기 화면이 위에 있으므로, row_idx+1
                    self.grid_layout.addWidget(btn, row_idx + 1, col_idx, 1, 2)  
                    col_offset = 1
                else:
                    btn.setFixedSize(80,70)
                    self.grid_layout.addWidget(btn, row_idx + 1, col_idx + col_offset)
                
                #버튼 색상 설정
                if label in ['÷', '×', '−', '+', '=']:
                    btn.setStyleSheet(self.style_button("#ff9500", "white"))
                elif label in ['C', '±', '%']:
                    btn.setStyleSheet(self.style_button("#a5a5a5", "black"))
                else:
                    btn.setStyleSheet(self.style_button("#333333", "white"))
            
        self.main_layout.addLayout(self.grid_layout)
        self.setLayout(self.main_layout)

    #버튼 둥글게
    def style_button(self, bg_color, text_color):
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
    def on_button_clicked(self, text):
        if text == 'AC':
            self.reset()
        elif text == '=':
            self.equal()
        elif text == '±':
            self.negative_positive()
        elif text == '%':
            self.percent()
        elif text == '.':
            if self.comma_count:
                self.display.setText(self.display.text() + text)
                self.comma_count = False
        elif text in '123456789':
            # 3. 각각의 버튼을 누를 때 마다 숫자가 입력 될 수 있게 이벤트를 처리한다.
            self.display.setText(self.display.text() + text)
            self.comma_count = True    
        
class EngineeringCalculator(EngineeringCalculatorUI):

    def __init__(self):
        super().__init__()
        self.connect_buttons()

    def connect_buttons(self):
        for label, button in self.buttons.items():
            button.clicked.connect(lambda _, t=label: self.on_button_clicked(t))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = EngineeringCalculator()
    window.show()
    sys.exit(app.exec_())
# 4. 이번 과제에서는 실제로 계산 기능까지 구현된 필요는 없다.
# 5.완성된 코드는 engineering_calculator.py 로 저장한다.