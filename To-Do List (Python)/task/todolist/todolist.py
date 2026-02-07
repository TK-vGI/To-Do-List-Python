from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, func
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today, nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

MAIN_MENU = """
1) Today's tasks
2) Week's tasks
3) All tasks
4) Add a task
0) Exit
""".strip()

# Helper functions
def format_day(date_obj):
    return f"{date_obj.strftime('%A')} {date_obj.day} {date_obj.strftime('%b')}"


def tasks_for_date(date_obj):
    """Return all tasks for a specific date."""
    date_str = date_obj.strftime("%Y-%m-%d")
    return session.query(Task).filter(func.date(Task.deadline) == date_str).all()


# Menu actions

def today_tasks():
    today = datetime.today().date()
    print(f"\nToday {today.day} {today.strftime('%b')}:")

    tasks = tasks_for_date(today)

    if not tasks:
        print("Nothing to do!\n")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task.task}")
    print()

def weeks_tasks():
    today = datetime.today().date()

    for offset in range(7):
        day = today + timedelta(days=offset)
        print(f"{format_day(day)}:")

        tasks = tasks_for_date(day)

        if not tasks:
            print("Nothing to do!\n")
            continue

        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.task}")
        print()

def all_tasks():
    print("\nAll tasks:")
    tasks = session.query(Task).order_by(Task.deadline).all()

    if not tasks:
        print("Nothing to do!\n")
        return

    for task in tasks:
        d = task.deadline
        print(f"{task.task}. {d.day} {d.strftime('%b')}")
    print()

def add_task():
    print("\nEnter a task")
    task_text = input().strip()

    print("Enter a deadline")
    while True:
        date_str = input().strip()
        try:
            deadline = datetime.strptime(date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD")

    new_task = Task(task=task_text, deadline=deadline)
    session.add(new_task)
    session.commit()

    print("The task has been added!\n")


# Main loop

def main():
    while True:
        print(MAIN_MENU)
        choice = input().strip()

        if choice == "1":
            today_tasks()
        elif choice == "2":
            weeks_tasks()
        elif choice == "3":
            all_tasks()
        elif choice == "4":
            add_task()
        elif choice == "0":
            print("\nBye!")
            break

if __name__ == "__main__":
    main()