
class FilePath:
    """ file path management class """

    def __init__(self, *path: str | tuple[str]):
        """
            set path.
        :param path: path or names
        """
        self.__path: str = ""
        if not type(path) is str:
            [self.add_path(name) for name in path]
            return
        return

    @property
    def path(self) -> str:
        """
            file path.
        :return: path
        """
        return self.__path

    def __str__(self) -> str:
        """
            file path.
        :return: path
        """
        return self.__path

    def add_path(self, name: str) -> None:
        """
            add file path
        :param name: file or directory name
        """
        if self.__path == "":
            self.__path = name
            return
        self.__path += f"/{name}"
        return

    def __eq__(self, other) -> bool:
        """
            check self eq other
        :param other: data to check
        :return: bool
        """
        other_type = type(other)
        if other_type is str:
            return self.__path == other
        if other_type is FilePath:
            return self.__path == other.path
        return False

    def __add__(self, other) -> str:
        """
            addition path.
        :param other: file name or path
        :return: str
        """
        other_type = type(other)
        if other_type is str:
            return self.__path + "/" + other
        if other_type is FilePath:
            return self.__path + "/" + other.path
        raise TypeError(f'can only concatenate str or FilePath (not "{other_type.__name__}") to FilePath')
