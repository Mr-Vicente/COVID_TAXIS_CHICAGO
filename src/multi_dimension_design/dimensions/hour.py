

class Hour():
    original_key: str
    hour: int
    minute: int
    is_rush_hour: bool

    def __init__(self, original_key, hour, minute):
        self.original_key = original_key
        self.hour = hour
        self.minute = minute

    def is_rush_hour(self, hour):
        return (hour >= 7 and hour <= 10) or (hour >= 17 and hour <= 19)