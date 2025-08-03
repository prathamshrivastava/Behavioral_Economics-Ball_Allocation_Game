from otree.api import *

doc = """
Public Bad Game with 3 players
"""

class Constants(BaseConstants):
    name_in_url = 'public_bad'
    players_per_group = 3
    num_rounds = 10
    endowment = 9  # Total tokens each player starts with
    private_values = [18, 16, 14, 12, 10, 8, 6, 4, 2]  # Values for private account
    public_contributor_value = 15  # Value gained from own contribution
    public_others_value = -5  # Impact from others' contributions

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    total_public_contribution = models.IntegerField(initial=0)

class Player(BasePlayer):
    # Token allocation
    private_tokens = models.IntegerField(initial=0)  # Tokens placed in private account
    public_tokens = models.IntegerField(initial=0)   # Tokens placed in public account
    
    # Contributions from other players
    p2_contribution = models.IntegerField(initial=0)
    p3_contribution = models.IntegerField(initial=0)
    
    # Earnings
    private_earnings = models.IntegerField(initial=0)  # Earnings from private account
    public_earnings = models.IntegerField(initial=0)   # Earnings from public account
    final_earnings = models.IntegerField(initial=0)    # Total earnings for the round

    cumulative_earnings = models.IntegerField(initial=0)

# PAGES
class Game(Page):
    @staticmethod
    def live_method(player, data):
        if data['type'] == 'update_payoff':
            player.private_tokens = data['tokens_to_private']
            player.public_tokens = data['tokens_to_public']
            player.private_earnings = data['private_payoff']
            player.public_earnings = data['public_payoff']
            return {player.id_in_group: data}
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        group = player.group
        players = group.get_players()
        
        # Calculate total public contribution
        group.total_public_contribution = sum([p.public_tokens for p in players])
        
        # Assign other players' contributions
        p1, p2, p3 = players
        p1.p2_contribution = p2.public_tokens
        p1.p3_contribution = p3.public_tokens
        p2.p2_contribution = p1.public_tokens
        p2.p3_contribution = p3.public_tokens
        p3.p2_contribution = p1.public_tokens
        p3.p3_contribution = p2.public_tokens
        
        # Calculate final earnings for each player
        for p in players:
            p.final_earnings = p.private_earnings + p.public_earnings

class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True

class Results(Page):
    @staticmethod
    def vars_for_template(player):
        # Get all rounds and sort in reverse order (newest first)
        all_rounds = player.in_all_rounds()
        rounds_newest_first = list(reversed(all_rounds))
        
        # Calculate cumulative earnings (starting from the newest round)
        cumulative_earnings = 0
        for round in rounds_newest_first:
            cumulative_earnings += round.final_earnings
            round.cumulative_earnings = cumulative_earnings
        
        return {
            'player': player,
            'all_rounds': rounds_newest_first,  # Pass the reversed list
            'round_number': player.round_number
        }

page_sequence = [Game, ResultsWaitPage, Results]