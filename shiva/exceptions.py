# -*- coding: utf-8 -*-


class PathDoesNotExistError(Exception):

    def __init__(self, path):
        message = "Path '%s' does not exist." % path
        super(PathDoesNotExistError, self).__init__(message)


class PathIsNotDirectoryError(Exception):

    def __init__(self, path):
        message = "Path '%s' is not a directory." % path
        super(PathIsNotDirectoryError, self).__init__(message)


class PathIsNotFileError(Exception):

    def __init__(self, path):
        message = "Path '%s' is not a file." % path
        super(PathIsNotFileError, self).__init__(message)
