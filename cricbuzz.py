import random

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
        # THROW BALL AND GET THE BALL TYPE, assuming here that ball type is always NORMAL
        self.ball_type = BallType.NORMAL

        # wicket or no wicket
        if self.is_wicket_taken():
            self.run_type = RunType.ZERO
            # considering only BOLD
            self.wicket = Wicket(WicketType.BOLD, bowling_team.get_current_bowler(), over, self)
            # making only striker out for now
            batting_team.set_striker(None)
        else:
            self.run_type = self.get_run_type()

            if self.run_type in {RunType.ONE, RunType.THREE}:
                # swap striker and non-striker
                temp = batting_team.get_striker()
                batting_team.set_striker(batting_team.get_non_striker())
                batting_team.set_non_striker(temp)

        # update player scoreboard
        self.notify_updaters(self)

    def notify_updaters(self, ball_details):
        for observer in self.score_updater_observer_list:
            observer.update(ball_details)

    def get_run_type(self):
        val = random.random()
        if val <= 0.2:
            return RunType.ONE
        elif 0.3 <= val <= 0.5:
            return RunType.TWO
        elif 0.6 <= val <= 0.8:
            return RunType.FOUR
        else:
            return RunType.SIX

    def is_wicket_taken(self):
        # random function return value between 0 and 1
        return random.random() < 0.2

from enum import Enum
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
        # Set batting players
        try:
            self.batting_team.choose_next_batsman()
        except Exception as e:
            pass

        no_of_overs = self.match_type.no_of_overs()
        for over_number in range(1, no_of_overs + 1):
            # Choose bowler
            self.bowling_team.choose_next_bowler(self.match_type.max_over_count_bowlers())

            over = OverDetails(over_number, self.bowling_team.get_current_bowler())
            self.overs.append(over)
            try:
                won = over.start_over(self.batting_team, self.bowling_team, runs_to_win)
                if won:
                    break
            except Exception as e:
                break

            # Swap striker and non-striker
            temp = self.batting_team.get_striker()
            self.batting_team.set_striker(self.batting_team.get_non_striker())
            self.batting_team.set_non_striker(temp)

    def get_total_runs(self):
        return self.batting_team.get_total_runs()

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
                    batting_team.choose_next_batsman()

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

from abc import ABC, abstractmethod

class ScoreUpdaterObserver(ABC):
    def update(self, ball_details):
        pass

class BattingScoreUpdater(ScoreUpdaterObserver):
    def update(self, ball_details):
        run = 0

        if RunType.ONE == ball_details.run_type:
            run = 1
        elif RunType.TWO == ball_details.run_type:
            run = 2
        elif RunType.FOUR == ball_details.run_type:
            run = 4
            ball_details.played_by.batting_score_card.total_fours += 1
        elif RunType.SIX == ball_details.run_type:
            run = 6
            ball_details.played_by.batting_score_card.total_six += 1
        
        ball_details.played_by.batting_score_card.total_runs += run
        ball_details.played_by.batting_score_card.total_balls_played += 1

        if ball_details.wicket:
            ball_details.played_by.batting_score_card.wicket_details = ball_details.wicket
    
class BowlingScoreUpdater(ScoreUpdaterObserver):
    def update(self, ball_details):
        if ball_details.ball_number == 6 and ball_details.ball_type == BallType.NORMAL:
            ball_details.bowled_by.bowling_score_card.totalOversCount += 1

        if RunType.ONE == ball_details.run_type:
            ball_details.bowled_by.bowling_score_card.runs_giving += 1
        elif RunType.TWO == ball_details.run_type:
            ball_details.bowled_by.bowling_score_card.runs_giving += 2
        elif RunType.FOUR == ball_details.run_type:
            ball_details.bowled_by.bowling_score_card.runs_giving += 4
        elif RunType.SIX == ball_details.run_type:
            ball_details.bowled_by.bowling_score_card.runs_giving += 6

        if ball_details.wicket:
            ball_details.bowled_by.bowling_score_card.wickets_taken += 1

        if ball_details.ball_type == BallType.NOBALL:
            ball_details.bowled_by.bowling_score_card.no_ball_count += 1

        if ball_details.ball_type == BallType.WIDEBALL:
            ball_details.bowled_by.bowling_score_card.wide_ball_count += 1

class BattingScoreCard:
    total_runs = 0
    total_balls_played = 0
    total_fours = 0
    total_six = 0
    strike_rate = 0.0
    wicket_detail = None

class BowlingScoreCard:
    total_overs_count = 0
    runs_given = 0
    wickets_taken = 0
    no_ball_count = 0
    wide_ball_count = 0
    economy_rate = 0.0

class Person:
    name = None
    age = 0
    address = None

