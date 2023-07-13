import datetime
import sqlite3

import task

class Handler:
    def __init__(self, path: str) -> None:
        self.database_path = path
    
    def create_database(self) -> None:
        con = sqlite3.connect(self.database_path)
        # Tabla schedule.
        con.execute("CREATE TABLE task"
                    " (id int,"
                    " name text,"
                    " command text,"
                    " days text,"
                    " start_time time,"
                    " active bool,"
                    " PRIMARY KEY (id))")
        # Tabla log.
        con.execute("CREATE TABLE log"
                    " (id int,"
                    " task_id int,"
                    " message text,"
                    " status text,"
                    " PRIMARY KEY (id))")
        con.close()

    def pending_tasks(self) -> "list[task.Task]":
        con = sqlite3.connect(self.database_path)
        cursor = con.execute("SELECT *"
                             " FROM task"
                             " WHERE days LIKE '%{}%'"
                             " AND start_time <= '{}'"
                             " AND active = 1".format(datetime.datetime.today().weekday(),
                                                      datetime.datetime.today().time()
                                                      .strftime("%H:%M:%S")))
        return_list = []
        for row in cursor.fetchall():
            t = task.Task()
            t.id = row[0]
            t.name = row[1]
            t.command = row[2]
            t.days = row[3]
            t.start_time = row[4]
            t.active = row[5]
            return_list.append(t)

        return return_list
