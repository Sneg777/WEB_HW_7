from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    students = relationship('Student', back_populates='group')


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)
    subjects = relationship('Subject', back_populates='teacher')


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('Group', back_populates='students')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship('Teacher', back_populates='subjects')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    grade_date = Column(Date, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'))
    student = relationship('Student', backref='grades')
    subject = relationship('Subject', backref='grades')
