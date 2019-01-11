
from sqlalchemy import Table, Column, Boolean, DateTime, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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

    projects = relationship('Project', back_populates='team')
    users = relationship('User', secondary=user_team_table)

    def __repr__(self):
        return f"<Team(id={self.id}, name={self.name})>"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    tokens = relationship('Token', back_populates='user')
    team = relationship('Team', secondary=user_team_table)
    schedules = relationship('Schedule', back_populates='user')
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, team_id={self.team_id})>"

class Token(Base):
    __tablename__ = 'tokens'
    token_str = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    time_created = Column(DateTime, nullable=False)

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

