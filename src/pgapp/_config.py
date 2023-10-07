
class Config:
    """ config file management class """
    # import re
    import re

    def __init__(self, path: str):
        """"""
        # attribute variables
        self.__path = path

        # config data
        self.__text, self.__data = self.__read()
        return

    @property
    def path(self) -> str:
        """ config file path """
        return self.__path

    @property
    def text(self) -> str:
        """ config file text """
        return self.__text

    def __repr__(self):
        return f"[system] print text in {self.__path}\n{self.__text}"

    def __read(self) -> tuple[str, dict[str, str | int | float | bool]]:
        """
            read config data.
        :return: (config text, config dict data)
        """
        with open(file=self.path, mode="r", encoding="utf-8") as config:
            text = config.read()
        try:
            data: dict[str, str | int | float | bool] = dict(
                [
                    [
                        float(dum) if self.re.match(r"^\d+\.\d+$", dum)
                        else int(dum) if not self.re.match(r"\D", dum)
                        else bool(dum) if self.re.match(r"^(True)$|^(False)$", dum)
                        else dum
                        for dum in self.re.findall(r"^[^:]+|[^:]+$", line.replace(" ", ""))
                    ]
                    for line in text.split("\n")
                    if not line == ""
                ]
            )
        except ValueError as e:
            print(e)
            data = {}
        return text, data

    def __write(self, data: dict[str, str | int, float | bool]) -> None:
        """
            write config data.
        :param data: config dict data
        """
        with open(file=self.__path, mode="w", encoding="utf-8") as config:
            config.writelines(
                [
                    f"{key}: {value}\n"
                    for key, value in data.items()
                ]
            )
        return

    def __len__(self) -> int:
        """"""
        return len(self.__data)

    def __getitem__(self, key: str) -> str | int | float | bool:
        """
            return config data value.
        :param key: config data dict key
        :return: config data dict value
        """
        return self.__data[key]

    def __setitem__(self, key: str, value: str | int | float | bool) -> None:
        """
            set config data key and value.
        :param key: config data dict key
        :param value: config data dict value
        """
        if not type(key) is str:
            raise TypeError("Not match type -> key is str")
        value_types = (str, int, float, bool)
        if not type(value) in value_types:
            raise TypeError(f"Not match type -> value in {value_types}")
        self.__data[key] = value
        self.__write(self.__data)
        return

    def __delitem__(self, key) -> None:
        """
            del data.
        :param key: config data key to del
        """
        del self.__data[key]
        return

    def __contains__(self, key) -> bool:
        """
            search key.
        :param key: config data key to check
        :return: dose it exist
        """
        return key in self.__data.keys()


def create_config_file(path: str) -> None:
    """
        create config file.
    :param path: config file path.
    """
    with open(file=path, mode="w", encoding="utf-8"):
        pass
    return
