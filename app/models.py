from . import db
from flask_login import UserMixin

# =========================
# Institute
# =========================

class Institute(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    points = db.Column(
        db.Integer,
        default=0
    )

    # связь с командами
    teams = db.relationship(
        "Team",
        backref="institute",
        lazy=True
    )

    logo = db.Column(
        db.String(200)
    )

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

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

    sport_id = db.Column(
        db.Integer,
        db.ForeignKey("sport.id"),
        nullable=False
    )

    sport = db.relationship(
        "Sport",
        backref="teams"
    )

    institute_id = db.Column(
        db.Integer,
        db.ForeignKey("institute.id"),
        nullable=False
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
        return f"{self.name} ({self.sport})"

    def __str__(self):
        return f"{self.name} ({self.sport})"

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
        return f"{self.sport}: {self.team1_id} vs {self.team2_id}"

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

    def __str__(self):
        return self.name