class CommentsException(Exception):
    pass


class CommentsNotFound(CommentsException):
    pass


class CommentNotExist(CommentsException):
    pass


class UserDoesNotOwnCourse(CommentsException):
    pass
