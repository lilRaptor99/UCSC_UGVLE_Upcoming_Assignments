import json


def get_username():
    try:
        f = open(".uname.json", "r")
        data = json.load(f)
        f.close()
        if(data["username"] == ""):
            raise ValueError
        return data["username"]

    # Username-password file not found or error parsing data - prompt user to enter login details
    except (FileNotFoundError, json.decoder.JSONDecodeError, ValueError) as e:
        username = input("Enter Username: ")
        save = input("Save username? (y/n): ")

        if(save == "y" or save == "Y"):
            f = open(".uname.json", "w")
            uname_pwd = {"username": username, "password": ""}
            json.dump(uname_pwd, f)
            f.close()
        return username

    except Exception as e:
        print("An error occurred - login.get_username")
        print(e)
        exit(0)


def get_password():
    try:
        f = open(".uname.json", "r")
        data = json.load(f)
        f.close()
        if(data["password"] == ""):
            raise ValueError
        return data["password"]

    # User didn't save username
    except FileNotFoundError as e:
        return input("Enter Password: ")

    # Password not saved in file
    except ValueError as e:
        password = input("Enter Password: ")
        save = input("Save password? (y/n): ")

        if(save == "y" or save == "Y"):
            f = open(".uname.json", "r")
            # # goto begining of file
            # f.seek(0)
            data = json.load(f)
            uname_pwd = {"username": data["username"], "password": password}
            f.close()
            f = open(".uname.json", "w")
            json.dump(uname_pwd, f)
            f.close()

        return password

    except Exception as e:
        print("An error occurred - login.get_password")
        print(e)
        exit(0)
