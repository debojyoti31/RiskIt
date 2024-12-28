import pandas as pd
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
    st.warning("Please refrain from playing it with real money. It is designed purely for entertainment purposes and does not involve any form of real-money gambling.")

    # Rules expander
    with st.expander("Rules", expanded=False):
        st.markdown("""
        1. **Equal Contribution**: Each player contributes an equal amount of money to the pool.
2. **Risk Factor**: Each player sets a risk factor. **The game rewards the highest risk takers.**
3. **Random Outcome**: In each round, players are randomly assigned as winners or losers based on their risk factors. Lower risk factors increase the chances of winning.
4. **Pool Distribution for Winners**: 
   - The highest risk factor winners divide all the losers' money equally among themselves and also get back their original contribution.
   - Other winners get back their original contribution only.
5. **King Winners**: If there are winners with the highest risk factors whose risk factor surpasses a predefined threshold: 
   - Other winners must give a predefined percentage of their money to the kings.
   - Kings get back their original contribution plus the pool money from losers and the bonus money from other winners.
6. **Company Cut**: A predefined small percentage of money from the losers is taken by the company.
7. **No Winners Scenario**: If no player wins in a round, all players get back their original money minus the company cut as a consolation prize.
        """)

    # Game Settings
    with st.expander("Game Settings", expanded=False):
        initial_contribution = st.number_input("Initial Contribution:", min_value=10.0, max_value=None, value=100.0, step=10.0)
        min_risk_factor = st.slider("Minimum Risk Factor:", min_value=1.0, max_value=99.0, value=30.0, step=0.5)
        max_risk_factor = st.slider("Maximum Risk Factor:", min_value=min_risk_factor, max_value=99.0, value=80.0, step=0.5)
        king_risk_factor = st.slider("King Risk Factor:", min_value=min_risk_factor, max_value=max_risk_factor, value=65.0, step=0.5)
        kings_percent = st.slider("Kings Percent:", min_value=5.0, max_value=90.0, value=10.0, step=1.0)
        company_revenue_percent = st.slider("Company Revenue Percent:", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

    # Initialize or create a new game instance if not already present or if settings have changed
    if 'game' not in st.session_state or st.session_state.game_settings != (initial_contribution, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent):
        reset_game_session(initial_contribution, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent)
        st.session_state.game_settings = (initial_contribution, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent)

    # Display game details as formatted markdown
    st.subheader("Current Game Settings:")
    st.info(f"""
    - **Initial Contribution:** ${initial_contribution:.2f}
    - **Minimum Risk Factor:** {min_risk_factor:.1f}
    - **Maximum Risk Factor:** {max_risk_factor:.1f}
    - **King Risk Factor:** {king_risk_factor:.1f}
    - **Kings Percent:** {kings_percent:.1f}%
    - **Company Revenue Percent:** {company_revenue_percent:.1f}%
    """)

    # Adding players
    st.subheader("Add Players:")
    player_df = st.data_editor(pd.DataFrame( columns = ["Player Name", "Risk_factor"]), num_rows="dynamic", on_change= reset_game_session(initial_contribution, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent))
    for index, row in player_df.iterrows():
        if row["Player Name"] == None:
            player_name = ""
        else:
            player_name = row["Player Name"]
        try:
            risk_factor = float(row["Risk_factor"])
        except (ValueError, TypeError):
            risk_factor = 0.0
        if player_name.strip() == "":
            st.error("Player name cannot be empty.")
        elif player_name in [player.name for player in st.session_state.game.players]:
            st.error(f"Player with the same name,{player_name} already exists.")
        elif not(min_risk_factor <= risk_factor <= max_risk_factor):
            st.error(f"Risk factor of {player_name} must be between {min_risk_factor} and {max_risk_factor}")
        else:
            player = Player(player_name, risk_factor)
            st.session_state.game.add_player(player)

    # Display the list of players in the game
    if not st.session_state.game.players or len(st.session_state.game.players) < 3:
        st.error("Add atleast 3 players to play...")
    else:
        if not len(player_df) == len(st.session_state.game.players):
            st.error ("Not all players could be added, update the players...")
        else:
            st.write(f"Total Pool Amount: {initial_contribution*len(st.session_state.game.players)}")
            if st.button("Play Round", type="primary"):
                st.subheader("Round Results:")
                st.session_state.game.play_round()
                # Display updated player details
                df_players = st.session_state.game.get_player_details()
                st.dataframe(df_players)
                st.write(f"**Company Revenue:** {round(st.session_state.game.get_company_revenue(), 1)}")
        
                # Reset player and company data
                reset_amount() 

if __name__ == "__main__":
    main()