from collections import deque
class PlayerBattingController:
    yet_to_play = None
    striker = None
    non_striker = None

    def __init__(self, playing11):
        self.yet_to_play = deque()
        self.yet_to_play.extend(playing11)

    def get_next_player(self):
        if self.yet_to_play.is_empty():
            raise Exception()

        if not striker:
            striker = self.yet_to_play.poll()

        if not self.non_striker:
            self.non_striker = self.yet_to_play.poll()
    
    def get_striker(self):
        return self.striker

    def get_non_striker(self):
        return self.non_striker

    def set_striker(self, player_details):
        self.striker = player_details

    def set_non_striker(self, player_details):
        self.non_striker = player_details

from collections import defaultdict
class PlayerBowlingController:
    bowlers_list = None
    bowler_vs_over_count = None
    current_bowler = None

    def __init__(self, bowlers):
        self.set_bowlers_list(bowlers)

    def set_bowlers_list(self, bowlers_list):
        self.bowlers_list = deque()
        self.bowler_vs_over_count = defaultdict(int)
        for bowler in bowlers_list:
            self.bowlers_list.append(bowler)
            self.bowler_vs_over_count[bowler] = 0

    def get_next_bowler(self, max_over_count_per_bowler):
        player_details = self.bowlers_list.poll()
        if self.bowler_vs_over_count[player_details] + 1 == max_over_count_per_bowler:
            self.current_bowler = player_details
        else:
            self.current_bowler = player_details
            self.bowlers_list.append(player_details)
            self.bowler_vs_over_count[player_details] += 1
        
    def get_current_bowler(self):
        return self.current_bowler

class PlayerDetails:
    person = None
    player_type = None
    batting_score_card = None
    bowling_score_card = None

    def __init__(self, person, player_type):
        self.person = person
        self.player_type = player_type
        self.batting_score_card = BattingScoreCard()
        self.bowling_score_card = BowlingScoreCard()

    def print_batting_score_card(self):
        print("PlayerName: ", self.person.name, " -- totalRuns: ", self.batting_score_card.total_runs, " -- totalBallsPlayed: ", self.bowlingScoreCard.total_balls_played, " -- 4s: ", self.batting_score_card.total_fours, " -- 6s: ", self.batting_score_card.totalSix, " -- outby: ", end='')

        if self.batting_score_card.wicket_details:
            print(self.batting_score_card.wicket_details.taken_by.person.name)
        else:
            print("notout")


    def print_bowling_score_card(self):
        print("PlayerName: ", self.person.name, " -- totalOversThrown: ", self.bowling_score_card.total_overs_count, " -- totalRunsGiven: ", self.bowling_score_card.runs_given, " -- WicketsTaken: ", self.bowling_score_card.wickets_taken)

class PlayerType(Enum):
    BATSMAN = 'BATSMAN'
    BOWLER = "BOWLER"
    WICKETKEEPER = "WICKETKEEPER"
    CAPTAIN = "CAPTAIN"
    ALLROUNDER = "ALLROUNDER"

class Team:
    team_name = None
    playing11 = deque()
    bench = None
    batting_controller = None
    bowling_controller = None
    is_winner = False

    def __init__(self, teamName, playing11, bench, bowlers):
        self.team_name = teamName
        self.playing11 = playing11
        self.bench = bench
        self.batting_controller = PlayerBattingController(playing11)
        self.bowling_controller = PlayerBowlingController(bowlers)
    
    def get_team_name(self):
        return self.team_name

    def choose_next_batsman(self):
        self.batting_controller.get_next_player()

    def chooseNextBowler(self, max_over_count_per_bowler):
        self.bowling_controller.get_next_bowler(max_over_count_per_bowler)

    def getStriker(self):
        return self.batting_controller.get_striker()

    def get_non_striker(self):
        return self.batting_controller.get_non_striker()

    def set_striker(self, player):
        self.battingController.setStriker(player)

    def set_non_striker(self, player):
        self.batting_controller.set_non_striker(player)

    def get_current_bowler(self):
        return self.bowling_controller.get_current_bowler()

    def print_batting_score_card(self):
        for self.player_details in self.playing11:
            self.player_details.print_batting_score_card()

    def print_bowling_score_card(self):
        for self.player_details in self.playing11:
            if(self.player_details.bowling_score_card.total_overs_count > 0):
                self.player_details.print_bowling_score_card()

    def get_total_runs(self):
        total_run = 0
        for player in self.playing11:
            total_run += player.batting_score_card.total_runs
        
        return total_run

class Wicket:
    wicket_type = None
    taken_by = None
    over_detail = None
    ball_detail = None

    def __init__(self, wicket_type, taken_by, over_detail, ball_detail):
        self.wicket_type = wicket_type
        self.taken_by = taken_by
        self.over_detail = over_detail
        self.ball_detail = ball_detail

