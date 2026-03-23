import streamlit as st
import requests

# 1. API를 이용해서 실시간 환욜 정보 가져오기
def get_exchange_rate(base, target, amount):
  # 무료 환율 API 주소(base변수에 따라서 기준 '통화'가 바뀜)
  url = f"https://open.er-api.com/v6/latest/{base}"

  # 환율 주소를 인터넷으로 요청해서 데이터 받아오기
  response = requests.get(url)
  data = response.json() # 파이썬이 읽기 쉽게 변환

  # 알고싶은 통화(target변수)의 데이터가 있는지 확인
  if target in data['rates']:
    rate = data['rates'][target]  # 현재 환율
    result = amount + rate  # 환전된 금액
    return rate, result
  else:
    return None, None

# 2. 웹페이지 화면 구성하기
st.title("실시간 환율 계산기")

# 자주 사용하는 통화 기호 리스트
currency_list = ["KRW","USD","EUR","JPY","GBP","AUD"]

# 화면을 좌,우(2단)단으로 나누기
col1, col2 = st.columns(2)

with col1:
  # 내가 가진 돈(기본값 USD) 설정
  base_currency = st.selectbox("기준통화", currency_list, index=1)

with col2:
  # 목표 통화 설정
  target_currency = st.selectbox("목표 통화", currency_list, index=0)

col3, col4 = st.columns(2)

with col3:
  # 환전할 금액 입력
  base_amount = st.number_input("", min_value=1.0, value=1.0, key="input1")

with col4:
  target_amount = st.number_input("", min_value=1.0, value=1.0, key="input1")
  
# 3. 환율 계산 버튼과 결과 출력 로직
if st.button("환율 계산"):
  rate, result = get_exchange_rate(base_currency, target_currency, base_amount)
  st.info(f"환전결과 : {base_amount:,.2f}{base_currency} -> {result:,.2f}{target_currency}")
else:
  st.error("환율 정보를 가져오는데 실패했습니다.")


