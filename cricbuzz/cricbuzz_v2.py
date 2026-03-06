import random
from enum import Enum
from abc import ABC, abstractmethod
import uuid


class Ball:
    class BallBuilder:
        def __init__(self):
            self.over_number = 0
            self.ball_number = 0
            self._bowled_by = None
            self._faced_by = None
            self.runs_scored = 0
            self.wicket = None
            self.extra_type = None
            self.commentary = None

        def in_over(self, over_number):
            self.over_number = over_number
            return self

        def with_ball_number(self, ball_number):
            self.ball_number = ball_number
            return self

        def bowled_by(self, bowler):
            self._bowled_by = bowler
            return self

        def faced_by(self, batsman):
            self._faced_by = batsman
            return self

        def with_runs(self, runs):
            self.runs_scored = runs
            return self

        def with_wicket(self, wicket):
            self.wicket = wicket
            return self

        def with_extra_type(self, extra):
            self.extra_type = extra
            return self

        def with_commentary(self, commentary):
            self.commentary = commentary
            return self

        def build(self):
            if self.commentary is None:
                temp_ball = Ball(self)
                self.commentary = CommentaryManager.get_instance().generate_commentary(temp_ball)

            return Ball(self)

    def __init__(self, builder):
        self.over_number = builder.over_number
        self.ball_number = builder.ball_number
        self.bowled_by = builder._bowled_by
        self.faced_by = builder._faced_by
        self.runs_scored = builder.runs_scored
        self.wicket = builder.wicket
        self.extra_type = builder.extra_type
        self.commentary = builder.commentary

    def is_wicket(self):
        return self.wicket is not None

    def is_boundary(self):
        return self.runs_scored == 4 or self.runs_scored == 6

    def get_ball_number(self):
        return self.ball_number

    def get_bowled_by(self):
        return self.bowled_by

    def get_faced_by(self):
        return self.faced_by

    def get_runs_scored(self):
        return self.runs_scored

    def get_wicket(self):
        return self.wicket

    def get_extra_type(self):
        return self.extra_type

    def get_commentary(self):
        return self.commentary



class CommentaryManager:
    _instance = None

    def __init__(self):
        self.random = random.Random()
        self.commentary_templates = {}
        self.initialize_templates()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CommentaryManager()
        return cls._instance

    def initialize_templates(self):
        self.commentary_templates["RUNS_0"] = [
            "%s defends solidly.",
            "No run, good fielding by the cover fielder.",
            "A dot ball to end the over.",
            "Pushed to mid-on, but no run."
        ]
        self.commentary_templates["RUNS_1"] = [
            "Tucked away to the leg side for a single.",
            "Quick single taken by %s.",
            "Pushed to long-on for one."
        ]
        self.commentary_templates["RUNS_2"] = [
            "Two runs taken!",
            "Quick double taken by %s.",
            "Pushed to mid-on for two."
        ]
        self.commentary_templates["RUNS_4"] = [
            "FOUR! %s smashes it through the covers!",
            "Beautiful shot! That's a boundary.",
            "Finds the gap perfectly. Four runs."
        ]
        self.commentary_templates["RUNS_6"] = [
            "SIX! That's out of the park!",
            "%s sends it sailing over the ropes!",
            "Massive hit! It's a maximum."
        ]

        self.commentary_templates[f"WICKET_{WicketType.BOWLED.value}"] = [
            "BOWLED HIM! %s misses completely and the stumps are shattered!",
            "Cleaned up! A perfect yorker from %s."
        ]
        self.commentary_templates[f"WICKET_{WicketType.CAUGHT.value}"] = [
            "CAUGHT! %s skies it and the fielder takes a comfortable catch.",
            "Out! A brilliant catch in the deep by %s."
        ]
        self.commentary_templates[f"WICKET_{WicketType.LBW.value}"] = [
            "LBW! That one kept low and struck %s right in front.",
            "%s completely misjudged the line and pays the price."
        ]
        self.commentary_templates[f"WICKET_{WicketType.STUMPED.value}"] = [
            "STUMPED! %s misses it, and the keeper does the rest!",
            "Gone! Lightning-fast work by the keeper to stump %s."
        ]

        self.commentary_templates[f"EXTRA_{ExtraType.WIDE.value}"] = [
            "That's a wide. The umpire signals an extra run.",
            "Too far down the leg side, that'll be a wide."
        ]
        self.commentary_templates[f"EXTRA_{ExtraType.NO_BALL.value}"] = [
            "No ball! %s has overstepped. It's a free hit.",
            "It's a no-ball for overstepping."
        ]

    def generate_commentary(self, ball):
        key = self.get_event_key(ball)
        templates = self.commentary_templates.get(key, ["Just a standard delivery."])
        
        template = self.random.choice(templates)
        
        batsman_name = ball.get_faced_by().get_name() if ball.get_faced_by() else ""
        bowler_name = ball.get_bowled_by().get_name() if ball.get_bowled_by() else ""
        
        try:
            return template % batsman_name
        except:
            return template.replace("%s", batsman_name)

    def get_event_key(self, ball):
        if ball.is_wicket():
            return f"WICKET_{ball.get_wicket().get_wicket_type().value}"
        if ball.get_extra_type():
            return f"EXTRA_{ball.get_extra_type().value}"
        if 0 <= ball.get_runs_scored() <= 6:
            return f"RUNS_{ball.get_runs_scored()}"
        return "DEFAULT"



