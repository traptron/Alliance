from datetime import datetime

from . import db
from flask_login import UserMixin

# =========================
# Sport
# =========================

class Sport(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    points_win = db.Column(
        db.Integer,
        default=3
    )

    points_draw = db.Column(
        db.Integer,
        default=1
    )

    points_loss = db.Column(
        db.Integer,
        default=0
    )

    tie_breakers = db.Column(
        db.String(200),
        default="points,wins,goal_difference,scored"
    )

    def __str__(self):
        return self.name


# =========================
# Sport Stat Definition
# =========================

class SportStatDefinition(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sport_id = db.Column(
        db.Integer,
        db.ForeignKey("sport.id"),
        nullable=False
    )

    metric_key = db.Column(
        db.String(50),
        nullable=False
    )

    label = db.Column(
        db.String(100),
        nullable=False
    )

    unit = db.Column(
        db.String(20)
    )

    scope = db.Column(
        db.String(20),
        default="player"
    )

    sort_priority = db.Column(
        db.Integer,
        default=0
    )

    sport = db.relationship(
        "Sport",
        backref="stat_definitions"
    )

    def __str__(self):
        return f"{self.sport.name}: {self.label}" if self.sport else self.label


# =========================
# Player Stat
# =========================

class PlayerStat(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    player_id = db.Column(
        db.Integer,
        db.ForeignKey("player.id"),
        nullable=False
    )

    tournament_id = db.Column(
        db.Integer,
        db.ForeignKey("tournament.id"),
        nullable=False
    )

    metric_key = db.Column(
        db.String(50),
        nullable=False
    )

    value = db.Column(
        db.Float,
        default=0
    )

    player = db.relationship(
        "Player",
        backref="stats"
    )

    tournament = db.relationship(
        "Tournament",
        backref="player_stats"
    )

    def __str__(self):
        return f"{self.player} {self.metric_key}: {self.value}"

# =========================
# Tournament
# =========================

class Tournament(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    sport_id = db.Column(
        db.Integer,
        db.ForeignKey("sport.id"),
        nullable=False
    )

    season = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(50),
        default="active"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    sport = db.relationship(
        "Sport",
        backref="tournaments"
    )

    def __str__(self):
        return f"{self.name} ({self.season})" if self.season else self.name

# =========================
# Team
# =========================

class Team(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    logo = db.Column(
        db.String(200)
    )

    sport_id = db.Column(
        db.Integer,
        db.ForeignKey("sport.id"),
        nullable=False
    )

    sport = db.relationship(
        "Sport",
        backref="teams"
    )

    tournament_id = db.Column(
        db.Integer,
        db.ForeignKey("tournament.id"),
        nullable=False
    )

    tournament = db.relationship(
        "Tournament",
        backref="teams"
    )

    # связь с игроками
    players = db.relationship(
        "Player",
        backref="team",
        lazy=True
    )

    wins = db.Column(
        db.Integer,
        default=0
    )

    draws = db.Column(
        db.Integer,
        default=0
    )

    losses = db.Column(
        db.Integer,
        default=0
    )

    points = db.Column(
        db.Integer,
        default=0
    )

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

# =========================
# Player
# =========================

class Player(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    goals = db.Column(
        db.Integer,
        default=0
    )

    assists = db.Column(
        db.Integer,
        default=0
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("team.id"),
        nullable=False
    )

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

# =========================
# Match
# =========================

class Match(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sport_id = db.Column(
        db.Integer,
        db.ForeignKey("sport.id"),
        nullable=False
    )

    sport = db.relationship(
        "Sport",
        backref="matches"
    )

    tournament_id = db.Column(
        db.Integer,
        db.ForeignKey("tournament.id"),
        nullable=False
    )

    tournament = db.relationship(
        "Tournament",
        backref="matches"
    )

    date = db.Column(
        db.String(50)
    )

    team1_id = db.Column(
        db.Integer,
        db.ForeignKey("team.id")
    )

    team2_id = db.Column(
        db.Integer,
        db.ForeignKey("team.id")
    )

    team1 = db.relationship(
        "Team",
        foreign_keys=[team1_id]
    )

    team2 = db.relationship(
        "Team",
        foreign_keys=[team2_id]
    )

    score1 = db.Column(
        db.Integer,
        default=0
    )

    score2 = db.Column(
        db.Integer,
        default=0
    )

    status = db.Column(
        db.String(50),
        default="upcoming"
    )

    def __str__(self):
        team1 = self.team1.name if self.team1 else "TBD"
        team2 = self.team2.name if self.team2 else "TBD"
        return f"{team1} vs {team2}"

# =========================
# User
# =========================

class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    def __str__(self):
        return self.username
