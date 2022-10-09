import configparser
import getpass
from passlib.hash import md5_crypt


def getpassword():
    while True:
        password = getpass.getpass(prompt="Password: ")
        confirm_pass = getpass.getpass(prompt="Confirm Password: ")
        if (password == confirm_pass):
            break
        else:
            print("Passwords did not match")
            continue
    hashed_pass = md5_crypt.hash(password)
    return hashed_pass


def register():
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini')
    sections = config_parser.sections()
    while True:
        while True:
            username = input("Enter new username: ")
            if (username in sections):
                print("Username in use")
                continue
            break
        user_type = input("Select user type. \n 1-Patient \n 2-Staff \n")
        if (user_type == "1"):
            user_type = "patient"
            privilege_level = "p0"
        elif (user_type == "2"):
            while True:
                staff_type = input(
                    "Select staff type \n1-Doctor\n2-Lab\n3-Pharmacy\n4-Admin\n")
                if staff_type == "1":
                    verificiation = input("Enter code\n")
                    if verificiation == "dct101":
                        user_type = "doctor"
                        privilege_level = "p1"
                        break
                    else:
                        print("The code you entered is wrong")
                        continue
                elif staff_type == "2":
                    verificiation = input("Enter code\n")
                    if verificiation == "lab101":
                        user_type = "lab"
                        privilege_level = "p2"
                        break
                    else:
                        print("The code you entered is wrong")
                        continue
                elif staff_type == "3":
                    verificiation = input("Enter code\n")
                    if verificiation == "phm101":
                        user_type = "pharmacy"
                        privilege_level = "p3"
                        break
                    else:
                        print("The code you entered is wrong")
                        continue
                elif staff_type == "4":
                    verificiation = input("Enter code\n")
                    if verificiation == "adm101":
                        user_type = "admin"
                        privilege_level = "p4"
                        break
                    else:
                        print("The code you entered is wrong")
                        continue
                else:
                    print("Please enter a valid input")
                    continue
        else:
            print("Invalid Input")
            continue
        break
    hashed_password = getpassword()
    config_parser = configparser.ConfigParser()
    config_parser[username] = {"password": hashed_password,
                               "user_type": user_type,
                               "privilege_level": privilege_level}
    config_file = open('config.ini', 'a')
    config_parser.write(config_file)
    config_file.close()
    print("Registration Successful")


def login():
    while True:
        username = input("Username: ")
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini')
        sections = config_parser.sections()
        if (username in sections):
            while True:
                password = getpass.getpass(prompt="Password: ")
                stored_password = config_parser.get(username, "password")
                if md5_crypt.verify(password, stored_password):
                    session(username)
                    break
                else:
                    print("Wrong password")
                    continue
            break
        else:
            print("Invalid username")
            continue


def view(patient_username, privilege):
    config_parser = configparser.ConfigParser()
    config_parser.read("data.ini")
    while True:
        record = input(
            "What do you want to view\n 1-personal details \n 2-sickness details \n 3-drug prescriptions \n 4-lab test prespriptions\n 5-exit\n")
        if record == "1":
            print(config_parser.get(patient_username, "personal_details"))
            continue
        elif record == "2":
            print(config_parser.get(patient_username, "sickness_details"))
            continue
        elif record == "3":
            if (privilege != 'p2'):
                print(config_parser.get(patient_username, "drug_prescription"))
            else:
                print('No access')
            continue
        elif record == "4":
            if (privilege != 'p3'):
                print(config_parser.get(patient_username, "lab_prescription"))
            else:
                print('No access')
            continue
        elif record == "5":
            break
        else:
            print("Invalid input")


def edit(patient_username, privilege):
    config_parser = configparser.ConfigParser()
    config_parser.read("data.ini")
    while True:
        record = input(
            "What do you want to edit\n 1-personal details \n 2-sickness details \n 3-drug prescriptions \n 4-lab test prespriptions\n 5-exit\n")
        if record == "1":
            if privilege == "p4":
                print('Current Details: ', config_parser.get(
                    patient_username, "personal_details"))
                new_details = input("Enter new details: ")
                config_parser.set(patient_username,
                                  "personal_details", new_details)
                print('New Details: ', config_parser.get(
                    patient_username, 'personal_details'))
            else:
                print('No access')
        elif record == "2":
            if privilege == "p1":
                print('Current Details: ', config_parser.get(
                    patient_username, "sickness_details"))
                new_details = input("Enter new details: ")
                config_parser.set(patient_username,
                                  "sickness_details", new_details)
                print('New Details: ', config_parser.get(
                    patient_username, "sickness_details"))
            else:
                print('No access')
        elif record == "3":
            if privilege == "p1":
                print('Current prescription: ', config_parser.get(
                    patient_username, "drug_prescription"))
                new_prescription = input("Enter new prescription: ")
                config_parser.set(patient_username,
                                  "drug_prescription", new_prescription)
                print('New prescription: ', config_parser.get(
                    patient_username, "drug_prescription"))
            else:
                print('No access')
        elif record == "4":
            if privilege == "p1":
                print('Current prescription: ', config_parser.get(
                    patient_username, "lab_prescription"))
                new_prescription = input("Enter new prescription: ")
                config_parser.set(patient_username,
                                  "lab_prescription", new_prescription)
                print('New prescription: ', config_parser.get(
                    patient_username, "lab_prescription"))
            else:
                print('No access')
        elif record == "5":
            break
        else:
            print("Invalid input")
    config_parser.write(open('data.ini', 'w'))


def session(username):
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini')
    privilege_level = config_parser.get(username, "privilege_level")
    if privilege_level == "p0":
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini')
        sections = config_parser.sections()
        if username in sections:
            view(username, privilege_level)
        else:
            print("No records currently")
    else:
        while True:
            action = input("Press 1 to view/edit\nPress any other to exit\n")
            if action == "1":
                config_parser = configparser.ConfigParser()
                config_parser.read('config.ini')
                sections = config_parser.sections()
                while True:
                    task = input(
                        "What do you want to do\n 1-View details\n 2-Edit details\n 3-Exit\n")
                    if task == "1" or task == "2":
                        patient_username = input("Enter patient username: ")
                        if patient_username in sections:
                            if task == "1":
                                view(patient_username, privilege_level)
                                break
                            elif task == "2":
                                edit(patient_username, privilege_level)
                                break
                        else:
                            print("No records currently")
                            continue
                    elif task == "3":
                        break
                    else:
                        print("Invalid Input")
                        continue
            else:
                break


print("Welcome to hospital system")
while True:
    activity = input(
        "What do you need to do?\n 1-Login\n 2-Register\n 3-Exit\n")
    if activity == "1":
        login()
    elif activity == "2":
        register()
    elif activity == "3":
        break
    else:
        print("Invalid input")
        continue
