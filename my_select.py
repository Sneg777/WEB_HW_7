from datetime import datetime

from sqlalchemy import and_, or_, func, desc, select
from sqlalchemy.orm import joinedload, subqueryload

from conf.database import session
from conf.models import Teacher, Student, Group, Subject, Grade


# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_01():
    result = session.query(Student.id, Student.fullname,
                           func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Student).join(
        Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_02(subject_name):
    result = (
        session.query(
            Student.fullname,
            func.avg(Grade.grade).label('average_grade'))
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
        .first()
    )
    return result


# 3. Знайти середній бал у групах з певного предмета.
def select_03(subject_name):
    result = (
        session.query(
            Group.name,
            func.avg(Grade.grade).label('average_grade'))
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
        .all()
    )
    return result


# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_04():
    result = (
        session.query(
            func.avg(Grade.grade).label('average_grade'))
        .scalar()
    )
    return result


# 5. Знайти які курси читає певний викладач.
def select_05(teacher_name):
    result = (
        session.query(Subject.name)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.fullname == teacher_name)
        .all()
    )
    return result


# 6. Знайти список студентів у певній групі.
def select_06(group_name):
    result = (
        session.query(Student.fullname)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.name == group_name)
        .all()
    )
    return result


# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_07(group_name, subject_name):
    result = (
        session.query(Student.fullname, Grade.grade)
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return result


# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_08(teacher_name):
    result = (
        session.query(
            func.avg(Grade.grade).label('average_grade'))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.fullname == teacher_name)
        .scalar()
    )
    return result


# 9. Знайти список курсів, які відвідує певний студент.
def select_09(student_name):
    result = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.fullname == student_name)
        .distinct()
        .all()
    )
    return result


# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_name, teacher_name):
    result = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Student.fullname == student_name, Teacher.fullname == teacher_name)
        .distinct()
        .all()
    )
    return result


# 11. Середній бал, який певний викладач ставить певному студентові.
def select_11(teacher_name, student_name):
    result = (
        session.query(
            func.avg(Grade.grade).label('average_grade'))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Teacher.fullname == teacher_name, Student.fullname == student_name)
        .scalar()
    )
    return result


# 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12(group_name, subject_name):
    subquery = (
        session.query(func.max(Grade.grade_date))
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .scalar()
    )

    result = (
        session.query(Student.fullname, Grade.grade)
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name, Subject.name == subject_name, Grade.grade_date == subquery)
        .all()
    )
    return result


if __name__ == "__main__":
    # Example usage
    print(select_01())
    print(select_02("offer"), end='\n\n')
    print(select_03("offer"), end='\n\n')
    print(select_04(), end='\n\n')
    print(select_05("Nicole Travis"), end='\n\n')
    print(select_06("Group how"), end='\n\n')
    print(select_07("Group how", "offer"), end='\n\n')
    print(select_08("Nicole Travis"), end='\n\n')
    print(select_09("David Conley"), end='\n\n')
    print(select_10("David Conley", "Nicole Travis"), end='\n\n')
    print(select_11("Nicole Travis", "David Conley"), end='\n\n')
    print(select_12("Group how", "offer"), end='\n\n')
