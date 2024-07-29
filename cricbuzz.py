import random
from enum import Enum
from abc import ABC, abstractmethod
from collections import deque, defaultdict

class BallDetails: 
    def __init__(self, ball_number):
        self.ball_number = ball_number
        self.ball_type = None
        self.run_type = None
        self.played_by = None
        self.bowled_by = None
        self.wicket = None
        self.score_updater_observer_list = [BowlingScoreUpdater(), BattingScoreUpdater()]

    def start_ball_delivery(self, batting_team, bowling_team, over):
        self.played_by = batting_team.get_striker()
        self.bowled_by = over.bowled_by
        self.ball_type = BallType.NORMAL

        if self.is_wicket_taken():
            self.run_type = RunType.ZERO
            self.wicket = Wicket(WicketType.BOLD, bowling_team.get_current_bowler(), over, self)
            batting_team.set_striker(None)
        else:
            self.run_type = self.get_run_type()

            if self.run_type in {RunType.ONE, RunType.THREE}:
                temp = batting_team.get_striker()
                batting_team.set_striker(batting_team.get_non_striker())
                batting_team.set_non_striker(temp)

        self.notify_updaters()

    def notify_updaters(self):
        for observer in self.score_updater_observer_list:
            observer.update(self)

    def get_run_type(self):
        val = random.random()
        if val <= 0.2:
            return RunType.ONE
        elif 0.2 < val <= 0.4:
            return RunType.TWO
        elif 0.4 < val <= 0.6:
            return RunType.THREE
        elif 0.6 < val <= 0.8:
            return RunType.FOUR
        else:
            return RunType.SIX

    def is_wicket_taken(self):
        return random.random() < 0.2

class BallType(Enum):
    NORMAL = "NORMAL"
    WIDEBALL = "WIDEBALL"
    NOBALL = "NOBALL"

class InningDetails:
    def __init__(self, batting_team, bowling_team, match_type):
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.match_type = match_type
        self.overs = []

    def start(self, runs_to_win):
        try:
            self.batting_team.choose_next_batsman()
            self.batting_team.choose_next_batsman()  # Set both striker and non-striker
        except Exception as e:
            pass

        no_of_overs = self.match_type.no_of_overs()
        for over_number in range(1, no_of_overs + 1):
            self.bowling_team.choose_next_bowler(self.match_type.max_over_count_bowlers())

            over = OverDetails(over_number, self.bowling_team.get_current_bowler())
            self.overs.append(over)
            try:
                won = over.start_over(self.batting_team, self.bowling_team, runs_to_win)
                if won:
                    break
            except Exception as e:
                break

            temp = self.batting_team.get_striker()
            self.batting_team.set_striker(self.batting_team.get_non_striker())
            self.batting_team.set_non_striker(temp)

    def get_total_runs(self):
        return self.batting_team.get_total_runs()

    def print_batting_score_card(self):
        print(f"{self.batting_team.name} Batting Score Card:")
        for player in self.batting_team.players:
            score_card = player.batting_score_card
            if score_card.total_balls_played > 0:
                print(f"Player: {player.name}, Runs: {score_card.total_runs}, Balls: {score_card.total_balls_played}, "
                      f"Fours: {score_card.total_fours}, Sixes: {score_card.total_six}, Strike Rate: {score_card.strike_rate:.2f}")
        print()

    def print_bowling_score_card(self):
        print(f"{self.bowling_team.name} Bowling Score Card:")
        for player in self.bowling_team.players:
            score_card = player.bowling_score_card
            if score_card.total_overs_count > 0 or score_card.runs_given > 0 or score_card.wickets_taken > 0:
                print(f"Player: {player.name}, Overs: {score_card.total_overs_count}, Runs: {score_card.runs_given}, "
                      f"Wickets: {score_card.wickets_taken}, No Balls: {score_card.no_ball_count}, Wide Balls: {score_card.wide_ball_count}, "
                      f"Economy Rate: {score_card.economy_rate:.2f}")
        print()

