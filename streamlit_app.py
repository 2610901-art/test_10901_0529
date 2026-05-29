import streamlit as st

# 1. 앱 페이지 설정
st.set_page_config(page_title="스마트 자판기", page_icon="🥤", layout="centered")

# 2. 초기 데이터 세팅 (앱이 처음 실행될 때만 초기화)
if "vending_machine" not in st.session_state:
    st.session_state.vending_machine = {
        "음료수": [
            {"name": "콜라 🥤", "price": 1200, "stock": 5},
            {"name": "사이다 🍏", "price": 1100, "stock": 3},
            {"name": "이온음료 ⚡", "price": 1500, "stock": 2},
            {"name": "커피 ☕", "price": 800, "stock": 10},
        ],
        "inserted_money": 0,  # 투입된 총 금액
    }

# 사용하기 편하게 변수로 지정
vm = st.session_state.vending_machine

st.title("🥤 오즈의 스마트 자판기")
st.write("원하는 음료를 선택하고 돈을 넣어 구매해 보세요!")
st.markdown("---")

# 3. 레이아웃 나누기 (왼쪽: 음료 목록 및 구매, 오른쪽: 금액 투입 및 잔돈)
col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("💰 금액 투입 및 정산")
    # 현재 투입 금액 표시
    st.metric(label="현재 투입된 금액", value=f"{vm['inserted_money']}원")

    # 현금 투입 버튼들
    st.write("금액을 넣어주세요:")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💵 +500원"):
            vm["inserted_money"] += 500
            st.rerun()
        if st.button("💵 +1000원"):
            vm["inserted_money"] += 1000
            st.rerun()
    with c2:
        if st.button("🪙 +100원"):
            vm["inserted_money"] += 100
            st.rerun()
        if st.button("💳 잔돈 반환"):
            if vm["inserted_money"] > 0:
                st.toast(f"🪙 잔돈 {vm['inserted_money']}원이 반환되었습니다.")
                vm["inserted_money"] = 0
                st.rerun()
            else:
                st.warning("반환할 잔돈이 없습니다.")

with col1:
    st.subheader("🛒 음료수 메뉴판")
    
    # 음료수 목록 반복문으로 출력
    for idx, item in enumerate(vm["음료수"]):
        # 각 음료별로 깔끔하게 구역 나누기
        with st.container(border=True):
            cc1, cc2 = st.columns([2, 1])
            
            with cc1:
                st.markdown(f"### {item['name']}")
                st.write(f"**가격:** {item['price']}원")
                if item["stock"] > 0:
                    st.write(f"**재고:** {item['stock']}개 남음")
                else:
                    st.write("🔴 **품절**")
            
            with cc2:
                st.write("")  # 줄바꿈용 공백
                # 버튼 비활성화 조건 (재고가 없거나, 돈이 부족할 때)
                disabled_condition = item["stock"] <= 0 or vm["inserted_money"] < item["price"]
                
                if st.button(f"구매하기", key=f"buy_{idx}", disabled=disabled_condition):
                    # 구매 로직 처리
                    vm["inserted_money"] -= item["price"]
                    item["stock"] -= 1
                    st.success(f"🎉 {item['name']} 구매 완료!")
                    st.rerun()

st.markdown("---")
# 개발자용 재고 초기화 버튼 (테스트용)
if st.button("🔄 자판기 재고/금액 전체 초기화"):
    del st.session_state.vending_machine
    st.rerun()