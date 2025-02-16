from random import randint, choice
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.database import session
from conf.models import Group, Teacher, Student, Subject, Grade

fake = Faker()


def insert_groups():
    for _ in range(3):
        group = Group(name=f"Group {fake.unique.word()}")
        session.add(group)
    session.commit()


def insert_teachers():
    for _ in range(randint(3, 5)):
        teacher = Teacher(fullname=fake.unique.name())
        session.add(teacher)
    session.commit()


def insert_subjects():
    teachers = session.query(Teacher).all()
    for _ in range(randint(5, 8)):
        subject = Subject(name=fake.unique.word(), teacher_id=choice(teachers).id)
        session.add(subject)
    session.commit()


def insert_students():
    groups = session.query(Group).all()
    for _ in range(randint(30, 50)):
        student = Student(fullname=fake.unique.name(), group_id=choice(groups).id)
        session.add(student)
    session.commit()


def insert_grades():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for student in students:
        for subject in subjects:
            for _ in range(randint(10, 21)):
                grade = Grade(
                    grade=randint(1, 100),
                    grade_date=fake.date_between(start_date='-1y', end_date='today'),
                    student_id=student.id,
                    subject_id=subject.id
                )
                session.add(grade)
    session.commit()


if __name__ == "__main__":
    try:
        insert_groups()
        insert_teachers()
        insert_subjects()
        insert_students()
        insert_grades()
        print("Database seeded successfully!")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()