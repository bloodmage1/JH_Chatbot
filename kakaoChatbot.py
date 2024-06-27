import sys
import re

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "model_jh" 
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
model.config.use_cache = False

def generate_answer(model, tokenizer, question, max_length = 24):
    inputs = tokenizer(question, return_tensors="pt", add_special_tokens=True)
    inputs = {key: value for key, value in inputs.items() if key != 'token_type_ids'}
    output = model.generate(**inputs, max_length=max_length)
    
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    return answer

# questions = [
#     "당신의 장점이 무엇입니까?",
#     "앞으로의 꿈은 무엇입니까?",
#     "이직할 때에 가장 우선순위는 무엇인가요?"
# ]

def extract_and_remove_first_question(text):
    pattern = r'^(.*?\?)'
    match = re.search(pattern, text)
    if match:
        first_question = match.group(1)  # 첫 번째 문장 저장
        remaining_text = re.sub(pattern, '', text, count=1)  # 첫 문장 제거
        return first_question, remaining_text
    return "", text  

def truncate_after_spot(answer, number='.'):
    pattern = re.escape(number) + r'.*'
    truncated_answer = re.sub(pattern, '', answer, flags=re.DOTALL)
    return truncated_answer

class MessageLabel(QTextEdit):
    def __init__(self, text, is_user=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(text)
        self.is_user = is_user
        self.setWordWrapMode(3) 
        self.setSizePolicy(self.sizePolicy().Expanding, self.sizePolicy().Expanding)
        self.setStyleSheet(self.get_stylesheet())

    def get_stylesheet(self): # 뭔가 뻘짓한 느낌
        if self.is_user:
            return (
                "background-color: #FFFF00;"
                "border-radius: 10px;"
                "padding: 10px;"
                "margin: 5px;"
                "max-height: 25%;"
            )
        else:
            return (
                "background-color: #FFFFFF;"
                "border-radius: 10px;"
                "padding: 10px;"
                "margin: 5px;"
                "max-height: 25%;"
            )

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        tab = QTabWidget()
        general_tab = self.return_general_tab()
        chatbot_tab = self.return_chatbot_tab()
        tab.addTab(chatbot_tab, "챗봇")
        tab.addTab(general_tab, "속성")

        button_layout = QHBoxLayout()
        button_layout.addWidget(QPushButton("확인"))
        button_layout.addWidget(QPushButton("취소"))
        button_layout.addWidget(QPushButton("적용(A)"))
        button_layout.setAlignment(Qt.AlignRight)

        pal = tab.palette()
        pal.setColor(QPalette.Window, Qt.transparent)
        tab.setPalette(pal)

        main_layout.addWidget(tab)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("JH_Chatbot")
        self.setWindowIcon(QIcon("./kakao_icon.svg"))
        self.resize(420, 565)
        self.show()

    def return_chatbot_tab(self):
        layout = QVBoxLayout()

        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignTop)

        chat_scroll = QScrollArea()
        chat_scroll.setWidgetResizable(True)
        chat_widget = QWidget()
        chat_widget.setLayout(self.chat_area)
        chat_scroll.setWidget(chat_widget)
        chat_scroll.setStyleSheet("background-color: #87CEEB;")
        layout.addWidget(chat_scroll)

        input_line = QLineEdit()
        layout.addWidget(input_line)

        send_button = QPushButton('Send')
        send_button.clicked.connect(lambda: self.sendMessage(input_line))
        layout.addWidget(send_button)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def sendMessage(self, input_line):
        user_message = input_line.text()
        if user_message.strip() == "":
            return

        user_label = MessageLabel(user_message, is_user=True)
        self.chat_area.addWidget(user_label, 0, Qt.AlignRight)

        bot_response = self.getBotResponse(user_message)
        bot_label = MessageLabel(bot_response, is_user=False)
        self.chat_area.addWidget(bot_label, 0, Qt.AlignLeft)

        input_line.clear()

    def getBotResponse(self, message):

        answer = generate_answer(model, tokenizer, message)
        _, tr_answer = extract_and_remove_first_question(answer)

        tr_answer = truncate_after_spot(tr_answer)
        
        return tr_answer

    def return_general_tab(self):
        formlayout = QFormLayout()

        image_label = self.kakao_icon_label()
        lineedit1 = QLineEdit("카카오톡")
        lineedit1.setFixedHeight(27)
        lineedit1.setTextMargins(0, 5, 0, 0)
        lineedit1.setAlignment(Qt.AlignTop)

        formlayout.addRow(image_label, lineedit1)
        formlayout.addRow(self.makeHLine())
        formlayout.addRow("파일 형식:", QLabel("바로 가기(.lnk)"))
        formlayout.addRow("설명:", QLabel("KakaoTalk"))
        formlayout.addRow(self.makeHLine())
        formlayout.addRow("위치:", QLabel("C:\\Users\\Public\\Desktop"))
        formlayout.addRow("크기:", QLabel("1.17KB (1,202 바이트)"))
        formlayout.addRow("디스크 할당 크기:", QLabel("4.00KB (4,096 바이트)"))
        formlayout.addRow(self.makeHLine())
        formlayout.addRow("만든 날짜:", QLabel("‎2024‎년 ‎3‎월 ‎10‎일 ‎일요일, ‏‎오후 2:17:46"))
        formlayout.addRow("수정한 날짜:", QLabel("‎2024‎년 ‎3‎월 ‎10‎일 ‎일요일, ‏‎오후 2:17:46"))
        formlayout.addRow("엑세스한 날짜:", QLabel("‎2024‎년 ‎3‎월 ‎10‎일 ‎일요일, ‏‎오후 2:17:46"))
        formlayout.addRow(self.makeHLine())

        property = QHBoxLayout()
        property.addWidget(QCheckBox("읽기 전용(R)"))
        property.addWidget(QCheckBox("숨김(H)"))
        property.addWidget(QPushButton("고급(D)..."))
        formlayout.addRow("특성:", property)

        widget = QWidget()
        widget.setLayout(formlayout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(widget)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setWidgetResizable(True)

        return scroll_area

    def kakao_icon_label(self):
        image_label = QLabel()
        pixmap = QPixmap("./kakao_icon.svg")
        pixmap = pixmap.scaledToHeight(35)
        image_label.setPixmap(pixmap)
        return image_label

    def makeHLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())