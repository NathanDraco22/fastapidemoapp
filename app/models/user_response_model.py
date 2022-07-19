


class UserResponse:
    ok  : bool
    msg : str
    token : str|None = None

    def __init__(self, ok:bool , msg:str, token:str|None = None ) -> None:
        self.ok    = ok
        self.msg   = msg
        self.token = token

        pass
