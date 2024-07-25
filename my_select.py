import time

from sqlalchemy import func
from app.db_models import Students, Teachers, Subjects, GroupNo, GroupLists, Marks
from app.db import session

def select_1():
    print('''ЗАВДАННЯ 1:
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.''')
    time.sleep(2)
    try:
        top_students = (
            session.query(
                Students.first_name,
                Students.last_name,
                func.avg(Marks.mark).label('avg_mark')
            )
            .join(Marks, Students.student_id == Marks.student_id_fk)
            .group_by(Students.student_id)
            .order_by(func.avg(Marks.mark).desc())
            .limit(5)
            .all()
        )

        for student in top_students:
            print(f"Студент: {student.first_name} {student.last_name}, Середній бал: {student.avg_mark:.2f}")

    except Exception as e:
        print(f"Помилка при отриманні даних: {e}")


from sqlalchemy import func
from app.db_models import Students, Marks, Subjects
from app.db import session

def select_2(subject_name):
    print('''ЗАВДАННЯ 2: 
    Знайти студента із найвищим середнім балом з певного предмета.''')
    time.sleep(2)
    try:
        top_student = (
            session.query(
                Students.first_name,
                Students.last_name,
                func.avg(Marks.mark).label('avg_mark')
            )
            .join(Marks, Students.student_id == Marks.student_id_fk)
            .join(Subjects, Marks.subject_id_fk == Subjects.subject_id)
            .filter(Subjects.subject_name == subject_name)
            .group_by(Students.student_id)
            .order_by(func.avg(Marks.mark).desc())
            .first()
        )

        print(f"Студент: {top_student.first_name} {top_student.last_name}, Середній бал з предмету '{subject_name}': {top_student.avg_mark:.2f}")

    except Exception as e:
        print(f"Помилка при отриманні даних: {e}")


def select_3(subject_id):
    print('''ЗАВДАННЯ 3:
    Знайти середній бал у групах з певного предмета.''')
    time.sleep(2)
    try:
        subject_name = session.query(Subjects.subject_name).filter(Subjects.subject_id == subject_id).scalar()
        result = session.query(
            GroupNo.group_number,
            func.avg(Marks.mark).label('average_mark')
        ).join(
            GroupLists, GroupLists.group_id_fk == GroupNo.group_id
        ).join(
            Students, GroupLists.student_id_fk == Students.student_id
        ).join(
            Marks, Marks.student_id_fk == Students.student_id
        ).filter(
            Marks.subject_id_fk == subject_id
        ).group_by(
            GroupNo.group_number
        ).order_by(
            func.avg(Marks.mark).desc()
        ).all()
        print(f"Середній бал для предмета {subject_name}:")
        for group, average_mark in result:
            print(f"в групі {group} середній бал становить {average_mark:.2f}")
    except Exception as e:
        print(f"Помилка при отриманні середнього балу для груп: {e}")


def select_4():
    print('''ЗАВДАННЯ 4:
    Знайти середній бал на потоці (по всій таблиці оцінок).''')
    time.sleep(2)
    try:
        avg_mark = session.query(func.avg(Marks.mark)).scalar()
        print(f"Середній бал на потоці: {avg_mark:.2f}")
        return avg_mark
    except Exception as e:
        print(f"Помилка при отриманні середнього балу на потоці: {e}")


def select_5(teacher_id):
    print('''ЗАВДАННЯ 5:
    Знайти які курси читає певний викладач.''')
    time.sleep(2)
    teacher = session.query(Teachers).filter(Teachers.teacher_id == teacher_id).first()
    if not teacher:
        print(f"Викладача з ID {teacher_id} не знайдено.")
        return f"Викладача з ID {teacher_id} не знайдено."
    teacher_name = f"{teacher.first_name} {teacher.last_name}"
    try:
        courses = session.query(Subjects.subject_name).filter(Subjects.teacher_id_fk == teacher_id).all()
        print(f"Викладач {teacher_name} (ID {teacher_id}) читає такі курси:")
        for course in courses:
            print(course.subject_name)
    except Exception as e:
        print(f"Помилка при отриманні курсів, які читає викладач з ID {teacher_id}: {e}")


def select_6(group_id):
    print('''ЗАВДАННЯ 6:
    Знайти список студентів у певній групі.''')
    time.sleep(2)
    try:
        student_ids = session.query(GroupLists.student_id_fk).filter(GroupLists.group_id_fk == group_id).all()
        if not student_ids:
            print(f"Групи з ID {group_id} не існує.")
            return f"Групи з ID {group_id} не існує."
        student_ids = [student_id[0] for student_id in student_ids] # Розпаковуємо student_ids з формату [(id1,), (id2,), ...] до [id1, id2, ...]
        students = session.query(Students).filter(Students.student_id.in_(student_ids)).all() #список студентів
        print(f"Список студентів у групі з ID {group_id}:")
        for student in students:
            print(f"ID студента {student.student_id}. {student.first_name} {student.last_name}")

        return students
    except Exception as e:
        print(f"Помилка при отриманні списку студентів у групі з ID {group_id}: {e}")


