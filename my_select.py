import time

from sqlalchemy import func, delete, text
from app.db_models import Students, Teachers, Subjects, GroupNo, GroupLists, Marks
from app.db import session



def select_1():
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


def select_2(subject_name):
    # Перевірка наявності назви предмета у таблиці Subjects
    subject_name_exists = session.query(Subjects).filter(Subjects.subject_name == subject_name).first() is not None

    if not subject_name_exists:
        print(f'''Предмету '{subject_name}' в базі не знайдено.
              Ось список предметів, що є в базі: 
              Mathematics
              Ukrainian
              English
              Biology
              Geography
              Chemistry
              Physics
              History''')
        return f"Предмету '{subject_name}' в базі не знайдено." 
    
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

        print(f"Студент: {top_student.first_name} {top_student.last_name}, cередній бал з предмету '{subject_name}': {top_student.avg_mark:.2f}")

    except Exception as e:
        print(f"Помилка при отриманні даних: {e}")


def select_3(subject_id):
        # Перевірка наявності назви предмета у таблиці Subjects
    subject_id_exists = session.query(Subjects).filter(Subjects.subject_id == subject_id).first()
    if not subject_id_exists:
        print(f'''Предмету '{subject_id}' в базі не знайдено.
              В базі є 8 предметів.''')
        return f"Предмету '{subject_id}' в базі не знайдено." 
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
    try:
        avg_mark = session.query(func.avg(Marks.mark)).scalar()
        print(f"Середній бал на потоці: {avg_mark:.2f}")
        return avg_mark
    except Exception as e:
        print(f"Помилка при отриманні середнього балу на потоці: {e}")


def select_5(teacher_id):
        # Перевірка наявності назви предмета у таблиці Subjects
    teacher_id_exists = session.query(Teachers).filter(Teachers.teacher_id == teacher_id).first()
    if not teacher_id_exists:
        print(f'''Викладача '{teacher_id}' в базі не знайдено.
              В базі є 5 виклалачів.''')
        return f"Викладача '{teacher_id}' в базі не знайдено." 
    teacher = session.query(Teachers).filter(Teachers.teacher_id == teacher_id).first()
    if not teacher:
        print(f"Викладач з ID {teacher_id} нічого не викладає.")
        return f"Викладач з ID {teacher_id} нічого не викладає"
    teacher_name = f"{teacher.first_name} {teacher.last_name}"
    try:
        courses = session.query(Subjects.subject_name).filter(Subjects.teacher_id_fk == teacher_id).all()
        print(f"Викладач {teacher_name} (ID {teacher_id}) читає такі курси:")
        for course in courses:
            print(course.subject_name)
    except Exception as e:
        print(f"Помилка при отриманні курсів, які читає викладач з ID {teacher_id}: {e}")


def select_6(group_id):
        # Перевірка наявності назви предмета у таблиці Subjects
    group_id_exists = session.query(GroupNo).filter(GroupNo.group_id == group_id).first()
    if not group_id_exists:
        print(f'''ID групи '{group_id}' в базі не знайдено.
              В базі є 3 групи.''')
        return f"ID групи '{group_id}' в базі не знайдено." 
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
    group_id_exists = session.query(GroupNo).filter(GroupNo.group_id == group_id).first()
    # subject_id_exists = session.query(Subjects).filter(Subjects.subject_id == subject_id).first()
    if not group_id_exists:
        print(f'''ID групи '{group_id}' в базі не знайдено.
              В базі є 3 групи.''')
        return f"ID групи '{group_id}' в базі не знайдено." 
    # if not subject_id_exists:
    #     print(f'''ID предмету '{subject_id}' в базі не знайдено.
    #           В базі є 8 предметів.''')
    #     return f"ID предмету '{subject_id}' в базі не знайдено" 
    try:
        # Отримуємо список student_id у заданій групі
        student_ids = session.query(GroupLists.student_id_fk).filter(GroupLists.group_id_fk == group_id).all()
        
        if not student_ids:
            print(f"У групі {group_id} не знайдено оцінок для предмету {subject_id}.")
            return f"У групі {group_id} не знайдено оцінок для предмету {subject_id}."

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
    try:
        # Отримуємо список предметів, за якими є оцінки у студента
        subjects = session.query(Subjects).join(Marks, Marks.subject_id_fk == Subjects.subject_id)\
                                          .filter(Marks.student_id_fk == student_id)\
                                          .distinct().all()

        if not subjects:
            print(f"Студента з ID {student_id} немає в базі. В базі є лише 50 студентів")
            return f"Студента з ID {student_id} немає в базі. В базі є лише 50 студентів"
        
        print(f"Список курсів для студента з ID {student_id}:")
        subject_names = [subject.subject_name for subject in subjects]
        for subject_name in subject_names:
            print(subject_name)
        
        return subject_names
    except Exception as e:
        print(f"Помилка при отриманні курсів для студента з ID {student_id}: {e}")