class OverDetails:
    def __init__(self, over_number, bowled_by):
        self.over_number = over_number
        self.balls = []
        self.extra_balls_count = 0
        self.bowled_by = bowled_by

    def start_over(self, batting_team, bowling_team, runs_to_win):
        ball_count = 1
        while ball_count <= 6:
            ball = BallDetails(ball_count)
            ball.start_ball_delivery(batting_team, bowling_team, self)
            
            if ball.ball_type == BallType.NORMAL:
                self.balls.append(ball)
                ball_count += 1
                if ball.wicket is not None:
                    try:
                        batting_team.choose_next_batsman()
                    except IndexError:
                        return False

                if runs_to_win != -1 and batting_team.get_total_runs() >= runs_to_win:
                    batting_team.is_winner = True
                    return True
            else:
                self.extra_balls_count += 1

        return False

class RunType(Enum):
    ZERO = 'ZERO'
    ONE = 'ONE'
    TWO = 'TWO'
    THREE = 'THREE'
    FOUR = 'FOUR'
    SIX = 'SIX'

class ScoreUpdaterObserver(ABC):
    @abstractmethod
    def update(self, ball_details):
        pass

class BattingScoreUpdater(ScoreUpdaterObserver):
    def update(self, ball_details):
        run = 0

        if RunType.ONE == ball_details.run_type:
            run = 1
        elif RunType.TWO == ball_details.run_type:
            run = 2
        elif RunType.THREE == ball_details.run_type:
            run = 3
        elif RunType.FOUR == ball_details.run_type:
            run = 4
            ball_details.played_by.batting_score_card.total_fours += 1
        elif RunType.SIX == ball_details.run_type:
            run = 6
            ball_details.played_by.batting_score_card.total_six += 1
        
        ball_details.played_by.batting_score_card.total_runs += run
        ball_details.played_by.batting_score_card.total_balls_played += 1
        ball_details.played_by.batting_score_card.strike_rate = (ball_details.played_by.batting_score_card.total_runs / ball_details.played_by.batting_score_card.total_balls_played) * 100

        if ball_details.wicket:
            ball_details.played_by.batting_score_card.wicket_detail = ball_details.wicket
    
class BowlingScoreUpdater(ScoreUpdaterObserver):
    def update(self, ball_details):
        if ball_details.ball_number == 6 and ball_details.ball_type == BallType.NORMAL:
            ball_details.bowled_by.bowling_score_card.total_overs_count += 1

        if RunType.ONE == ball_details.run_type:
            ball_details.bowled_by.bowling_score_card.runs_given += 1
        elif RunType.TWO == ball_details.run_type:
            ball_details.bowled_by.bowling_score_card.runs_given += 2
        elif RunType.THREE == ball_details.run_type:
            ball_details.bowled_by.bowling_score_card.runs_given += 3
        elif RunType.FOUR == ball_details.run_type:
            ball_details.bowled_by.bowling_score_card.runs_given += 4
        elif RunType.SIX == ball_details.run_type:
            ball_details.bowled_by.bowling_score_card.runs_given += 6

        if ball_details.wicket:
            ball_details.bowled_by.bowling_score_card.wickets_taken += 1

        if ball_details.ball_type == BallType.NOBALL:
            ball_details.bowled_by.bowling_score_card.no_ball_count += 1

        if ball_details.ball_type == BallType.WIDEBALL:
            ball_details.bowled_by.bowling_score_card.wide_ball_count += 1

        if ball_details.bowled_by.bowling_score_card.total_overs_count > 0:
            ball_details.bowled_by.bowling_score_card.economy_rate = ball_details.bowled_by.bowling_score_card.runs_given / ball_details.bowled_by.bowling_score_card.total_overs_count

class BattingScoreCard:
    def __init__(self):
        self.total_runs = 0
        self.total_balls_played = 0
        self.total_fours = 0
        self.total_six = 0
        self.strike_rate = 0.0
        self.wicket_detail = None

class BowlingScoreCard:
    def __init__(self):
        self.total_overs_count = 0
        self.runs_given = 0
        self.wickets_taken = 0
        self.no_ball_count = 0
        self.wide_ball_count = 0
        self.economy_rate = 0.0

class PlayerDetails:
    def __init__(self, name):
        self.name = name
        self.batting_score_card = BattingScoreCard()
        self.bowling_score_card = BowlingScoreCard()

