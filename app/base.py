
class Base:

    (
        ALL_ACTIONS,
        HOME,
        END,
        START,
        BACK,
        STOP,
        FINISH,
        *_
    ) = list(map(lambda x: str(x), range(900, 950)))    

    TIME_GRID = [
        ["08:00", "08:30", "09:00"],
        ["09:30", "10:00", "10:30"],
        ["11:00", "11:30", "12:00"],
        ["12:30", "13:00", "13:30"],
        ["14:00", "14:30", "15:00"],
        ["15:30", "16:00", "16:30"],
        ["17:00", "17:30", "18:00"],
        ["18:30", "19:00", "19:30"]
    ]
    def __init__(
        self,
        text_data: dict
    ):
        self.text_data = text_data
    