def select_10(student_id, teacher_id): 
    try:
        # список предметів, які викладає певний викладач певному студенту:
        subjects = session.query(Subjects).join(Marks, Marks.subject_id_fk == Subjects.subject_id)\
                                          .filter(Marks.student_id_fk == student_id, Subjects.teacher_id_fk == teacher_id)\
                                          .distinct().all()

        if not subjects:
            print(f'''Не знайдено студента з ID {student_id}, або викладача з ID {teacher_id}.
                  Студентів є 50, а викладачів - лише 5. 
                  Перевір, будь ласка, свої вхідні параметри для пошуку.''')
            return f"Не знайдено студента з ID {student_id}, або викладача з ID {teacher_id}."

        print(f"Список курсів для студента з ID {student_id}, які читає викладач з ID {teacher_id}:")
        subject_names = [subject.subject_name for subject in subjects]
        for subject_name in subject_names:
            print(subject_name)
        
        return subject_names
    except Exception as e:
        print(f"Помилка при отриманні курсів для студента з ID {student_id}, які читає викладач з ID {teacher_id}: {e}")


def truncate_table(table_name):
    session.execute(delete(table_name))
    session.commit()


list_of_queries = ["1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.", 
                   "2. Знайти студента із найвищим середнім балом з певного предмета.",
                   "3. Знайти середній бал у групах з певного предмета.", 
                   "4. Знайти середній бал на потоці (по всій таблиці оцінок).", 
                   "5. Знайти які курси читає певний викладач.", 
                   "6. Знайти список студентів у певній групі.",
                   "7. Знайти оцінки студентів у окремій групі з певного предмета.",
                   "8. Знайти середній бал, який ставить певний викладач зі своїх предметів.",
                   "9. Знайти список курсів, які відвідує студент.",
                   "10. Список курсів, які певному студенту читає певний викладач."
                   ]

# def alter_sequence():
    # session.execute(text("ALTER SEQUENCE subjects_subject_id_seq RESTART WITH 1"))
    # session.execute(text("ALTER SEQUENCE students_student_id_seq RESTART WITH 1"))
    # session.execute(text("ALTER SEQUENCE group_no_group_id_seq RESTART WITH 1"))
    # session.execute(text("ALTER SEQUENCE group_lists_group_id_fk_seq RESTART WITH 1"))
    # session.execute(text("ALTER SEQUENCE marks_id_seq RESTART WITH 1"))
    # session.execute(text("ALTER SEQUENCE teachers_teacher_id_seq RESTART WITH 1"))
    # session.commit()

def main():
    query_number = int(input("Введіть необхідний номер завдання (від 1 до 12): "))
    print(list_of_queries[int(f"{query_number}")-1])
    time.sleep(1.5)
    if query_number == 1:
        select_1()
    elif query_number == 2:
        subject_name = input("Введіть назву предмета: ")
        select_2(subject_name)
    elif query_number == 3:
        subject_id = int(input("Введіть ID предмету: "))
        select_3(subject_id)
    elif query_number == 4:
        select_4()
    elif query_number == 5:
        teacher_id = int(input("Введіть ID необхідного викладача: "))
        select_5(teacher_id)
    elif query_number == 6:
        group_id = int(input("Введіть ID необхідної групи: "))
        select_6(group_id)
    elif query_number == 7:
        group_id = int(input("Введіть ID необхідної групи: "))
        subject_id = int(input("Введіть ID предмету: "))
        select_7(group_id, subject_id)
    elif query_number == 8:
        teacher_id = int(input("Введіть ID необхідного викладача: "))
        select_8(teacher_id)
    elif query_number == 9:
        student_id = int(input("Введіть ID необхідного студента: "))
        select_9(student_id)
    elif query_number == 10:
        student_id = int(input("Введіть ID необхідного студента: ")) 
        teacher_id = int(input("Введіть ID необхідного викладача: "))
        select_10(student_id, teacher_id)
    else:
        print("Невірне введення, спробуйте ще раз.")
    


if __name__ == "__main__":
    main()
    # select_1()
    # select_2(subject_name="Biology")
    # select_3(subject_id=9) 
    # select_4()
    # select_5(teacher_id=6)
    # select_6(group_id="6")
    # select_7(group_id=5, subject_id=5)
    # select_8(teacher_id=1)
    # select_9(student_id=56)
    # select_10(student_id=50, teacher_id=1)

    # truncate_table(Marks)
    # truncate_table(GroupLists)
    # truncate_table(GroupNo)
    # truncate_table(Subjects)
    # truncate_table(Teachers)
    # truncate_table(Students)


