import random
import streamlit as st

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
    5. J, Q, Kは10として扱い、Aは11として扱います。
    """)

# カードの表示機能
def display_cards(cards, title=""):
    # カードの見た目を表示
    card_symbols = {
        1: "A", 2: "2", 3: "3", 4: "4", 5: "5", 
        6: "6", 7: "7", 8: "8", 9: "9", 10: "10"
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
    st.markdown(f"**合計: {sum(cards)}**")

# 初期化
if "players_hand" not in st.session_state:
    st.session_state.players_hand = [random.randint(1, 10)]
    st.session_state.game_over = False
    st.session_state.message = ""

# 勝敗カウント用の変数を初期化
for state_var in ["wins", "losses", "draws"]:
    if state_var not in st.session_state:
        st.session_state[state_var] = 0

# スコアボードの表示
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("勝ち", st.session_state.wins, delta=None)
with col2:
    st.metric("負け", st.session_state.losses, delta=None)
with col3:
    st.metric("引き分け", st.session_state.draws, delta=None)

st.divider()

# 合計が21を超えていない間、操作可能
if not st.session_state.game_over:
    display_cards(st.session_state.players_hand, "あなたの手札")
    
    col1, col2 = st.columns(2)
    with col1:
        hit_button = st.button("ヒット", key="hit", use_container_width=True)
    with col2:
        stand_button = st.button("スタンド", key="stand", use_container_width=True)
    
    if hit_button:
        # カードを追加
        st.session_state.players_hand.append(random.randint(1, 10))
        st.balloons()
        
        # 合計が21を超えたらゲームオーバー
        if sum(st.session_state.players_hand) > 21:
            st.session_state.game_over = True
            st.session_state.message = "バースト！あなたの負けです。"
            st.session_state.losses += 1
            st.error(st.session_state.message)
            
    if stand_button:
        # ディーラーの手札
        dealer_hand = [random.randint(1, 10)]
        while sum(dealer_hand) < 17:
            dealer_hand.append(random.randint(1, 10))
            
        st.session_state.dealer_hand = dealer_hand
        st.session_state.game_over = True
        
        # 結果判定
        player_sum = sum(st.session_state.players_hand)
        dealer_sum = sum(dealer_hand)
        
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

# ゲームオーバー時の表示
if st.session_state.game_over:
    # プレイヤーとディーラーの手札を表示
    display_cards(st.session_state.players_hand, "あなたの手札")
    
    if hasattr(st.session_state, 'dealer_hand'):
        display_cards(st.session_state.dealer_hand, "ディーラーの手札")
    
    # 新しいゲームを開始するボタン
    if st.button("新しいゲームを開始", use_container_width=True):
        st.session_state.players_hand = [random.randint(1, 10)]
        st.session_state.game_over = False
        st.session_state.message = ""
        if hasattr(st.session_state, 'dealer_hand'):
            del st.session_state.dealer_hand
        st.rerun()