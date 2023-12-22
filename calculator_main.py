import math
import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_line1 = QHBoxLayout()
        layout_line2 = QHBoxLayout()
        layout_line3 = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        self.equation = QLineEdit("")

        ### layout_equation_solution 레이아웃에 수식 및 답을 같이 표시하는 위젯을 추가
        layout_equation_solution.addRow(self.equation)

        ### 사칙연산 및 연산자 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")
        button_remainder = QPushButton("%")
        button_square = QPushButton("x²")
        button_square_root = QPushButton("√")
        button_fraction = QPushButton("1/x")

        ### =, C, CE, Backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("C")
        button_clearentry = QPushButton("CE")
        button_backspace = QPushButton("◀")

        ### 첫 번째 줄에 나머지, CE, C, Backspace 버튼들의 제 역할들에 시그널 설정
        button_remainder.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_clear.clicked.connect(self.button_clear_clicked)
        button_clearentry.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, C, CE, backspace 위젯 생성
        layout_line1.addWidget(button_remainder)
        layout_line1.addWidget(button_clearentry)
        layout_line1.addWidget(button_clear)
        layout_line1.addWidget(button_backspace)

        ### 두 번째 줄에 역수, 제곱, 제곱근, 나머지 버튼들의 제 역할들에 시그널 설정
        button_square.clicked.connect(self.button_square_clicked)
        button_square_root.clicked.connect(self.button_square_root_clicked)
        button_fraction.clicked.connect(self.button_fraction_clicked)
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        ### 1/x, x², √, / 위젯 생성
        layout_line2.addWidget(button_fraction)
        layout_line2.addWidget(button_square)
        layout_line2.addWidget(button_square_root)
        layout_line2.addWidget(button_division)

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_equal.clicked.connect(self.button_equal_clicked)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        ### 각 숫자 버튼들의 옆에 x, -, +, =, +/- 연산 기호 위젯 생성
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number >0:
                x,y = divmod(number-1, 3)
                layout_line3.addWidget(number_button_dict[number], x, y)
            elif number==0:
                layout_line3.addWidget(number_button_dict[number], 3, 1)

        ### x, -, +, = 기호 윈도우 계산기에 맞게 자리 배치
        layout_line3.addWidget(button_product, 0, 3)
        layout_line3.addWidget(button_minus, 1, 3)
        layout_line3.addWidget(button_plus, 2, 3)
        layout_line3.addWidget(button_equal, 3, 3)

        ### 소숫점 버튼과 +/- 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_line3.addWidget(button_dot, 3, 2)

        button_negate = QPushButton("+/-")
        button_negate.clicked.connect(self.button_negate_clicked)
        layout_line3.addWidget(button_negate, 3, 0)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_line1)
        main_layout.addLayout(layout_line2)
        main_layout.addLayout(layout_line3)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################

    ### 부호 바꾸는 함수
    def button_negate_clicked(self):
        num = float(self.equation.text())
        result = -num
        self.equation.setText(str(result))

    ### 제곱근 구하는 함수
    def button_square_root_clicked(self):
        num = float(self.equation.text())
        result = math.sqrt(num)
        self.equation.setText(str(result))
    ### 제곱 구하는 함수
    def button_square_clicked(self):
        num = float(self.equation.text())
        result = num * num
        self.equation.setText(str(result))
    ### 역수 구하는 함수
    def button_fraction_clicked(self):
        num = float(self.equation.text())
        if num == 0:
            self.equation.setText("0으로 나눌 수 없습니다.") # 0을 분모로 가지게 되면 실패글이 뜨게 만듬
        else:
            result = 1 / num
            self.equation.setText(str(result))

    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        equation += operation
        self.equation.setText(equation)

    def button_equal_clicked(self):
        equation = self.equation.text()
        equation = eval(equation)
        self.equation.setText(str(equation))

    def button_clear_clicked(self):
        self.equation.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())