class MatchType(Enum):
    T20 = "T20"
    ODI = "ODI"
    TEST = "TEST"

class MatchStatus(Enum):
    SCHEDULED = "SCHEDULED"
    LIVE = "LIVE"
    IN_BREAK = "IN_BREAK"
    FINISHED = "FINISHED"
    ABANDONED = "ABANDONED"

class PlayerRole(Enum):
    BATSMAN = "BATSMAN"
    BOWLER = "BOWLER"
    ALL_ROUNDER = "ALL_ROUNDER"
    WICKET_KEEPER = "WICKET_KEEPER"

class WicketType(Enum):
    BOWLED = "BOWLED"
    CAUGHT = "CAUGHT"
    LBW = "LBW"
    RUN_OUT = "RUN_OUT"
    STUMPED = "STUMPED"
    HIT_WICKET = "HIT_WICKET"

class ExtraType(Enum):
    WIDE = "WIDE"
    NO_BALL = "NO_BALL"
    BYE = "BYE"
    LEG_BYE = "LEG_BYE"



class Innings:
    def __init__(self, batting_team, bowling_team):
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.score = 0
        self.wickets = 0
        self.balls = []
        self.player_stats = {}
        
        for player in batting_team.get_players():
            self.player_stats[player] = PlayerStats()
        for player in bowling_team.get_players():
            self.player_stats[player] = PlayerStats()

    def add_ball(self, ball):
        self.balls.append(ball)
        runs_scored = ball.get_runs_scored()
        self.score += runs_scored
        
        if ball.get_extra_type() in [ExtraType.WIDE, ExtraType.NO_BALL]:
            self.score += 1
        else:
            ball.get_faced_by().get_stats().update_runs(runs_scored)
            ball.get_faced_by().get_stats().increment_balls_played()
            self.player_stats[ball.get_faced_by()].update_runs(runs_scored)
            self.player_stats[ball.get_faced_by()].increment_balls_played()
        
        if ball.is_wicket():
            self.wickets += 1
            ball.get_bowled_by().get_stats().increment_wickets()
            self.player_stats[ball.get_bowled_by()].increment_wickets()

    def print_player_stats(self):
        for player, stats in self.player_stats.items():
            if stats.get_balls_played() > 0 or stats.get_wickets() > 0:
                print(f"Player: {player.get_name()} - Stats: {stats}")

    def get_overs(self):
        valid_balls = sum(1 for b in self.balls 
                         if b.get_extra_type() not in [ExtraType.WIDE, ExtraType.NO_BALL])
        
        completed_overs = valid_balls // 6
        balls_in_current_over = valid_balls % 6
        
        return completed_overs + (balls_in_current_over / 10.0)

    def get_batting_team(self):
        return self.batting_team

    def get_bowling_team(self):
        return self.bowling_team

    def get_score(self):
        return self.score

    def get_wickets(self):
        return self.wickets

    def get_balls(self):
        return self.balls


