import csv
import validate_email

infos_path = r"Info\login_info.csv"
users_path = r"Info\users.csv"


class UsernameTakenError(Exception):
    pass

def load():
    users = []

    with open(infos_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            users.append({
                'Email': row['Email'],
                'Password': row['Password'],
                'Username': row.get('Username', '')  # If 'Username' is not present, default to an empty string
            })

    return users

def register(username, email, password):
    user_list = load()

    # Validate email
    if not validate_email.validate_email(email):
        return False

    # Validate username
    if not username or any(user['Username'] == username for user in user_list):
        return False
    # Validate password (you can add validation logic here)
    
    if any(user['Email'] == email for user in user_list):
        return False


    # If all validations pass, proceed with registration
    with open(infos_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Email', 'Password', 'Username']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'Email': email,
            'Password': password,
            'Username': username
        })   
                 
    return True
