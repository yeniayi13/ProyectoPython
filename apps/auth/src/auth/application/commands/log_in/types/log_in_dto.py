class Log_in_dto():
    user:str
    password:str

    def __init__(self, user:str, password:str):
        self.user = user
        self.password = password
    