class WicketType(Enum):
    RUNOUT = 'RUNOUT'
    BOLD = 'BOLD'
    CATCH = 'CATCH'

import random
class Match:
    team_A = None
    team_B = None
    match_date = None
    venue = None
    toss_winner = None
    innings = None
    match_type = None

    def __init__(self, team_A, team_B, match_date, venue, match_type):
        self.team_A = team_A
        self.team_B = team_B
        self.match_date = match_date
        self.venue = venue
        self.match_type = match_type
        innings = []

    def start_match(self):
        # 1. Toss
        toss_winner = self.toss(self.team_A, self.team_B)

        # start The Inning, there are 2 innings in a match
        for inning in range(3):
            # assuming here that tossWinner batFirst
            is_chasing = False
            if inning == 1:
                battingTeam = toss_winner
                bowlingTeam = None
                if toss_winner.get_team_name() == self.team_A.get_team_name():
                    bowlingTeam = self.team_B
                else:
                    bowlingTeam = self.team_A
                inningDetails = InningDetails(battingTeam, bowlingTeam, self.match_type)
                inningDetails.start(-1)
            else:
                bowlingTeam = self.toss_winner
                battingTeam = None
                if toss_winner.get_team_name() == self.team_A.get_team_name():
                    battingTeam = self.team_B
                else:
                    battingTeam = self.team_A
                inning_details = InningDetails(battingTeam, bowlingTeam, self.match_type)
                inning_details.start(self.innings[0].get_total_runs())
                if bowlingTeam.getTotalRuns() > battingTeam.get_total_runs():
                    bowlingTeam.isWinner = True

            self.innings[inning-1] = inningDetails

            # print inning details
            print()
            print("INNING ", inning, " -- total Run: ", battingTeam.getTotalRuns())
            print("---Batting ScoreCard : ", battingTeam.teamName + "---")

            battingTeam.print_batting_score_card()

            print()
            print("---Bowling ScoreCard : " + bowlingTeam.teamName + "---")
            bowlingTeam.print_bowling_score_card()

        print()
        if self.team_A.is_winner:
            print("---WINNER---" + self.team_A.teamName)

        else:
            print("---WINNER---" + self.team_B.teamName)

    def toss(self, team_A, team_B):
        # random function return value between 0 and 1
        if random.uniform(0, 1) < 0.5:
            return team_A
        else:
            return team_B
    
class MatchType(ABC):
    @abstractmethod
    def no_of_overs(self):
        pass

    @abstractmethod
    def max_over_count_bowlers(self):
        pass

class OneDayMatchType(MatchType):
    def no_of_overs(self):
        return 50

    def max_over_count_bowlers(self):
        return 10

class T20MatchType(MatchType):
    def no_of_overs(self):
        return 20

    def max_over_count_bowlers(self):
        return 5

class Main:
    def main(self):
        ob = Main()

        team_A = ob.add_team("India")
        team_B = ob.add_team("SriLanka")

        match_type = T20MatchType()
        match = Match(team_A, team_B, None, "SMS STADIUM", match_type)
        match.start_match()

    def add_team(self, name):
        player_details = []

        p1 = self.add_player(name+"1", PlayerType.ALLROUNDER)
        p2 = self.add_player(name+"2", PlayerType.ALLROUNDER)
        p3 = self.add_player(name+"3", PlayerType.ALLROUNDER)
        p4 = self.add_player(name+"4", PlayerType.ALLROUNDER)
        p5 = self.add_player(name+"5", PlayerType.ALLROUNDER)
        p6 = self.add_player(name+"6", PlayerType.ALLROUNDER)
        p7 = self.add_player(name+"7", PlayerType.ALLROUNDER)
        p8 = self.add_player(name+"8", PlayerType.ALLROUNDER)
        p9 = self.add_player(name+"9", PlayerType.ALLROUNDER)
        p10 = self.add_player(name+"10", PlayerType.ALLROUNDER)
        p11 = self.add_player(name+"11", PlayerType.ALLROUNDER)
        
        player_details.append(p1)
        player_details.append(p2)
        player_details.append(p3)
        player_details.append(p4)
        player_details.append(p5)
        player_details.append(p6)
        player_details.append(p7)
        player_details.append(p8)
        player_details.append(p9)
        player_details.append(p10)
        player_details.append(p11)

        bowlers = []
        bowlers.append(p8)
        bowlers.append(p9)
        bowlers.append(p10)
        bowlers.append(p11)

        team = Team(name, player_details, [], bowlers)
        return team

    def add_player(self, name, player_type):
        person = Person()
        person.name = name
        player_details = PlayerDetails(person, player_type)
        return player_details

if __name__ == '__main__':
    main = Main()
    main.main()