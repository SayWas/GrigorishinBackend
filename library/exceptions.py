class LibraryException(Exception):
    pass


class LibraryPreviewEmpty(LibraryException):
    pass


class LibraryPreviewNotExist(LibraryException):
    pass


class LibraryNotFound(LibraryException):
    pass


class LibraryBookNotExist(LibraryException):
    pass
