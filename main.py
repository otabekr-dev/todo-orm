import sys
from getpass import getpass
from pprint import pprint

from pydantic import ValidationError
from passlib.context import CryptContext

from database import engine, Base, LocalSession
from models import User, Task
from schemas import UserRegister, UserLogin, TaskCreation

pwd_context = CryptContext(schemes=['bcrypt'])

Base.metadata.create_all(engine)


def register():
    first_name = input('Enter your first name: ')
    last_name = input('Enter your last name : ')
    email = input('Enter your email: ')
    password = getpass('Enter your password: ')

    try:
        user_data = UserRegister(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        hashed_password = pwd_context.hash(password)

        db = LocalSession()

        user = User(
            first_name = user_data.first_name,
            last_name = user_data.last_name,
            email = user_data.email,
            hashed_password = hashed_password 
        )

        db.add(user)
        db.commit()
        print('Successfully registered')


    except ValidationError as e:
        pprint(e.errors())

def login():
    email = input('Enter your email: ')
    password = getpass('Enter your password: ')

    try:
        user_data = UserLogin(
            email = email,
            password = password 
        )
    
        db = LocalSession()
        user = db.query(User).filter_by(email=user_data.email).first()

        is_valid = pwd_context.verify(user_data.password, user.hashed_password)
        if is_valid:
            print('Successfully logged in')
        
        db.close()
        return user

    except ValidationError as e:
        pprint(e.errors())



def show_tasks(user):
    db = LocalSession()

    task = db.query(Task).filter_by(user_id = user.user_id).all()

    if task:
        print(task)
    else:
        print("You don't have any task")

    db.close()

def add_task(user):
    name = input('Enter the task name: ')
    description = input('Enter the description: ')

    try:
        task_data = TaskCreation(name = name, description = description)

        db = LocalSession()
        task = Task(
            name = task_data.name,
            description = task_data.description,
            user_id = user.user_id
        )

        db.add(task)
        db.commit()
        db.close()
        print('Task is successfully added')

    except ValidationError as e:
        pprint(e.errors())

def main():
    user = None

    while True:

        if user:
            print('\n-----Menu-----\n')        
            print('1.My tasks')        
            print('2.Add task')        
            print('3.Log out')

            user_choice = input('Enter the number (1-3): ')

            if user_choice == '1':
                show_tasks(user)
            elif user_choice == '2':
                add_task(user)
            elif user_choice == '3':
                user = None
            else:
                print('Non existing option')      
        else:
            print('\n-----Menu-----\n')        
            print('1.Register')
            print('2.Log in')
            print('3.Log out')


            user_choice = input('Enter the number (1-3): ')

            if user_choice == '1':
                register()
            elif user_choice == '2':
                user = login()
            elif user_choice == '3':
                sys.exit()
            else:
                print('Non existing option')  

if __name__ == '__main__':
    main()                                      