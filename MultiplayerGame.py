import random
import pandas as pd
import time

class MultiplayerGame:
    def __init__(self, value, min_risk_factor, max_risk_factor, king_risk_factor, kings_percent, company_revenue_percent):
        self.value = value
        self.min_risk_factor = min_risk_factor
        self.max_risk_factor = max_risk_factor
        self.king_risk_factor = king_risk_factor
        self.kings_percent = kings_percent

        self.players = []
        self.company_revenue = 0
        self.remaining_pool_value = 0
        self.return_amount = (100 - company_revenue_percent) / 100.0 * value

    def add_player(self, player):
         self.players.append(player)


    def play_round(self):

        winners = []
        losers = []

        for player in self.players:
         
            random.seed(time.time())
            win_probability = random.random()  # Random number between 0 and 1
            if win_probability * 100.0 > player.get_risk_factor():
                winners.append(player)
            else:
                losers.append(player)
                self.remaining_pool_value += self.return_amount
                self.company_revenue += self.value - self.return_amount

        if winners:
            highest_risk_factor = max([player.get_risk_factor() for player in winners])
            highest_risk_count = sum(1 for player in winners if player.get_risk_factor() == highest_risk_factor)

            if highest_risk_factor < self.king_risk_factor:
                for player in winners:
                    if player.get_risk_factor() < highest_risk_factor:
                        player.set_win(self.value)
                    else:
                        player_winnings = self.value + (self.remaining_pool_value / highest_risk_count)
                        player.set_win(player_winnings)
            else:
                bonus = 0
                kings = []
                for player in winners:
                    if player.get_risk_factor() < highest_risk_factor:
                        player_winnings = (100 - self.kings_percent) / 100.0 * self.value
                        bonus += self.value - player_winnings
                        player.set_win(player_winnings)
                    else:
                        kings.append(player)

                for player in kings:
                    player_winnings = self.value + ((self.remaining_pool_value + bonus) / highest_risk_count)
                    player.set_win(player_winnings)

        else:
            for player in losers:
                player.set_win(self.return_amount)


    def get_player_details(self):
        player_data = []
        for player in self.players:
            player_data.append({
                "Name": player.get_name(),
                "Risk Factor": player.get_risk_factor(),
                "Win": player.get_win()
            })
        return pd.DataFrame(player_data)


    def get_company_revenue(self):
        return self.company_revenue

    def set_company_revenue(self, company_revenue):
         self.company_revenue = company_revenue

    def set_remaining_pool_value(self, remaining_pool_value):
         self.remaining_pool_value = remaining_pool_value