# interface
class MatchFormatStrategy(ABC):
    @abstractmethod
    def get_total_innings(self):
        pass

    @abstractmethod
    def get_total_overs(self):
        pass

    @abstractmethod
    def get_format_name(self):
        pass

class T20FormatStrategy(MatchFormatStrategy):
    def get_total_innings(self):
        return 2

    def get_total_overs(self):
        return 20

    def get_format_name(self):
        return "T20"

class ODIFormatStrategy(MatchFormatStrategy):
    def get_total_innings(self):
        return 2

    def get_total_overs(self):
        return 50

    def get_format_name(self):
        return "ODI"


#interface
class MatchObserver(ABC):
    @abstractmethod
    def update(self, match, last_ball):
        pass

class CommentaryDisplay(MatchObserver):
    def update(self, match, last_ball):
        if match.get_current_status() == MatchStatus.FINISHED:
            print("[COMMENTARY]: Match has finished!")
        elif match.get_current_status() == MatchStatus.IN_BREAK:
            print("[COMMENTARY]: Inning has ended!")
        else:
            print(f"[COMMENTARY]: {last_ball.get_commentary()}")

class UserNotifier(MatchObserver):
    def update(self, match, last_ball):
        if match.get_current_status() == MatchStatus.FINISHED:
            print("[NOTIFICATION]: Match has finished!")
        elif match.get_current_status() == MatchStatus.IN_BREAK:
            print("[NOTIFICATION]: Inning has ended!")
        elif last_ball and last_ball.is_wicket():
            print("[NOTIFICATION]: Wicket! A player is out.")
        elif last_ball and last_ball.is_boundary():
            print(f"[NOTIFICATION]: It's a boundary! {last_ball.get_runs_scored()} runs.")

class ScorecardDisplay(MatchObserver):
    def update(self, match, last_ball):
        if match.get_current_status() == MatchStatus.FINISHED:
            print("\n--- MATCH RESULT ---")
            print(match.get_result_message().upper())
            print("--------------------")
            
            print("Player Stats:")
            counter = 1
            for inning in match.get_innings():
                print(f"Inning {counter}")
                inning.print_player_stats()
                counter += 1
        elif match.get_current_status() == MatchStatus.IN_BREAK:
            print("\n--- END OF INNINGS ---")
            last_innings = match.get_innings()[-1]
            print(f"Final Score: {last_innings.get_batting_team().get_name()}: "
                  f"{last_innings.get_score()}/{last_innings.get_wickets()} "
                  f"(Overs: {last_innings.get_overs():.1f})")
            print("------------------------")
        else:
            print("\n--- SCORECARD UPDATE ---")
            current_innings = match.get_current_innings()
            print(f"{current_innings.get_batting_team().get_name()}: "
                  f"{current_innings.get_score()}/{current_innings.get_wickets()} "
                  f"(Overs: {current_innings.get_overs():.1f})")
            print("------------------------")



# interface
class MatchState(ABC):
    @abstractmethod
    def process_ball(self, match, ball):
        pass

    def start_next_innings(self, match):
        print("ERROR: Cannot start the next innings from the current state.")

class ScheduledState(MatchState):
    def process_ball(self, match, ball):
        print("ERROR: Cannot process a ball for a match that has not started.")

class InBreakState(MatchState):
    def process_ball(self, match, ball):
        print("ERROR: Cannot process a ball. The match is currently in a break.")

    def start_next_innings(self, match):
        print("Starting the next innings...")
        match.create_new_innings()
        match.set_state(LiveState())
        match.set_current_status(MatchStatus.LIVE)

class FinishedState(MatchState):
    def process_ball(self, match, ball):
        print("ERROR: Cannot process a ball for a finished match.")

