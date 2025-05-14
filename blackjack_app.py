import random
import blackjack_app as st

# 初期化
if "players_hand" not in st.session_state:
    st.session_state.players_hand = [random.randint(1, 10)]
    st.session_state.game_over = False
    st.session_state.message = ""

# 合計が21を超えていない間、操作可能
if not st.session_state.game_over:
    st.write(f"現在の手札: {st.session_state.players_hand}")
    st.write(f"合計: {sum(st.session_state.players_hand)}")

    action = st.radio("次の行動を選択してください", ("ヒット", "スタンド"))

    if st.button("実行"):
        if action == "ヒット":
            new_card = random.randint(1, 10)
            st.session_state.players_hand.append(new_card)
            if sum(st.session_state.players_hand) > 21:
                st.session_state.message = "バーストしました！"
                st.session_state.game_over = True
        elif action == "スタンド":
            st.session_state.message = "スタンドしました！"
            st.session_state.game_over = True

# ゲーム終了時のメッセージ
if st.session_state.game_over:
    st.write(st.session_state.message)
    st.write(f"最終的な手札: {st.session_state.players_hand}")
    st.write(f"合計: {sum(st.session_state.players_hand)}")
    if st.button("リスタート"):
        st.session_state.players_hand = [random.randint(1, 10)]
        st.session_state.game_over = False
        st.session_state.message = ""
