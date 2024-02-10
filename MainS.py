import streamlit as st
from MultiplayerGame import MultiplayerGame
from Player import Player

def main():
    st.title("RiskIt Multiplayer Game")

    # Sidebar inputs
    st.sidebar.header("Game Settings")
    value = st.sidebar.number_input("Initial Pool Value:", min_value=10.0, max_value=None, value=100.0, step=10.0)
    min_risk_factor = st.sidebar.slider("Minimum Risk Factor:", min_value=50.0, max_value=90.0, value=50.0, step=0.5)
    max_risk_factor = st.sidebar.slider("Maximum Risk Factor:", min_value=min_risk_factor, max_value=99.0, value=95.0, step=0.5)
    king_risk_factor = st.sidebar.slider("King Risk Factor:", min_value=min_risk_factor, max_value=max_risk_factor, value=90.0, step=0.5)
    kings_percent = st.sidebar.slider("Kings Percent:", min_value=5.0, max_value=90.0, value=10.0, step=1.0)
    company_revenue_percent = st.sidebar.slider("Company Revenue Percent:", min_value=0.5, max_value=10.0, value=1.5, step=0.1)

    # Initialize or create a new game instance if not already present
    if 'game' not in st.session_state:
        st.session_state.game = MultiplayerGame(value, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent)

    # Display game details
    st.subheader("Game Details")
    st.write(f"- Initial Pool Value: ${value}")
    st.write(f"- Minimum Risk Factor: {min_risk_factor}")
    st.write(f"- Maximum Risk Factor: {max_risk_factor}")
    st.write(f"- King Risk Factor: {king_risk_factor}")
    st.write(f"- Kings Percent: {kings_percent}%")
    st.write(f"- Company Revenue Percent: {company_revenue_percent}%")

    # Adding players
    with st.form("player_form"):
        st.header("Add Players to Game")
        player_name = st.text_input("Enter player name:")
        risk_factor = st.slider("Enter risk factor:", min_value=min_risk_factor, max_value=max_risk_factor, value=min_risk_factor, step=0.5)
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            player = Player(player_name, risk_factor)
            st.session_state.game.add_player(player)
            st.success(f"Added player {player_name} with risk factor {risk_factor}")

    # Display the list of players in the game
    st.header("Players in the Game")
    player_data = [(player.name, player.risk_factor) for player in st.session_state.game.players]
    if player_data:
        st.table(player_data)
    else:
        st.write("No players added yet.")
    st.write(f"Total Pool Amount: {value*len(st.session_state.game.players)}")

    # Play a round
    if st.button("Play Round"):
        st.subheader("Round Results")
        st.session_state.game.play_round()

        # Display updated player details
        st.write("**Updated Player Details:**")
        df_players = st.session_state.game.get_player_details()
        st.dataframe(df_players)
        st.write(f"**Company Revenue:** {st.session_state.game.get_company_revenue()}")

        # Reset player and company data
        for player in st.session_state.game.players:
            player.set_win(0)
        st.session_state.game.set_company_revenue(0)
        st.session_state.game.set_remaining_pool_value(0)

if __name__ == "__main__":
    main()