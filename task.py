import datetime

class Task:
    def __init__(self) -> None:
        self.id = 0
        self.name = ""
        self.command = ""
        self.days = ""
        self.start_time = datetime.time()
        self.active = False