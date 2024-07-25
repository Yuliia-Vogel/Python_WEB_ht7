from random import shuffle, randint, sample
from datetime import datetime

from faker import Faker

from app.db_models import Students, Teachers, GroupNo, GroupLists, Subjects, Marks
from app.db import session


fake = Faker(locale="uk-UA")

def make_fake_students():
    try:
        for _ in range(50):
            student = Students(
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            session.add(student)
        session.commit()
        print("50 студентів додано успішно.")
    except Exception as e:
        session.rollback()
        print(f"Помилка при додаванні студентів: {e}")


def make_fake_teachers():
    try:
        for _ in range(5):
            teacher = Teachers(
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            session.add(teacher)
        session.commit()
        print("5 викладачів додано успішно.")
    except Exception as e:
        session.rollback()
        print(f"Помилка при додаванні викладачів: {e}")


def add_fake_groups():
    try:
        groups_list = ["E23", "P26", "N67"]

        for group in groups_list:
            session.add(GroupNo(group_number=group))
        session.commit()
        print("Групи додано успішно.")
    except Exception as e:
        session.rollback()
        print(f"Помилка при додаванні груп: {e}")


def make_fake_group_lists():
    try:
        student_ids = [student.student_id for student in session.query(Students.student_id).all()]
        group_ids = [group.group_id for group in session.query(GroupNo.group_id).all()]
        shuffle(student_ids)
        group_count = len(group_ids)

        for i, student_id in enumerate(student_ids):
            group_id = group_ids[i % group_count]
            group_list = GroupLists(group_id_fk=group_id, student_id_fk=student_id)
            session.add(group_list)

        session.commit()
        print("Студенти успішно розподілені по групах.")
    except Exception as e:
        session.rollback()
        print(f"Помилка при розподілі студентів по групах: {e}")


def make_fake_subjects():
    try:
        subjects_list = ["Mathematics", "Ukrainian", "English", "Biology", "Geography", "Chemistry", "Physics", "History"]

        # Додавання предметів до бази даних без викладачів
        for subj in subjects_list:
            session.add(Subjects(subject_name=subj))
        session.commit()  # Зберігаємо предмети, щоб вони мали subject_id
        print("Успішно додано предмети.")
    except Exception as e:
        session.rollback()
        print(f"Помилка при додаванні предметів: {e}")


def add_teachers_to_subjects():
    try:
        # Отримання списку викладачів
        teachers_ids = [teacher.teacher_id for teacher in session.query(Teachers.teacher_id).all()]
        shuffle(teachers_ids)

        # Отримання списку предметів з їхніми id
        subjects = session.query(Subjects).all()

        # Розподіл викладачів по предметах
        for i, subject in enumerate(subjects):
            teacher_id = teachers_ids[i % len(teachers_ids)]  # Циклічно вибираємо викладача
            subject.teacher_id_fk = teacher_id  # Призначаємо викладача предмету

        session.commit()
        print("Успішно додано вчителів, що викладають предмети")
    except Exception as e:
        session.rollback()
        print(f"Помилка при додаванні вчителів до предметів: {e}")


def add_fake_marks():
    try:
        students = session.query(Students).all()
        subjects = session.query(Subjects).all()

        for student in students:
            num_marks = 16 # визначаємо кількість оцінок для кожного студента
            # chosen_subjects = sample(subjects, num_marks)

            for subject in subjects:
                for _ in range(2):  # Додаємо по 2 оцінки з кожного предмету
                    mark = Marks(
                        student_id_fk = student.student_id,
                        subject_id_fk = subject.subject_id,
                        mark = randint(1, 100),
                        creation_date = datetime.now()
                    )
                    session.add(mark)

        session.commit()
        print("Успішно додано оцінки студентам")
    except Exception as e:
        session.rollback()
        print(f"Помилка при додаванні оцінок студентам: {e}")


if __name__ == "__main__":
    make_fake_students()
    add_fake_groups()
    make_fake_teachers()
    make_fake_group_lists()
    make_fake_subjects()
    add_teachers_to_subjects()
    add_fake_marks()