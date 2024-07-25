from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db import Base


class Students(Base):
    __tablename__ = "students"

    student_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Student {self.student_id}: {self.first_name} {self.last_name}"


class GroupNo(Base):
    __tablename__ = "group_no"

    group_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_number: Mapped[str] = mapped_column(String(3))


class GroupLists(Base):
    __tablename__ = "group_lists"

    group_id_fk: Mapped[int] = mapped_column(ForeignKey("group_no.group_id"), primary_key=True)
    student_id_fk: Mapped[int] = mapped_column(ForeignKey("students.student_id"), primary_key=True) 
    # оці два primary_key=True вкінці показують, що це складений первинний ключ, бо жодна таблиця 
    # SQLAlchemy не може існувати без хоча б 1 первинного ключа


class Teachers(Base):
    __tablename__ = "teachers"

    teacher_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))


class Subjects(Base):
    __tablename__ = "subjects"

    subject_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject_name: Mapped[str] = mapped_column(String(50), unique=True)
    teacher_id_fk: Mapped[int] = mapped_column(ForeignKey("teachers.teacher_id"), nullable=True) #дозволяємо NULL


class Marks(Base):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id_fk: Mapped[int] = mapped_column(ForeignKey("students.student_id"))
    subject_id_fk: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"))
    mark: Mapped[int] = mapped_column(Integer)
    creation_date: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return f"Mark(id={self.id}, student_id_fk={self.student_id_fk}, subject_id_fk={self.subject_id_fk}, mark={self.mark}, creation_date={self.creation_date})"