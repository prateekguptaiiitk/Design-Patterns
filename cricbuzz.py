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

    def getNextPlayer(self):
        if self.yetToPlay.isEmpty():
            raise Exception()

        if not striker:
            striker = self.yet_to_play.poll()

        if not nonStriker:
            nonStriker = self.yet_to_play.poll()
    
    def getStriker(self):
        return self.striker

    def getNonStriker(self):
        return self.non_striker

    def setStriker(self, player_details):
        self.striker = player_details

    def setNonStriker(self, player_details):
        self.non_striker = player_details

from collections import defaultdict
class PlayerBowlingController:
    bowlersList = None
    bowlerVsOverCount = None
    current_bowler = None

    def PlayerBowlingController(self, bowlers):
        self.setBowlersList(bowlers)

    def setBowlersList(self, bowlers_list):
        self.bowlers_list = deque()
        self.bowlerVsOverCount = defaultdict(int)
        for bowler in bowlers_list:
            self.bowlersList.append(bowler)
            self.bowlerVsOverCount.add(bowler, 0)

    def getNextBowler(self, maxOverCountPerBowler):
        playerDetails = self.bowlers_list.poll()
        if self.bowlerVsOverCount[playerDetails] + 1 == maxOverCountPerBowler:
            self.current_bowler = playerDetails
        else:
            self.current_bowler = playerDetails
            self.bowlers_list.append(playerDetails)
            self.bowlerVsOverCount[playerDetails] += 1
        
    def getCurrentBowler(self):
        return self.current_bowler

class PlayerDetails:
    person = None
    playerType = None
    battingScoreCard = None
    bowlingScoreCard = None

    def __init__(self, person, playerType):
        self.person = person
        self.playerType = playerType
        self.battingScoreCard = BattingScoreCard()
        self.bowlingScoreCard = BowlingScoreCard()

    # need to refactor below two functions
    def printBattingScoreCard(self):
        print("PlayerName: ", self.person.name, " -- totalRuns: ", self.battingScoreCard.total_runs, " -- totalBallsPlayed: ", self.bowlingScoreCard.total_balls_played, " -- 4s: ", self.battingScoreCard.total_fours, " -- 6s: ", battingScoreCard.totalSix, " -- outby: ",   ((battingScoreCard.wicketDetails != null) ? battingScoreCard.wicketDetails.takenBy.person.name : "notout"))

    def printBowlingScoreCard(self):
        System.out.println("PlayerName: " + person.name + " -- totalOversThrown: " + bowlingScoreCard.totalOversCount
                + " -- totalRunsGiven: " + bowlingScoreCard.runsGiven + " -- WicketsTaken: " + bowlingScoreCard.wicketsTaken)