class LiveState(MatchState):
    def process_ball(self, match, ball):
        current_innings = match.get_current_innings()
        current_innings.add_ball(ball)
        match.notify_observers(ball)
        self.check_for_match_end(match)

    def check_for_match_end(self, match):
        current_innings = match.get_current_innings()
        innings_count = len(match.get_innings())
        is_final_innings = (innings_count == match.get_format_strategy().get_total_innings())

        # Win condition: Chasing team surpasses the target
        if is_final_innings:
            target_score = match.get_innings()[0].get_score() + 1
            if current_innings.get_score() >= target_score:
                wickets_remaining = (len(current_innings.get_batting_team().get_players()) - 1) - current_innings.get_wickets()
                self.declare_winner(match, current_innings.get_batting_team(), f"won by {wickets_remaining} wickets")
                return

        # End of innings condition
        if self.is_innings_over(match):
            if is_final_innings:
                score1 = match.get_innings()[0].get_score()
                score2 = current_innings.get_score()

                if score1 > score2:
                    self.declare_winner(match, match.get_team1(), f"won by {score1 - score2} runs")
                elif score2 > score1:
                    wickets_remaining = (len(current_innings.get_batting_team().get_players()) - 1) - current_innings.get_wickets()
                    self.declare_winner(match, current_innings.get_batting_team(), f"won by {wickets_remaining} wickets")
                else:
                    self.declare_winner(match, None, "Match Tied")
            else:
                print("End of the innings!")
                match.set_state(InBreakState())
                match.set_current_status(MatchStatus.IN_BREAK)
                match.notify_observers(None)

    def declare_winner(self, match, winning_team, message):
        print("MATCH FINISHED!")
        match.set_winner(winning_team)
        result_message = f"{winning_team.get_name()} {message}" if winning_team else message
        match.set_result_message(result_message)

        match.set_state(FinishedState())
        match.set_current_status(MatchStatus.FINISHED)
        match.notify_observers(None)

    def is_innings_over(self, match):
        current_innings = match.get_current_innings()
        all_out = current_innings.get_wickets() >= len(current_innings.get_batting_team().get_players()) - 1
        overs_finished = int(current_innings.get_overs()) >= match.get_format_strategy().get_total_overs()
        return all_out or overs_finished



class Match:
    def __init__(self, match_id, team1, team2, format_strategy):
        self.id = match_id
        self.team1 = team1
        self.team2 = team2
        self.format_strategy = format_strategy
        self.innings = [Innings(team1, team2)]
        self.current_state = ScheduledState()
        self.current_status = None
        self.observers = []
        self.winner = None
        self.result_message = ""

    def process_ball(self, ball):
        self.current_state.process_ball(self, ball)

    def start_next_innings(self):
        self.current_state.start_next_innings(self)

    def create_new_innings(self):
        if len(self.innings) >= self.format_strategy.get_total_innings():
            print("Cannot create a new innings, match has already reached its limit.")
            return
        
        next_innings = Innings(self.team2, self.team1)
        self.innings.append(next_innings)

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, ball):
        for observer in self.observers:
            observer.update(self, ball)

    def get_current_innings(self):
        return self.innings[-1]

    def get_id(self):
        return self.id

    def get_team1(self):
        return self.team1

    def get_team2(self):
        return self.team2

    def get_format_strategy(self):
        return self.format_strategy

    def get_innings(self):
        return self.innings

    def get_current_status(self):
        return self.current_status

    def get_winner(self):
        return self.winner

    def get_result_message(self):
        return self.result_message

    def set_state(self, state):
        self.current_state = state

    def set_current_status(self, status):
        self.current_status = status

    def set_winner(self, winner):
        self.winner = winner

    def set_result_message(self, message):
        self.result_message = message


class Over:
    def __init__(self, over_number: int, bowler):
        self.over_number = over_number
        self.bowler = bowler
        self.balls = []

    def add_ball(self, ball):
        self.balls.append(ball)

    def get_total_runs(self):
        return sum(ball.runs_scored for ball in self.balls)

    def get_wickets(self):
        return [ball.wicket for ball in self.balls if ball.wicket is not None]

    def is_complete(self):
        return len(self.balls) == 6



class PlayerStats:
    def __init__(self):
        self.runs = 0
        self.balls_played = 0
        self.wickets = 0

    def update_runs(self, run_scored):
        self.runs += run_scored

    def increment_balls_played(self):
        self.balls_played += 1

    def increment_wickets(self):
        self.wickets += 1

    def get_runs(self):
        return self.runs

    def get_balls_played(self):
        return self.balls_played

    def get_wickets(self):
        return self.wickets

    def __str__(self):
        return f"Runs: {self.runs}, Balls Played: {self.balls_played}, Wickets: {self.wickets}"



