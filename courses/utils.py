from enum import Enum


class ErrorCode(str, Enum):
    COURSE_NOT_FOUND = "COURSE_NOT_FOUND"
    COURSES_NOT_FOUND = "COURSES_NOT_FOUND"
    COURSE_NOT_EXIST = "COURSE_NOT_EXIST"
