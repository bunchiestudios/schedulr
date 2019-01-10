
from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from isoweek import Week

Base = declarative_base()


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    projects = relationship('Project', back_populates='team')
    users = relationship('User', back_populates='team')

    def __repr__(self):
        return f"<Team(id={self.id}, name={self.name})>"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(128), nullable=False)

    team = relationship('Team', back_populates='users')
    schedules = relationship('Schedule', back_populates='user')
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, team_id={self.team_id})>"

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

