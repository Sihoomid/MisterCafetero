import datetime
from os import path
from subprocess import check_output
from time import sleep

import db_handler

print("Mister Cafetero\n----\nEjecutor de tareas programadas\n--------")
print("\nPreparando café...\n")

dbHandler = db_handler.Handler("tasks.sqlite3")
if not path.exists("tasks.sqlite3"):
    dbHandler.create_database()

while True:
    sleep(5)
    dbHandler.unmark_tasks()
    pendTasks = dbHandler.pending_tasks()
    
    for t in pendTasks:
        print("¡Un café! --> El {} a las {} lanza \"{}\""
              .format(datetime.datetime.today().strftime("%d/%m/%y"),
                      datetime.datetime.today().strftime("%H:%M:%S"),
                      t.name))
        # Lanza la tarea.
        okResult = True
        msgResult = "Bien tirado"
        statusResult = "OK"
        try:
            check_output(t.command, shell=False)
        except:
            okResult = False
            msgResult = "Error lanzando la tarea"
            statusResult = "ERROR"
        dbHandler.insert_new_log(t.id, msgResult, statusResult)
        # Deja la tarea como ya lanzada en el programador.
        dbHandler.mark_launched_task(t.id)
