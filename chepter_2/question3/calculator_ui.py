from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QApplication
from PyQt5.QtCore import Qt

class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone Calc')#제목 명
        self.setFixedSize(330,480)#전체 사이즈
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
            ['AC', '±', '%', '÷'],
            ['7', '8', '9', 'X'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row_idx, row in enumerate(buttons):
            col_offset = 0
            for col_idx, label in enumerate(row):
                btn = QPushButton(label)
                self.buttons[label] = btn

                # 버튼 크기 조정
                if label == '0':
                    btn.setFixedSize(140,70)
                    # addWidget(widget, row, column, rowSpan, columnSpan) # 계산기 화면이 위에 있으므로, row_idx+1
                    self.grid_layout.addWidget(btn, row_idx + 1, 0, 1, 2)  
                    col_offset = 1
                else:
                    btn.setFixedSize(70,70)
                    self.grid_layout.addWidget(btn, row_idx + 1, col_idx + col_offset)
                
                #버튼 색상 설정
                if label in ['/', '*', '-', '+', '=']:
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

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec_())