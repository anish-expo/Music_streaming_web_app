#Backend/schedule_task.py

from tasks import daily_reminder
a='ssss'
b = 'sub'
task = daily_reminder.delay(a, b)

print("task-id:", task.id)