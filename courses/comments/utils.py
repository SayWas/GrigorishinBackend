from enum import Enum


class ErrorCode(str, Enum):
    COMMENTS_NOT_FOUND = "COMMENTS_NOT_FOUND"
    COMMENT_NOT_EXIST = "COMMENT_NOT_EXIST"