class Player:
    def __init__(self, player_id, name, role):
        self.id = player_id
        self.name = name
        self.role = role
        self.stats = PlayerStats()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_role(self):
        return self.role

    def get_stats(self):
        return self.stats


class MatchRepository:
    def __init__(self):
        self.matches = {}

    def save(self, match):
        self.matches[match.get_id()] = match

    def find_by_id(self, match_id):
        return self.matches.get(match_id)

class PlayerRepository:
    def __init__(self):
        self.players = {}

    def save(self, player):
        self.players[player.get_id()] = player

    def find_by_id(self, player_id):
        return self.players.get(player_id)


class Team:
    def __init__(self, team_id, name, players):
        self.id = team_id
        self.name = name
        self.players = players

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_players(self):
        return self.players


class Wicket:
    class Builder:
        def __init__(self, wicket_type, player_out):
            self.wicket_type = wicket_type
            self.player_out = player_out
            self._caught_by = None
            self._runout_by = None

        def caught_by(self, player):
            self._caught_by = player
            return self

        def runout_by(self, player):
            self._runout_by = player
            return self

        def build(self):
            return Wicket(self)

    def __init__(self, builder):
        self.wicket_type = builder.wicket_type
        self.player_out = builder.player_out
        self.caught_by = builder._caught_by
        self.runout_by = builder._runout_by

    def get_wicket_type(self):
        return self.wicket_type

    def get_player_out(self):
        return self.player_out

    def get_caught_by(self):
        return self.caught_by

    def get_runout_by(self):
        return self.runout_by



class CricInfoService:
    _instance = None

    def __init__(self):
        self.match_repository = MatchRepository()
        self.player_repository = PlayerRepository()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CricInfoService()
        return cls._instance

    def create_match(self, team1, team2, format_strategy):
        match_id = str(uuid.uuid4())
        match = Match(match_id, team1, team2, format_strategy)
        self.match_repository.save(match)
        print(f"Match {format_strategy.get_format_name()} created between {team1.get_name()} and {team2.get_name()}.")
        return match

    def start_match(self, match_id):
        match = self.match_repository.find_by_id(match_id)
        match.set_current_status(MatchStatus.LIVE)

        if match:
            match.set_state(LiveState())
            print(f"Match {match_id} is now LIVE.")

    def process_ball_update(self, match_id, ball):
        match = self.match_repository.find_by_id(match_id)
        if match:
            match.process_ball(ball)

    def start_next_innings(self, match_id):
        match = self.match_repository.find_by_id(match_id)
        if match:
            match.start_next_innings()

    def subscribe_to_match(self, match_id, observer):
        match = self.match_repository.find_by_id(match_id)
        if match:
            match.add_observer(observer)

    def end_match(self, match_id):
        match = self.match_repository.find_by_id(match_id)
        if match:
            match.set_state(FinishedState())
            print(f"Match {match_id} has FINISHED.")

    def add_player(self, player_id, player_name, player_role):
        player = Player(player_id, player_name, player_role)
        self.player_repository.save(player)
        return player