class PlayerBattingController:
    def __init__(self, players):
        self.players = players
        self.striker = None
        self.non_striker = None
        self.out_players = []

    def get_next_player(self):
        if not self.players:
            raise IndexError("No players left to bat")
        if self.striker is None:
            self.striker = self.players.pop(0)
        elif self.non_striker is None:
            self.non_striker = self.players.pop(0)
        else:
            self.out_players.append(self.striker)
            self.striker = self.players.pop(0)

    def get_striker(self):
        return self.striker

    def set_striker(self, player):
        self.striker = player

    def get_non_striker(self):
        return self.non_striker

    def set_non_striker(self, player):
        self.non_striker = player

class PlayerBowlingController:
    def __init__(self, players):
        self.players = deque(players)
        self.current_bowler = None
        self.bowler_over_count = defaultdict(int)

    def get_next_bowler(self, max_over_count_per_bowler):
        while self.bowler_over_count[self.players[0]] >= max_over_count_per_bowler:
            self.players.rotate(-1)
        
        self.current_bowler = self.players[0]
        self.bowler_over_count[self.current_bowler] += 1

    def get_current_bowler(self):
        return self.current_bowler

class TeamDetails:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.player_batting_controller = PlayerBattingController(players.copy())
        self.player_bowling_controller = PlayerBowlingController(players.copy())
        self.is_winner = False

    def choose_next_batsman(self):
        self.player_batting_controller.get_next_player()

    def choose_next_bowler(self, max_over_count_per_bowler):
        self.player_bowling_controller.get_next_bowler(max_over_count_per_bowler)

    def get_current_bowler(self):
        return self.player_bowling_controller.get_current_bowler()

    def get_striker(self):
        return self.player_batting_controller.get_striker()

    def set_striker(self, player_details):
        self.player_batting_controller.set_striker(player_details)

    def get_non_striker(self):
        return self.player_batting_controller.get_non_striker()

    def set_non_striker(self, player_details):
        self.player_batting_controller.set_non_striker(player_details)

    def get_total_runs(self):
        total_runs = 0
        for player in self.players:
            total_runs += player.batting_score_card.total_runs
        return total_runs

class Wicket:
    def __init__(self, wicket_type, taken_by, over, ball):
        self.wicket_type = wicket_type
        self.taken_by = taken_by
        self.over = over
        self.ball = ball

class WicketType(Enum):
    BOLD = 'BOLD'

class MatchType(ABC):
    @abstractmethod
    def no_of_overs(self):
        pass

    @abstractmethod
    def max_over_count_bowlers(self):
        pass

class ODI(MatchType):
    def no_of_overs(self):
        return 50

    def max_over_count_bowlers(self):
        return 10

class T20(MatchType):
    def no_of_overs(self):
        return 20

    def max_over_count_bowlers(self):
        return 4

def main():
    # Create players
    players_team1 = [PlayerDetails(f"Player1_{i+1}") for i in range(11)]
    players_team2 = [PlayerDetails(f"Player2_{i+1}") for i in range(11)]

    # Create teams
    team1 = TeamDetails("Team 1", players_team1)
    team2 = TeamDetails("Team 2", players_team2)

    # Choose match type
    match_type = T20()

    # Create innings
    inning1 = InningDetails(team1, team2, match_type)
    inning2 = InningDetails(team2, team1, match_type)

    # Start first inning
    inning1.start(runs_to_win=-1)
    print(f"Team 1 scored: {inning1.get_total_runs()} runs")
    inning1.print_batting_score_card()
    inning1.print_bowling_score_card()

    # Start second inning
    inning2.start(runs_to_win=inning1.get_total_runs())
    print(f"Team 2 scored: {inning2.get_total_runs()} runs")
    inning2.print_batting_score_card()
    inning2.print_bowling_score_card()

    # Determine winner
    if inning1.get_total_runs() > inning2.get_total_runs():
        print("Team 1 wins")
    elif inning1.get_total_runs() < inning2.get_total_runs():
        print("Team 2 wins")
    else:
        print("Match is a draw")

if __name__ == "__main__":
    main()