def select_7(group_id, subject_id):
    print('''ЗАВДАННЯ 7:
    Знайти оцінки студентів у окремій групі з певного предмета.''')
    time.sleep(2)
    try:
        # Отримуємо список student_id у заданій групі
        student_ids = session.query(GroupLists.student_id_fk).filter(GroupLists.group_id_fk == group_id).all()
        
        if not student_ids:
            print(f"Групи {group_id} не існує.")
            return f"Групи {group_id} не існує."

        student_ids = [student_id[0] for student_id in student_ids] # Розпаковуємо student_ids з формату [(id1,), (id2,), ...] до [id1, id2, ...]

        marks = session.query(Marks).filter(
            Marks.student_id_fk.in_(student_ids),
            Marks.subject_id_fk == subject_id
        ).all()

        subject_name = session.query(Subjects.subject_name).filter(Subjects.subject_id == subject_id).scalar()
        
        print(f"Оцінки студентів у групі з ID {group_id} з предмету {subject_name}:")
        for mark in marks:
            student = session.query(Students).filter(Students.student_id == mark.student_id_fk).one()
            print(f"Студент: {student.first_name} {student.last_name}, Оцінка: {mark.mark}, Дата: {mark.creation_date}")
        return marks
    except Exception as e:
        print(f"Помилка при отриманні оцінок студентів у групі з ID {group_id} з предмету {subject_id}: {e}")


def select_8(teacher_id):
    print('''ЗАВДАННЯ 8:
    Знайти середній бал, який ставить певний викладач зі своїх предметів.''')
    time.sleep(1.5)
    try:
        subjects = session.query(Subjects).filter(Subjects.teacher_id_fk == teacher_id).all() # список предметів, які викладає викладач
        if not subjects:
            print(f"Викладача з ID {teacher_id} немає.")
            return f"Викладача з ID {teacher_id} немає."
        
        subject_ids = [subject.subject_id for subject in subjects] # список айдішок предметів
        marks = session.query(Marks).filter(Marks.subject_id_fk.in_(subject_ids)).all() # всі оцінки для предметів цього викладача
        average_mark = session.query(func.avg(Marks.mark)).filter(Marks.subject_id_fk.in_(subject_ids)).scalar() # Обчислення середнього балу

        print(f"Середній бал, який ставить викладач з ID {teacher_id} зі своїх предметів: {average_mark:.2f}")
        return average_mark
    except Exception as e:
        print(f"Помилка при отриманні середнього балу викладача з ID {teacher_id}: {e}")


def select_9(student_id):
    print('''ЗАВДАННЯ 9:
    Знайти список курсів, які відвідує певний студент.''')
    time.sleep(1.5)
    try:
        # Отримуємо список груп, до яких належить студент
        group_ids = session.query(GroupLists.group_id_fk).filter(GroupLists.student_id_fk == student_id).all()
        
        if not group_ids:
            print(f"Студента з ID {student_id} з немає.")
            return f"Студента з ID {student_id} немає."
        
        group_ids = [group_id[0] for group_id in group_ids]

        # Отримуємо список предметів, що викладаються у групах студента
        subjects = session.query(Subjects).join(GroupLists, Subjects.subject_id == GroupLists.group_id_fk)\
                                          .join(GroupNo, GroupNo.group_id == GroupLists.group_id_fk)\
                                          .filter(GroupLists.group_id_fk.in_(group_ids))\
                                          .distinct().all()

        if not subjects:
            print(f"Не знайдено предметів для студента з ID {student_id}.")
            return f"Не знайдено предметів для студента з ID {student_id}."
        
        print(f"Список курсів для студента з ID {student_id}:")
        for subject in subjects:
            print(subject.subject_name)
        
        return [subject.subject_name for subject in subjects]
    except Exception as e:
        print(f"Помилка при отриманні курсів для студента з ID {student_id}: {e}")

def select_10(student_id, teacher_id): 
    print('''ЗАВДАННЯ 10:
    Список курсів, які певному студенту читає певний викладач.''')
    time.sleep(1.5)
    try:
        # Отримання списку груп, до яких належить студент
        group_ids = session.query(GroupLists.group_id_fk).filter(GroupLists.student_id_fk == student_id).all()
        
        if not group_ids:
            print(f"Студента з ID {student_id} немає.")
            return f"Студента з ID {student_id} немає."
        
        group_ids = [group_id[0] for group_id in group_ids]

        # Отримання списку предметів, які читає викладач і які належать до груп студента
        subjects = session.query(Subjects).join(GroupLists).filter(
            Subjects.teacher_id_fk == teacher_id,
            GroupLists.group_id_fk.in_(group_ids)
        ).distinct().all()

        if not subjects:
            print(f"Не знайдено курсів для студента з ID {student_id}, які читає викладач з ID {teacher_id}.")
            return f"Не знайдено курсів для студента з ID {student_id}, які читає викладач з ID {teacher_id}."

        print(f"Список курсів для студента з ID {student_id}, які читає викладач з ID {teacher_id}:")
        for subject in subjects:
            print(subject.subject_name)
        
        return [subject.subject_name for subject in subjects]
    except Exception as e:
        print(f"Помилка при отриманні курсів для студента з ID {student_id}, які читає викладач з ID {teacher_id}: {e}")



if __name__ == "__main__":
    # select_1()
    # select_2(subject_name="")
    # select_3(sublect_id=) 
    # select_4()
    # select_5(teacher_id=3)
    # select_6(group_id=)
    # select_7(group_id=2, subject_id=5)
    # select_8(teacher_id=1)
    select_9(student_id=2)
    # select_10(student_id=15, teacher_id=3)