
from typing import Optional

from sqlalchemy import Table, Column, Boolean, DateTime, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import datetime

from isoweek import Week

Base = declarative_base()

user_team_table = Table(
    'user_team',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('team_id', Integer, ForeignKey('teams.id')),
    UniqueConstraint('user_id', name='unique_user'),
)


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    projects = relationship('Project', back_populates='team')
    users = relationship('User', secondary=user_team_table, back_populates='_teams')
    owner = relationship('User', foreign_keys=[owner_id])
    join_tokens = relationship('JoinToken', back_populates='team')

    def __repr__(self):
        return f"<Team(id={self.id}, name={self.name})>"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    tokens = relationship('Token', back_populates='user')
    _teams = relationship('Team', secondary=user_team_table, back_populates='users')
    schedules = relationship('Schedule', back_populates='user')

    @property
    def team(self) -> Optional[Team]:
        """
        This is a read-only property. Do not UNDER ANY CIRCUMSTANCES attempt to set this.
        """
        return self._teams[0] if self._teams else None
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, team_id={self.team_id})>"

class JoinToken(Base):
    __tablename__ = 'join_token'
    token_str = Column(String(255), primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))

    team = relationship('Team', back_populates='join_tokens')

class Token(Base):
    __tablename__ = 'tokens'
    token_str = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    user = relationship('User', back_populates='tokens')

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    name = Column(String(250), nullable=False)

    team = relationship('Team', back_populates='projects')
    schedules = relationship('Schedule', back_populates='project')
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, team_id={self.team_id})>"

class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    week = Column(Integer, nullable=False)
    hours = Column(Integer, nullable=False)

    user = relationship('User', back_populates="schedules")
    project = relationship('Project', back_populates="schedules")
    
    def __repr__(self):
        return f"<Schedule(id={self.id}, user_id={self.user_id}, project_id={self.project_id}, week={Week.fromordinal(self.week).isoformat()})>"

