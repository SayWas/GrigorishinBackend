class CoursesException(Exception):
    pass


class CourseNotFound(CoursesException):
    pass


class CoursesNotFound(CoursesException):
    pass


class CourseNotExist(CoursesException):
    pass
