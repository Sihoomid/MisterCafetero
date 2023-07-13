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
                    " launched bool,"
                    " PRIMARY KEY (id))")
        # Tabla log.
        con.execute("CREATE TABLE log"
                    " (id int,"
                    " task_id int,"
                    " message text,"
                    " status text,"
                    " PRIMARY KEY (id))")
        con.close()

    def insert_new_log(self, task_id: int, message: str, status: str) -> None:
        con = sqlite3.connect(self.database_path)
        cursor = con.execute("SELECT MAX(id) FROM log")
        row = cursor.fetchone()
        newindex = 1
        if row != None:
            if row[0] != None:
                newindex = int(str(row[0])) + 1
        cursor.close()
        con.execute(
            "INSERT INTO log (id, task_id, message, status) VALUES ({}, {}, '{}', '{}')".format(
            newindex,
            task_id,
            message.replace("'", "\""),
            status))
        con.commit()
        con.close()

    def mark_launched_task(self, task_id: int) -> None:
        con = sqlite3.connect(self.database_path)
        con.execute(
            "UPDATE task SET launched = 1 WHERE id = {}".format(task_id))
        con.commit()
        con.close()

    def pending_tasks(self) -> "list[task.Task]":
        con = sqlite3.connect(self.database_path)
        cursor = con.execute(
            "SELECT *"
            " FROM task"
            " WHERE days LIKE '%{}%'"
            " AND start_time <= '{}'"
            " AND active = 1"
            " AND launched = 0".format(datetime.datetime.today().weekday(),
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
        cursor.close()
        con.close()

        return return_list
    
    def unmark_tasks(self) -> None:
        con = sqlite3.connect(self.database_path)
        con.execute(
            "UPDATE task SET launched = 0 WHERE days NOT LIKE '%{}%'".format(
            datetime.datetime.today().weekday()
            )
        )
        con.execute(
            "UPDATE task SET launched = 0 WHERE days LIKE '%{}%' AND start_time > '{}'".format(
            datetime.datetime.today().weekday(),
            datetime.datetime.today().time()
            )
        )
        con.commit()
        con.close()        
