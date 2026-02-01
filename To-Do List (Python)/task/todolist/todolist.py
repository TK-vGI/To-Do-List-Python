# Use a list of dictionaries (better for SQL integration later)
tasks_list = [{"id": 1, "task": "Do yoga"},
              {"id": 2, "task": "Make a breakfast"},
              {"id": 3, "task": "Learn the basics of SQL"},
              {"id": 4, "task": "Learn about ORM"}]

def main():
    print("Today:")
    for task in tasks_list:
        print(f"{task['id']}) {task['task']}")


if __name__ == "__main__":
    main()
