from datetime import datetime
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, ForeignKey, JSON, Identity, Table, Column, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship, declarative_base

Auth_Base = declarative_base()


class Role(Auth_Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(Identity(increment=1, always=True), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    permissions = mapped_column(JSON, nullable=True)

    users: Mapped[List["User"]] = relationship(back_populates="role", lazy='joined')


class CountryBlock(Auth_Base):
    __tablename__ = "country_block"

    id: Mapped[int] = mapped_column(Identity(increment=1, always=True), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    countries: Mapped[List["Country"]] = relationship(back_populates="country_block", lazy='joined')


class Country(Auth_Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(Identity(increment=1, always=True), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    country_block_id: Mapped[int] = mapped_column(ForeignKey("country_block.id"))
    country_block: Mapped["CountryBlock"] = relationship(back_populates="countries", lazy='joined')


class Comment(Auth_Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Identity(increment=1, always=True), primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at = mapped_column(TIMESTAMP, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="comments", lazy='joined')

    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    course: Mapped["Course"] = relationship(back_populates="comments", lazy='joined')


user_course = Table(
    "user_course",
    Auth_Base.metadata,

    Column("id", Integer, Identity(increment=1, always=True), primary_key=True),
    Column("user_id", ForeignKey("user.id")),
    Column("course_id", ForeignKey("course.id"))
)

book_course = Table(
    "book_course",
    Auth_Base.metadata,

    Column("id", Integer, Identity(increment=1, always=True), primary_key=True),
    Column("book_id", ForeignKey("book.id")),
    Column("course_id", ForeignKey("course.id"))
)


class Course(Auth_Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(Identity(increment=1, always=True), primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    subtitle: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    starting_at = mapped_column(TIMESTAMP, nullable=False)
    image_link: Mapped[str] = mapped_column(nullable=False)

    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    country: Mapped["Country"] = relationship(lazy='joined')

    users: Mapped[List["User"]] = relationship(secondary=user_course, back_populates="courses", lazy='joined')

    comments: Mapped[List["Comment"]] = relationship(back_populates="course", lazy='joined')

    books: Mapped[List["Book"]] = relationship(secondary=book_course, back_populates="courses", lazy='joined')


class Schedule(Auth_Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(Identity(increment=1, always=True), primary_key=True)
    start_time = mapped_column(TIMESTAMP, nullable=False)
    end_time = mapped_column(TIMESTAMP, nullable=False)

    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    course: Mapped["Course"] = relationship(lazy='joined')


class User(SQLAlchemyBaseUserTable[int], Auth_Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Identity(increment=1), primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    firstName: Mapped[str] = mapped_column(nullable=False)
    lastName: Mapped[str] = mapped_column(nullable=False)
    created_at = mapped_column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="users", lazy='joined')

    courses: Mapped[List["Course"]] = relationship(secondary=user_course, back_populates="users", lazy='joined')

    comments: Mapped[List["Comment"]] = relationship(back_populates="user", lazy='joined')


class Book(Auth_Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Identity(increment=1, always=True), primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    download_link: Mapped[str | None] = mapped_column(nullable=True)

    courses: Mapped[List["Course"]] = relationship(secondary=book_course, back_populates="books", lazy='joined')

    library_previews: Mapped[List["LibraryPreview"]] = relationship(back_populates="book", lazy='joined')


class LibraryPreview(Auth_Base):
    __tablename__ = "library_preview"

    id: Mapped[int] = mapped_column(Identity(increment=1, always=True), primary_key=True)
    quote: Mapped[str] = mapped_column(nullable=False)
    quote_author: Mapped[str] = mapped_column(nullable=False)

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    book: Mapped["Book"] = relationship(back_populates="library_previews", lazy='joined')
