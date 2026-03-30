import streamlit as st
import requests

# 1. API를 이용해서 실시간 환욜 정보 가져오기
def get_exchange_rate(base, target):
  # 무료 환율 API 주소(base변수에 따라서 기준 '통화'가 바뀜)
  url = f"https://open.er-api.com/v6/latest/{base}"

  # 환율 주소를 인터넷으로 요청해서 데이터 받아오기
  response = requests.get(url)
  data = response.json() # 파이썬이 읽기 쉽게 변환

  # 알고싶은 통화(target변수)의 데이터가 있는지 확인
  if target in data['rates']:
    rate = data['rates'][target]  # 현재 환율
    # result = amount + rate  # 환전된 금액
    return rate
  else:
    return None

# 콜백함수와 세션 설정
if "amount_top" not in st.session_state:
  st.session_state.amount_top = 1.0
  st.session_state.amount_bot = 1.0
  st.session_state.curr_top = "USD"
  st.session_state.curr_bot = "KRW"

# 계산기용 세션 설정
if "cal_formula" not in st.session_state:
  st.session_state.cal_formula = ""

  # 미달러 1.0 기준 원화 계산
  rate = get_exchange_rate("USD","KRW")
  if rate:
    st.session_state.amount_bot = 1.0 * rate

def calc_bottom():
  rate = get_exchange_rate(st.session_state.curr_top, st.session_state.curr_bot)
  if rate:
    st.session_state.amount_bot = st.session_state.amount_top * rate

def calc_top():
  rate = get_exchange_rate(st.session_state.curr_bot, st.session_state.curr_top)
  if rate:
    st.session_state.amount_top = st.session_state.amount_bot * rate

def currency_change():
  calc_bottom()

# 계산기 기능 함수 만들기
def click_button(val):
  if val == "=":
    try:
      # 수식 계산
      formula = st.session_state.cal_formula.replace('x','*').replace('%','/')
      result_value = eval(formula)
      st.session_state.amount_top = float(result_value)
      st.session_state.cal_formula = str(result_value)
      calc_bottom()
    except:
      st.session_state.cal_formula = "Error"
  elif val == 'C':
    st.session_state.cal_formula = ""
  elif val == "환율 적용":
    try:
      # 계산 결과를 상단 환율 입력 필드로 전송
      st.session_state.amount_top = float(st.session_state.cal_formula)
      calc_bottom()
    except:
      pass
  else:
    st.session_state.cal_formula += str(val)

# 2. 웹페이지 화면 구성하기
st.title("실시간 환율 계산기")

# 자주 사용하는 통화 기호 리스트
currency_list = ["KRW","USD","EUR","JPY","GBP","AUD"]

# 화면을 좌,우(2단)단으로 나누기
col1, col2 = st.columns(2)

with col1:
  # 내가 가진 돈(기본값 USD) 설정
  st.selectbox("기준통화", currency_list, key="curr_top", on_change=currency_change)

with col2:
  # 환전할 금액 입력
  st.number_input("", min_value=1.0, key="amount_top", on_change=calc_bottom)

col3, col4 = st.columns(2)

with col3:
  # 목표 통화 설정
  st.selectbox("목표 통화", currency_list, key="curr_bot", on_change=currency_change)

# 3. 환율 계산 실시간 결과 출력 로직
#if base_currency == target_currency:
#  rate = 1.0
#  result = base_amount
#else:
#  rate = get_exchange_rate(base_currency, target_currency)
#  if rate is not None:
#    result = base_amount * rate
#  else:
#    result = 0.0

with col4:
  st.number_input("", key="amount_bot", on_change=calc_top)
    
# 계산기 UI 만들기
st.subheader("계산기")

# 숫자를 입력할 텍스트 박스만들기
st.text_input("수식입력", value=st.session_state.cal_formula)

# 계산기 버튼 만들기
buttons = [
  '7','8','9','%',
  '4','5','6','x',
  '1','2','3','-',
  '0','.','=','+',
]

cols = st.columns(4)
for i, btn in enumerate(buttons):
  with cols[i%4]:
    if st.button(btn, key=f"btn_{btn}", use_container_width=True):
      click_button(btn)

if st.button("환율 계산", use_container_width=True):
  click_button("환율 적용")
