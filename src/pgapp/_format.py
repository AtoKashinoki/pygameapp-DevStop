# import ABC and abstractmethod
from abc import ABC, abstractmethod


class DescriptorBasis(ABC):
    """ descriptor basis class """

    def __init__(self, *built_in_types: object, mode="w"):
        """
            initial descriptor

        available mode
         * "w" mode - Can be overwritten
         * "wr" mode - Can only be written once

        :param built_in_types: variable types
        :param mode: write mode in variable
        """

        self.__built_in_types = built_in_types
        self.__mode = mode
        return

    def __set_name__(self, owner, name):
        """ set variable name """
        self.__owner, self.__name = owner, name
        return

    @property
    def name(self) -> str:
        """ variable name """
        return self.__name

    @property
    def owner(self) -> str:
        """ variable owner """
        return self.__owner

    def validate(self, value):
        """
            validate set value
        :param value: value to validate
        """
        return

    def __set__(self, instance: object, value):
        """ set value """
        # validate mode
        if self.__mode == "r":
            raise TypeError(f"It is now a read-only variable: {self.__name}")

        # validate built-in type
        if (type(value) not in self.__built_in_types) and not (value is None and None in self.__built_in_types):
            raise TypeError(f"Not match built-in types: {type(value)}")

        # validate function
        self.validate(value)

        # set value
        instance.__dict__[self.__name] = value

        # change mode
        if self.__mode == "wr":
            self.__mode = "r"
        return

    def __get__(self, instance, owner):
        """ get value """
        return instance.__dict__[self.__name]


class FilePath:
    """ file path management class """
    path = DescriptorBasis(str)

    def __init__(self, *path: str | tuple[str]):
        """
            set path.
        :param path: path or names
        """
        self.path = ""
        if not type(path) is str:
            [self.add_path(name) for name in path]
            return
        return

    def __str__(self) -> str:
        """
            file path.
        :return: path
        """
        return self.path

    def add_path(self, name: str) -> None:
        """
            add file path
        :param name: file or directory name
        """
        if self.path == "":
            self.path = name
            return
        self.path += f"/{name}"
        return

    def __eq__(self, other) -> bool:
        """
            check self eq other
        :param other: data to check
        :return: bool
        """
        other_type = type(other)
        if other_type is str:
            return self.path == other
        if other_type is FilePath:
            return self.path == other.path
        return False

    def __add__(self, other) -> str:
        """
            addition path.
        :param other: file name or path
        :return: str
        """
        other_type = type(other)
        if other_type is str:
            return self.path + "/" + other
        if other_type is FilePath:
            return self.path + "/" + other.path
        raise TypeError(f'can only concatenate str or FilePath (not "{other_type.__name__}") to FilePath')
