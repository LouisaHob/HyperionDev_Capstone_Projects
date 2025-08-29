"""
This program is a simple task manager that allows users to log in, add tasks, and view tasks.
Start the program and load the list of users (names and passwords) from a file.
Ask the user to log in by entering their username and password.
If the login is successful, show a menu of options based on who logged in.
If the user is an admin, they can:
    - Add a new user to the system.
    - Add a new task for someone to do.
    - See all the tasks.
    - See statistics (like how many tasks and users there are).
    - Exit the program.
If the user is not an admin, they can:
    - Add a new task for themselves or others.
    - See all tasks or just their own tasks.
    - Exit the program.
If the user chooses to add a new user (admin only), ask for a username nd password, 
then save it in the user list.
If the user chooses to add a task, ask for details (who the task is for, title, description, 
due date) and save the task in the task list.
If the user wants to see tasks, show a list of all tasks or just the tasks assigned to them.
If the admin wants statistics, show how many tasks are in the system and how many users are 
registered.
If the user types something that is not an option, ask them to try again.
"""

# =====importing libraries===========
from datetime import datetime

# ==== Login Section ====
def load_users():
    users = {}
    try:
        with open("user.txt", "r") as f:
            for line in f:
                try:
                    username, password = line.strip().split(', ')
                    users[username] = password
                except ValueError:
                    print(f"Skipping malformed line in user.txt: {line.strip()}")
    except FileNotFoundError:
        print("Error: user.txt file not found. Please make sure it exists.")
    return users


def login(users):
    while True:
        username = input("Username: ")
        password = input("Password: ")
        if username in users and users[username] == password:
            print("Login successful!\n")
            return username
        else:
            print("Invalid username or password. Please try again.\n")


def register_user(users):
    new_username = input("Enter new username: ")
    if new_username in users:
        print("Username already exists.\n")
        return
    new_password = input("Enter new password: ")
    confirm_password = input("Confirm password: ")
    if new_password == confirm_password:
        try:
            with open("user.txt", "a") as f:
                f.write(f"\n{new_username}, {new_password}")
            print("User registered successfully.\n")
        except Exception as e:
            print(f"Failed to register user: {e}")
    else:
        print("Passwords do not match. User not registered.\n")


def add_task():
    assigned_to = input("Enter the username of the person "
                        "the task is assigned to: ")
    title = input("Enter the title of the task: ")
    description = input("Enter the description of the task: ")
    due_date = input("Enter the due date of the task (e.g. 20 Oct 2019): ")
    assigned_date = datetime.now().strftime("%d %b %Y")
    task_complete = "No"

    try:
        with open("tasks.txt", "a") as f:
            f.write(
                f"\n{assigned_to}, {title}, {description}, "
                f"{assigned_date}, {due_date}, {task_complete}"
            )
        print("Task added successfully.\n")
    except Exception as e:
        print(f"Error adding task: {e}")


def view_all_tasks():
    print("\nAll Tasks:\n")
    try:
        with open("tasks.txt", "r") as f:
            for line in f:
                try:
                    user, title, desc, assigned, due, complete = \
                        line.strip().split(", ")
                    print(
                        f"Task: {title}\n"
                        f"Assigned to: {user}\n"
                        f"Date Assigned: {assigned}\n"
                        f"Due Date: {due}\n"
                        f"Task Complete? {complete}\n"
                        f"Description: {desc}\n"
                    )
                except ValueError:
                    print(f"Skipping malformed task line: {line.strip()}")
    except FileNotFoundError:
        print("Error: tasks.txt file not found.\n")


def view_my_tasks(logged_in_user):
    print(f"\nTasks assigned to {logged_in_user}:\n")
    try:
        with open("tasks.txt", "r") as f:
            for line in f:
                try:
                    user, title, desc, assigned, due, complete = \
                        line.strip().split(", ")
                    if user == logged_in_user:
                        print(
                            f"Task: {title}\n"
                            f"Assigned to: {user}\n"
                            f"Date Assigned: {assigned}\n"
                            f"Due Date: {due}\n"
                            f"Task Complete? {complete}\n"
                            f"Description: {desc}\n"
                        )
                except ValueError:
                    print(f"Skipping malformed task line: {line.strip()}")
    except FileNotFoundError:
        print("Error: tasks.txt file not found.\n")


def display_statistics():
    try:
        with open("tasks.txt", "r") as task_file:
            tasks = task_file.readlines()
            task_count = len(tasks)
    except FileNotFoundError:
        print("Error: tasks.txt not found.")
        task_count = 0

    try:
        with open("user.txt", "r") as user_file:
            users = user_file.readlines()
            user_count = len(users)
    except FileNotFoundError:
        print("Error: user.txt not found.")
        user_count = 0

    print("\nStatistics:")
    print(f"Total number of tasks: {task_count}")
    print(f"Total number of users: {user_count}\n")


# ===== Main program =====
users = load_users()
logged_in_user = login(users)

while True:
    if logged_in_user == 'admin':
        menu = input('''Select one of the following options:
r  - register a user
a  - add task
va - view all tasks
vm - view my tasks
ds - display statistics
e  - exit
: ''').lower()
    else:
        menu = input('''Select one of the following options:
a  - add task
va - view all tasks
vm - view my tasks
e  - exit
: ''').lower()

    if menu == 'r':
        if logged_in_user == 'admin':
            register_user(users)
            users = load_users()  
        else:
            print("Only the admin can register new users.\n")

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all_tasks()

    elif menu == 'vm':
        view_my_tasks(logged_in_user)

    elif menu == 'ds' and logged_in_user == 'admin':
        display_statistics()

    elif menu == 'e':
        print('Goodbye!!!')
        break

    else:
        print("You have entered an invalid input. Please try again\n")