# JH_Chatbot

나에 대한 소개 정보를 학습하여 대답해주는 챗봇

## 1 프로젝트 소개

모두 다른 회사에서 면접에서 지원자에게 물어보는 질문은 한정적이라는 점을 깨닫고 공통적으로 할 수 있는 질문을 추린 다음 그 내용을 언어 모델에 학습시킨 후 PyQt로 쉽게 이용할 수 있게끔 만들어 보았다.

![image.jpg1](https://github.com/bloodmage1/JH_Chatbot/blob/main/img/first_capture.png) |![image.jpg2](https://github.com/bloodmage1/JH_Chatbot/blob/main/img/question1.png) |![image.jpg3](https://github.com/bloodmage1/JH_Chatbot/blob/main/img/question2.png)
 --- | --- | --- | 
|실행했을 때, 나타나는 처음 화면입니다|로잘린드 두번째 문제의 스크린샷입니다. 여러가지 난해한 질문에도 잘 답변합니다|로잘린드 첫번째 문제의 스크린샷입니다. 질문의 내용이 살짝 바뀌어도 제대로 대답하는 모습입니다.|


## 2. 개발 환경

- Window OS, Window 11
- Python 3.8.7
- PyQt5


## 3. 학습 환경(언어모델)

- Python 3.11.7
- torch 2.3.0+cu118
- transformers 4.30.1
- peft 0.10.0
- trl 0.7.10

## 4. 각 함수의 기능 설명

### Class MessageLabel

- def get_stylesheet(self):

  - 메시지가 사용자로부터 온 것인지 아닌지에 따라 적절한 스타일시트를 반환합니다.

### Class main

- def return_chatbot_tab(self):

  - 챗봇 탭의 레이아웃을 생성하고 반환합니다. 여기에는 채팅 영역, 입력 라인, 전송 버튼이 포함됩니다.
  
- def sendMessage(self, input_line):

  - 메시지를 보내는 과정을 처리하며, 사용자의 메시지와 봇의 응답을 채팅 영역에 표시합니다.
  
- def getBotResponse(self, message):

  - 주어진 메시지를 사용하여 챗봇의 응답을 생성하고, 응답을 형식화하는 추가 처리 단계를 적용합니다.

- def return_general_tab(self):

  - 일반 속성 탭의 레이아웃을 생성하고 반환합니다. 여기에는 파일 정보와 속성이 포함됩니다.
- def kakao_icon_label(self):

  - KakaoTalk 아이콘을 표시하는 QLabel 위젯을 생성하고 반환합니다.
- def makeHLine(self):

  - 레이아웃에서 구분선으로 사용되는 수평선(QFrame)을 생성하고 반환합니다.


## 5 학습한 자료

<img src="https://github.com/bloodmage1/JH_Chatbot/blob/main/img/introduce_capture.png"/>

나에 대한 각각의 질문1, 질문2(variation) 컬럼에 대하여 답변1을 담고 있는 csv 파일입니다.

## 6 from_pretained model
[https://huggingface.co/beomi/llama-2-koen-13b] 이 모델을 바탕으로 제 액셀 파일을 학습했습니다.