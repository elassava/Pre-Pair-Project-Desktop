#This is the login file.
import csv

def load():
    infos_path = r"Info\login_info.csv"
    emails = [ ]
    passwords = [ ]

    with open(infos_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            emails.append(row['Email'])
            passwords.append(row['Password'])

    return dict(zip(emails, passwords))



def is_user(email, password):
    email_password_dict = load()
    if email in email_password_dict:
        user_password = password
        if user_password == email_password_dict[email]: 
            return True
        else:
            return False
    return False

def email_exist(email):
    email_password_dict = load()
    if email in email_password_dict:
        return True
    else:
        return False
    

def update_password(email, new_password):
    rows = []
    with open(r'Info\login_info.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email:
                row[1] = new_password
            rows.append(row)
            



    with open(r'Info\login_info.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return True
