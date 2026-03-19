import streamlit as st
import random as rd

st.title("로또번호 생성기")
st.write("버튼을 누르면 로또 번호가 생성되요.")

if st.button("로또 본호 뽑기"):
  lotto_num = rd.sample(range(1,46),6)
  lotto_num.sort()

  st.subheader(f"이번주 행운의 번호 : {lotto_num}")

