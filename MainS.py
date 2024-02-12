
import streamlit as st
from MultiplayerGame import MultiplayerGame
from Player import Player

def reset_game_session(value, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent):
    st.session_state.game = MultiplayerGame(value, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent)

def reset_amount():
    for player in st.session_state.game.players:
        player.set_win(0)
    st.session_state.game.set_company_revenue(0)
    st.session_state.game.set_remaining_pool_value(0)


def main():
    st.title("RiskIt Multiplayer Game")

    # Rules expander
    with st.expander("Rules", expanded=False):
        st.markdown("""
        1. **Equal Contribution**: Each player contributes an equal amount of money to the pool. Let's say each player contributes $10.
        2. **Risk Factor**: Each player sets a risk factor. Higher risk factors imply lower chances of winning.
        3. **Random Outcome**: In each round, players are randomly assigned as winners or losers based on their risk factors. Higher risk factors decrease the chances of winning.
        4. **Company Cut**: A predefined small percentage of money from the losers is taken by the company, and the remaining money from losers is returned to the pool.
        5. **Pool Distribution for Winners**:
           - The highest risk factor winners divide the pool money equally among themselves and also get back their original contribution.
           - Other winners get back their original contribution only.
        6. **King Winners**: If there are winners with the highest risk factors whose risk factor surpasses a predefined threshold (very big risk):
           - Other winners (non-kings) must give a predefined percentage of their money to the kings.
           - Kings get back their original contribution plus the pool money from losers and the bonus money from other winners.
        7. **No Winners Scenario**: If no player wins in a round, all players get back their original money minus the company cut (as they all are losers) as a consolation prize.
        """)

    # Sidebar inputs
    st.sidebar.header("Game Settings")
    initial_contribution = st.sidebar.number_input("Initial Contribution:", min_value=10.0, max_value=None, value=100.0, step=10.0)
    min_risk_factor = st.sidebar.slider("Minimum Risk Factor:", min_value=1.0, max_value=99.0, value=30.0, step=0.5)
    max_risk_factor = st.sidebar.slider("Maximum Risk Factor:", min_value=min_risk_factor, max_value=99.0, value=80.0, step=0.5)
    king_risk_factor = st.sidebar.slider("King Risk Factor:", min_value=min_risk_factor, max_value=max_risk_factor, value=65.0, step=0.5)
    kings_percent = st.sidebar.slider("Kings Percent:", min_value=5.0, max_value=90.0, value=10.0, step=1.0)
    company_revenue_percent = st.sidebar.slider("Company Revenue Percent:", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

    # Initialize or create a new game instance if not already present or if settings have changed
    if 'game' not in st.session_state or st.session_state.game_settings != (initial_contribution, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent):
        reset_game_session(initial_contribution, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent)
        st.session_state.game_settings = (initial_contribution, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent)

    # Display game details as formatted markdown
    st.subheader("Game Details")
    st.markdown(f"""
    - **Initial Contribution:** ${initial_contribution:.2f}
    - **Minimum Risk Factor:** {min_risk_factor:.1f}
    - **Maximum Risk Factor:** {max_risk_factor:.1f}
    - **King Risk Factor:** {king_risk_factor:.1f}
    - **Kings Percent:** {kings_percent:.1f}%
    - **Company Revenue Percent:** {company_revenue_percent:.1f}%
    """)

    # Adding players
    with st.form("player_form"):
        st.header("Add Players to Game")
        player_name = st.text_input("Enter player name:")
        risk_factor = st.slider("Enter risk factor:", min_value=min_risk_factor, max_value=max_risk_factor, value=min_risk_factor, step=0.5)
        submitted = st.form_submit_button("Submit")

        if submitted:
            if player_name.strip() == "":
                st.error("Player name cannot be empty.")
            elif player_name in [player.name for player in st.session_state.game.players]:
                st.error("Player with the same name already exists.")
            else:
                player = Player(player_name, risk_factor)
                st.session_state.game.add_player(player)
                st.success(f"Added player {player_name} with risk factor {risk_factor}")

    # Display the list of players in the game
    st.header("Players in the Game")
    player_data = [(player.name, player.risk_factor) for player in st.session_state.game.players]
    if player_data:
        st.table(player_data)
        st.write(f"Total Pool Amount: {initial_contribution*len(st.session_state.game.players)}")

    # Play a round
    if len(player_data) > 2:
        if st.button("Play Round"):
            st.subheader("Round Results")
            st.session_state.game.play_round()
    
            # Display updated player details
            st.write("**Updated Player Details:**")
            df_players = st.session_state.game.get_player_details()
            st.dataframe(df_players)
            st.write(f"**Company Revenue:** {st.session_state.game.get_company_revenue()}")
    
            # Reset player and company data
            reset_amount()
    else:
        st.error("Add atleast 3 players to play...")

if __name__ == "__main__":
    main()
