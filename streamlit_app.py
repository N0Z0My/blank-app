import random
import streamlit as st
import time

# ページ設定
st.set_page_config(
    page_title="ブラックジャック",
    page_icon="🃏",
    layout="centered"
)

# タイトルとルール説明
st.title("🃏 ブラックジャック")
with st.expander("ゲームのルール"):
    st.markdown("""
    1. プレイヤーとディーラーはカードを引いて、合計が21に近づくよう競います。
    2. 合計が21を超えると「バースト」となり、即座に負けとなります。
    3. プレイヤーは「ヒット」でカードを追加するか、「スタンド」で手番を終了するか選べます。
    4. ディーラーは合計が17以上になるまで必ずカードを引き続けます。
    """)

# カードの表示機能
def display_cards(cards, title=""):
    card_symbols = {
        1: "A", 2: "2", 3: "3", 4: "4", 5: "5", 
        6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "J", 12:"Q", 13:"K" 
    }

    if title:
        st.subheader(title)

    cols = st.columns(len(cards))
    for i, card in enumerate(cards):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    border: 2px solid black; 
                    border-radius: 10px; 
                    width: 60px; 
                    height: 90px; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    font-size: 24px;
                    font-weight: bold;
                    background-color: white;
                    color: {'red' if card in [1, 7, 10] else 'black'};
                ">
                    {card_symbols[card]}
                </div>
                """, 
                unsafe_allow_html=True
            )
    st.markdown(f"**合計: {sum([min(v, 10) for v in cards]) }**")

# 初期化
if "players_hand" not in st.session_state:
    st.session_state.players_hand = [random.randint(1, 13)]
    st.session_state.dealer_hand = [random.randint(1, 13)] 
    st.session_state.game_over = False
    st.session_state.message = ""

# 勝敗カウント初期化
for state_var in ["wins", "losses", "draws"]:
    if state_var not in st.session_state:
        st.session_state[state_var] = 0

# スコアボード
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("勝ち", st.session_state.wins)
with col2:
    st.metric("負け", st.session_state.losses)
with col3:
    st.metric("引き分け", st.session_state.draws)

st.divider()

# プレイヤー操作可能ゾーン
if not st.session_state.game_over:
    display_cards(st.session_state.players_hand, "あなたの手札")

    col1, col2 = st.columns(2)
    with col1:
        hit_button = st.button("ヒット", use_container_width=True)
    with col2:
        stand_button = st.button("スタンド", use_container_width=True)

    if hit_button:
        st.session_state.players_hand.append(random.randint(1, 13))
        #st.rerun()

        if sum([min(v, 10) for v in st.session_state.players_hand]) > 21:
            while sum([min(v, 10) for v in st.session_state.dealer_hand]) < 17:
                st.session_state.dealer_hand.append(random.randint(1, 13))

            st.session_state.game_over = True
            st.session_state.message = "バースト！あなたの負けです。"
            st.session_state.losses += 1
            st.error(st.session_state.message)
            # display_cards(st.session_state.players_hand, "あなたの手札")
            time.sleep(1)
        st.rerun()

    if stand_button:
        while sum([min(v, 10) for v in st.session_state.dealer_hand]) < 17:
            st.session_state.dealer_hand.append(random.randint(1, 13))

        st.session_state.game_over = True

        player_sum = sum([min(v, 10) for v in st.session_state.players_hand])
        dealer_sum = sum([min(v, 10) for v in st.session_state.dealer_hand])

        if dealer_sum > 21:
            st.session_state.message = "ディーラーのバースト！あなたの勝ちです。"
            st.session_state.wins += 1
            st.success(st.session_state.message)
        elif player_sum > dealer_sum:
            st.session_state.message = "あなたの勝ちです！"
            st.session_state.wins += 1
            st.success(st.session_state.message)
        elif player_sum < dealer_sum:
            st.session_state.message = "あなたの負けです。"
            st.session_state.losses += 1
            st.error(st.session_state.message)
        else:
            st.session_state.message = "引き分けです。"
            st.session_state.draws += 1
            st.warning(st.session_state.message)

# 結果表示
if st.session_state.game_over:
    display_cards(st.session_state.players_hand, "あなたの手札")
    display_cards(st.session_state.dealer_hand, "ディーラーの手札")

    if st.button("新しいゲームを開始", use_container_width=True):
        st.session_state.players_hand = [random.randint(1, 13)]
        st.session_state.dealer_hand = [random.randint(1, 13)]
        st.session_state.game_over = False
        st.session_state.message = ""
        st.rerun()
