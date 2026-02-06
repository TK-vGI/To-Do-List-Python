from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer,primary_key=True,autoincrement=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.now, nullable=False)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

MAIN_MENU = """1) Today's tasks
2) Add a task
0) Exit"""

def user_input():
    return input()


def add_task():
    while True:
        print("\nEnter a task")
        t = input().strip()
        if t:
            break

    new_task = Task(task=t)
    session.add(new_task)
    session.commit()
    print("The task has been added!")
    print()


def today_task():
    print("\nToday:")
    tasks = session.query(Task).all()
    if not tasks:
        print("Nothing to do!\n")
        return
    for task in tasks:
        # Card might have been deleted earlier in this session
        if session.get(Task, task.id) is None:
            continue
        while True:
            # Keep when mapping: deadline = Column(DateTime, default=datetime.now)
            # ... and format only when displaying: deadline.strftime("%Y-%m-%d %H:%M")
            # print(f"{task.id}. {task.task} {task.deadline.strftime("%Y-%m-%d %H:%M")}")
            print(f"{task.id}. {task.task}")
            break
    print()
    return


def main():
    while True:
        print(MAIN_MENU)
        choice = user_input()

        if choice == "1":
            today_task()
        elif choice == "2":
            add_task()
        elif choice == "0":
            print("\nBye!")
            break
        else:
            print()
            print(f"{choice} is not an option\n")



if __name__ == "__main__":
    main()
