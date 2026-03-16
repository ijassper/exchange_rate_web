import random as rd

print("로또번호 생성기")

lotto_num = rd.sample(range(1,46),6)

lotto_num.sort()

print(f"이번주 행운의 번호 : {lotto_num}")

