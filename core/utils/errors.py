import enum

class Stages(enum):
    DOMAIN = 'Domain'
    APPLICATION = 'Application'
    INFRASTRUCTURE = 'Infrastructure'


class Error(Exception):
    msg: str
    code: int
    stage: Stages
    def __init__(self, name:str, msg: str, code:int) -> None:
        self.name = name
        self.msg = msg
        self.code = code
        super().__init__(msg)

    def __str__(self):
        return f"Error {self.code}: {self.msg}"