class CricinfoDemo:
    @staticmethod
    def main():
        service = CricInfoService.get_instance()

        # Setup Players and Teams
        p1 = service.add_player("P1", "Virat", PlayerRole.BATSMAN)
        p2 = service.add_player("P2", "Rohit", PlayerRole.BATSMAN)
        p3 = service.add_player("P3", "Bumrah", PlayerRole.BOWLER)
        p4 = service.add_player("P4", "Jadeja", PlayerRole.ALL_ROUNDER)

        p5 = service.add_player("P5", "Warner", PlayerRole.BATSMAN)
        p6 = service.add_player("P6", "Smith", PlayerRole.BATSMAN)
        p7 = service.add_player("P7", "Starc", PlayerRole.BOWLER)
        p8 = service.add_player("P8", "Maxwell", PlayerRole.ALL_ROUNDER)

        india = Team("T1", "India", [p1, p2, p3, p4])
        australia = Team("T2", "Australia", [p5, p6, p7, p8])

        # Create a T20 Match
        t20_match = service.create_match(india, australia, T20FormatStrategy())
        match_id = t20_match.get_id()

        # Create and subscribe observers
        scorecard = ScorecardDisplay()
        commentary = CommentaryDisplay()
        notifier = UserNotifier()

        service.subscribe_to_match(match_id, scorecard)
        service.subscribe_to_match(match_id, commentary)
        service.subscribe_to_match(match_id, notifier)

        # Start the match
        service.start_match(match_id)

        print("\n--- SIMULATING FIRST INNINGS ---")

        over1 = Over(1, p7)

        ball = Ball.BallBuilder().in_over(1).bowled_by(p7).faced_by(p1).with_runs(2).build()
        over1.add_ball(ball)
        service.process_ball_update(match_id, ball)

        ball = Ball.BallBuilder().in_over(1).bowled_by(p7).faced_by(p1).with_runs(1).build()
        over1.add_ball(ball)
        service.process_ball_update(match_id, ball)

        ball = Ball.BallBuilder().in_over(1).bowled_by(p7).faced_by(p2).with_runs(6).build()
        over1.add_ball(ball)
        service.process_ball_update(match_id, ball)

        p2_wicket = Wicket.Builder(WicketType.BOWLED, p2).build()
        ball = Ball.BallBuilder().in_over(1).bowled_by(p7).faced_by(p2).with_runs(0).with_wicket(p2_wicket).build()
        over1.add_ball(ball)
        service.process_ball_update(match_id, ball)

        p3_wicket = Wicket.Builder(WicketType.LBW, p3).build()
        ball = Ball.BallBuilder().in_over(1).bowled_by(p7).faced_by(p3).with_runs(0).with_wicket(p3_wicket).build()
        over1.add_ball(ball)
        service.process_ball_update(match_id, ball)

        ball = Ball.BallBuilder().in_over(1).bowled_by(p7).faced_by(p4).with_runs(4).build()
        over1.add_ball(ball)
        service.process_ball_update(match_id, ball)

        p4_wicket = Wicket.Builder(WicketType.CAUGHT, p4).caught_by(p6).build()
        ball = Ball.BallBuilder().in_over(2).bowled_by(p7).faced_by(p4).with_runs(0).with_wicket(p4_wicket).build()

        over2 = Over(2, p7)
        over2.add_ball(ball)

        service.process_ball_update(match_id, ball)

        print("\n\n--- INNINGS BREAK ---")
        print("Players are off the field. Preparing for the second innings.")

        # Start the second innings
        service.start_next_innings(match_id)

        print("\n--- SIMULATING SECOND INNINGS ---")

        over3 = Over(1, p3)

        ball = Ball.BallBuilder().in_over(1).bowled_by(p3).faced_by(p5).with_runs(4).build()
        over3.add_ball(ball)
        service.process_ball_update(match_id, ball)

        ball = Ball.BallBuilder().in_over(1).bowled_by(p3).faced_by(p5).with_runs(1).build()
        over3.add_ball(ball)
        service.process_ball_update(match_id, ball)

        p5_wicket = Wicket.Builder(WicketType.BOWLED, p5).build()
        ball = Ball.BallBuilder().in_over(1).bowled_by(p3).faced_by(p5).with_runs(0).with_wicket(p5_wicket).build()
        over3.add_ball(ball)
        service.process_ball_update(match_id, ball)

        p7_wicket = Wicket.Builder(WicketType.LBW, p7).build()
        ball = Ball.BallBuilder().in_over(1).bowled_by(p3).faced_by(p7).with_runs(0).with_wicket(p7_wicket).build()
        over3.add_ball(ball)
        service.process_ball_update(match_id, ball)

        p8_wicket = Wicket.Builder(WicketType.STUMPED, p8).build()
        ball = Ball.BallBuilder().in_over(1).bowled_by(p3).faced_by(p8).with_runs(0).with_wicket(p8_wicket).build()
        over3.add_ball(ball)
        service.process_ball_update(match_id, ball)

        service.end_match(match_id)


if __name__ == "__main__":
    CricinfoDemo.main()
