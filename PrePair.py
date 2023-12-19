# IMPORT STATEMENTS #

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QStackedWidget, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth import jwt
from google.oauth2 import service_account
#from google.auth import service_account
from google.cloud import logging_v2
from unidecode import unidecode

import random
import csv
import login
import register
import mailer
import add_game
import game_picker
from Design import stylesheet

SCOPES = ["https://www.googleapis.com/auth/logging.write"]

class LoginScreen(QWidget):


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pre-Pair")
        self.game_chooser_app = None
        self.stacked_widget = QStackedWidget(self)
        
        # Initialize pages.
        self.init_login_page() # Index 0
        self.init_create_account_page() # Index 1
        self.init_verification_page() # Index 2
        self.init_main_page() #Index 3 
        self.init_forget_password_page() #Index 4
        self.init_profile_page() # Index 5 
        self.init_change_password_page() #Index 6
        self.init_forget_password_email_page() # Index 7 
        self.init_add_new_game_page() # Index 8
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        
        # Initialize variables.
        self.email = ""
        self.username = ""
        self.played_game = ""
        self.current_verification_code = ""
        self.keyword = ""
        self.logging_client = self.setup_logging_client() # Set up the logging client
        
        # Set application-wide stylesheet
        self.setStyleSheet(stylesheet.get_stylesheet())
        self.setGeometry(500, 500, 500, 500)
        icon = QIcon(r"Design\prepair.jpg")
        self.setWindowIcon(icon)
        
# INITIALIZING PAGE FUNCTIONS - ORDERED BY INDEXES #  

    def init_login_page(self): # INDEX 0
        login_page = QWidget()

        email_label = QLabel('Email:', login_page)
        self.email_entry = QLineEdit(login_page)

        password_label = QLabel('Password:', login_page)
        self.password_entry = QLineEdit(login_page)
        self.password_entry.setEchoMode(QLineEdit.Password)

        login_button = QPushButton('Login', login_page)
        login_button.clicked.connect(self.check_login)

        create_account_button = QPushButton('Create New Account', login_page)
        create_account_button.clicked.connect(self.show_create_account_page)

        forget_password_button = QPushButton('Forgot My Password', login_page)
        forget_password_button.clicked.connect(self.show_reset_password_email_page)

        google_button = QPushButton('Login with Google', self)
        google_button.clicked.connect(self.authenticate_with_google)

        
        layout = QVBoxLayout(login_page)
        layout.addWidget(email_label)
        layout.addWidget(self.email_entry)
        layout.addWidget(password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(login_button)
        layout.addWidget(create_account_button)
        layout.addWidget(forget_password_button)

        layout.addWidget(google_button)
        
        self.stacked_widget.addWidget(login_page)
        

    def init_create_account_page(self): # INDEX 1 
        create_account_page = QWidget()

        create_account_label = QLabel('Please enter new account information:', create_account_page)

        self.create_account_username_label = QLabel('Username:', create_account_page)
        self.create_account_username_entry = QLineEdit(create_account_page)
        
        self.create_account_email_label = QLabel('Email:', create_account_page)
        self.create_account_email_entry = QLineEdit(create_account_page)
        
        self.create_account_password_label = QLabel('Password:', create_account_page)
        self.create_account_password_entry = QLineEdit(create_account_page)
        self.create_account_password_entry.setEchoMode(QLineEdit.Password)

        confirm_password_label = QLabel('Enter the password again:', create_account_page)
        self.confirm_password_entry = QLineEdit(create_account_page)
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)

        self.oyun_label = QLabel('Enter the game you play most:', create_account_page)
        self.oyun_entry = QLineEdit(create_account_page)
        
        create_account_button = QPushButton('Create', create_account_page)
        create_account_button.clicked.connect(self.create_account)
        
        back_button = QPushButton('Back', create_account_page)
        back_button.clicked.connect(self.logout)

        layout = QVBoxLayout(create_account_page)
        layout.addWidget(create_account_label)
        layout.addWidget(self.create_account_username_label)
        layout.addWidget(self.create_account_username_entry)
        
        layout.addWidget(self.create_account_email_label)
        layout.addWidget(self.create_account_email_entry)

        layout.addWidget(self.create_account_password_label)
        layout.addWidget(self.create_account_password_entry)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_entry)
        layout.addWidget(self.oyun_label)
        layout.addWidget(self.oyun_entry)
        layout.addWidget(create_account_button)
        layout.addWidget(back_button)
        
        self.stacked_widget.addWidget(create_account_page)

    def init_verification_page(self): #INDEX 2
        verification_page = QWidget()

        verification_label = QLabel('Please Enter the Verification Code:', verification_page)

        self.verification_entry = QLineEdit(verification_page)

        verify_button = QPushButton('Verify', verification_page)
        verify_button.clicked.connect(self.verify_code)

        back_button = QPushButton('Back', verification_page)
        back_button.clicked.connect(self.logout)
        
        layout = QVBoxLayout(verification_page)
        layout.addWidget(verification_label)
        layout.addWidget(self.verification_entry)
        layout.addWidget(verify_button)
        layout.addWidget(back_button)

        self.stacked_widget.addWidget(verification_page)
    
    def init_main_page(self): #INDEX 3
        main_page = QWidget()

        main_label = QLabel('Home Page', main_page)
        main_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        suggest_button = QPushButton('Suggest Players', main_page)
        suggest_button.clicked.connect(self.suggest_player)

        search_button = QPushButton('Search Games', main_page)
        search_button.clicked.connect(self.perform_search)
        
        profile_button = QPushButton('Profile', main_page)
        profile_button.clicked.connect(self.show_profile_page)

        logout_button = QPushButton('Log Out', main_page)
        logout_button.clicked.connect(self.logout)

        layout = QVBoxLayout(main_page)
        layout.addWidget(main_label)
    
        layout.addWidget(suggest_button)
        layout.addWidget(search_button)
        layout.addWidget(profile_button)
        layout.addWidget(logout_button)
        

        self.stacked_widget.addWidget(main_page)
        
    def init_forget_password_page(self): #INDEX 4
        forget_password_page = QWidget()
        self.keyword = "forget"

        new_password_label = QLabel('New Password:', forget_password_page)
        self.new_password_entry = QLineEdit(forget_password_page)
        self.new_password_entry.setEchoMode(QLineEdit.Password)

        confirm_new_password_label = QLabel('Verify New Password:', forget_password_page)
        self.confirm_new_password_entry = QLineEdit(forget_password_page)
        self.confirm_new_password_entry.setEchoMode(QLineEdit.Password)

        reset_password_button = QPushButton('Reset the Password', forget_password_page)
        reset_password_button.clicked.connect(self.reset_password)

        back_button = QPushButton('Back', forget_password_page)
        back_button.clicked.connect(self.logout)
        
        layout = QVBoxLayout(forget_password_page)
        layout.addWidget(new_password_label)
        layout.addWidget(self.new_password_entry)
        layout.addWidget(confirm_new_password_label)
        layout.addWidget(self.confirm_new_password_entry)
        layout.addWidget(reset_password_button)
        layout.addWidget(back_button)

        self.stacked_widget.addWidget(forget_password_page)
    
    def init_profile_page(self): #INDEX 5
        profile_page = QWidget()

        profile_label = QLabel('Profile', profile_page)
        profile_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        layout = QVBoxLayout(profile_page)
        layout.addWidget(profile_label)
        
        add_game_button = QPushButton('Add Game', profile_page)
        add_game_button.clicked.connect(self.show_add_game_page)
        
        change_password_button = QPushButton('Change My Password', profile_page)
        change_password_button.clicked.connect(self.show_change_password_page)
        
        back_button = QPushButton('Back', profile_page)
        back_button.clicked.connect(self.show_home_page)
        
        layout.addWidget(add_game_button)
        layout.addWidget(change_password_button)
        layout.addWidget(back_button)
        
        self.stacked_widget.addWidget(profile_page)
        
        
    def init_change_password_page(self): #INDEX 6
        change_password_page = QWidget()
        self.keyword = "change"
        
        previous_password_label = QLabel('Previous Password:', change_password_page)
        self.previous_password_entry = QLineEdit(change_password_page)
        self.previous_password_entry.setEchoMode(QLineEdit.Password)

        new1_password_label = QLabel('New Password:', change_password_page)
        self.new1_password_entry = QLineEdit(change_password_page)
        self.new1_password_entry.setEchoMode(QLineEdit.Password)

        confirm1_new_password_label = QLabel('Verify New Password:', change_password_page)
        self.confirm1_new_password_entry = QLineEdit(change_password_page)
        self.confirm1_new_password_entry.setEchoMode(QLineEdit.Password)

        reset_password1_button = QPushButton('Reset the Password', change_password_page)
        reset_password1_button.clicked.connect(self.update_password)

        back1_button = QPushButton('Back', change_password_page)
        back1_button.clicked.connect(self.show_profile_page)
        
        layout = QVBoxLayout(change_password_page)
        layout.addWidget(previous_password_label)
        layout.addWidget(self.previous_password_entry)
        layout.addWidget(new1_password_label)
        layout.addWidget(self.new1_password_entry)
        layout.addWidget(confirm1_new_password_label)
        layout.addWidget(self.confirm1_new_password_entry)
        layout.addWidget(reset_password1_button)
        layout.addWidget(back1_button)

        self.stacked_widget.addWidget(change_password_page)
    
    def init_forget_password_email_page(self): #INDEX 7
        forget_password_email_page = QWidget()
        self.keyword = "forget"
        
        email_label = QLabel('Email:', forget_password_email_page)
        self.reset_password_email_entry = QLineEdit(forget_password_email_page)

        send_verif_button = QPushButton('Send verification mail', forget_password_email_page)
        send_verif_button.clicked.connect(self.check_email)
        
        back_button = QPushButton('Back', forget_password_email_page)
        back_button.clicked.connect(self.logout)
        
        layout = QVBoxLayout(forget_password_email_page)
        layout.addWidget(email_label)
        layout.addWidget(self.reset_password_email_entry)
        layout.addWidget(send_verif_button)
        layout.addWidget(back_button)

        self.stacked_widget.addWidget(forget_password_email_page)
        
        
    def init_add_new_game_page(self): #INDEX 8
        add_game_page = QWidget()
        
        add_game_label = QLabel('Add Game:', add_game_page)
        self.add_game_entry = QLineEdit(add_game_page)


        add_new_game_button = QPushButton('Add the Game', add_game_page)
        add_new_game_button.clicked.connect(self.add_new_game)

        back2_button = QPushButton('Back', add_game_page)
        back2_button.clicked.connect(self.show_profile_page)
        
        layout = QVBoxLayout(add_game_page)
        layout.addWidget(add_game_label)
        layout.addWidget(self.add_game_entry)
        layout.addWidget(add_new_game_button)
        layout.addWidget(back2_button)

        self.stacked_widget.addWidget(add_game_page)
        
# PRE-PAIR.PY DA TANIMLANMIS FONKSIYONLAR #

    def add_new_game(self, game_name): # Adds given game to players profile.
        game_name = self.add_game_entry.text()
        
        if add_game.add_game(self.username, game_name):
            QMessageBox.information(self, 'Successful', 'Game is succesfully added to your profile.')
            
        else:
            QMessageBox.information(self, 'Failed', 'The game could not be added to your profile.')


    def check_login(self): # Login system.
        self.keyword = "login"
        current_index = self.stacked_widget.currentIndex()
        login_page = self.stacked_widget.widget(current_index)

        email = self.email_entry.text()
        self.email = email
        password = self.password_entry.text()
        
        self.username = self.get_username(email=email)
        self.played_games = self.get_user_games(self.username)

        if self.validate_login(email, password):
            self.current_verification_code = self.send_verification_email(email)
            QMessageBox.information(self, 'Successful', 'Please enter the code sent to your email to log into your account.')
            self.stacked_widget.setCurrentIndex(2)  # Doğrulama sayfasına geçiş yap
            self.email_entry.clear()
            self.password_entry.clear()
            
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid Mail or Password.')
            
        
    def check_email(self): # Email control system.
        self.keyword = "forget"
        email = self.reset_password_email_entry.text()

        if self.validate_mail(email):
            self.current_verification_code = self.send_verification_email(email)
            QMessageBox.information(self, 'Successful', 'Please enter the code sent to change your password.')
            self.stacked_widget.setCurrentIndex(2)  # Doğrulama sayfasına geçiş yap
            
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid mail.')
            
            
    def create_account(self): # Create an account system.
        self.username = self.create_account_username_entry.text()
        email = self.create_account_email_entry.text()
        password = self.create_account_password_entry.text()
        confirm_password = self.confirm_password_entry.text()
        self.played_game = self.oyun_entry.text()
        
        if password == confirm_password:
            # Add new account informations to the CSV file
            if register.register(email=email, password=password, username=self.username):
                QMessageBox.information(self, 'Successful', 'New account created.')
                
                add_game.add_game(self.username,self.played_game)
                
                self.stacked_widget.setCurrentIndex(0)  # Giriş ekranına geri dön
                
                self.create_account_username_entry.clear()
                self.create_account_email_entry.clear()
                self.create_account_password_entry.clear()
                self.confirm_password_entry.clear()
                self.oyun_entry.clear()
                
            else:
                QMessageBox.warning(self, 'Failed', 'This user already exists.')

        else:
            QMessageBox.warning(self, 'Failed', 'The passwords does not match.')


    def verify_code(self): # Verification system.
        entered_code = self.verification_entry.text()
        correct_code = self.current_verification_code

        if entered_code == correct_code:
            QMessageBox.information(self, 'Successful', 'Verification successful.')
            
            if (self.keyword == "forget"):
                self.stacked_widget.setCurrentIndex(4)
                
            elif (self.keyword == "change"):
                self.stacked_widget.setCurrentIndex(5)
                
            elif (self.keyword == "login"):
                self.stacked_widget.setCurrentIndex(3)
                
            self.verification_entry.clear()
            
        else:
            QMessageBox.warning(self, 'Failed', 'Invalid verification code.')
    
    def get_user_games(self, username, file_path=r"Info\users.csv"):
        try:
            with open(file_path, mode='r', newline='') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if row['Username'] == username:
                        # Oyunları virgülle ayrılmış stringi virgüle göre böler ve temizler
                        games = [game.strip() for game in row['Game'].split(',')]
                        return games
                    
        except FileNotFoundError:
            print("Error: File not found.")
        
        return None
            
    # Get user's username via given email.
    def get_username(self, email):
            try:
                with open(r"Info\login_info.csv", 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row['Email'] == email:
                            return row['Username']
                        
            except FileNotFoundError:
                print("Error: File not found.")
                
            return None
        
    def suggest_player(self): # Player suggestion system.
        suggested_players = []
        user_games = self.get_user_games(self.username)

        if user_games:
            with open(r"Info\users.csv", 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Username'] != self.username:
                        common_games = set(user_games) & set(row['Game'].split(','))
                        if common_games:
                            suggested_players.append(row['Username'])
            
            if len(suggested_players) == 0:
                QMessageBox.information(self, 'Suggestions', 'No matching players were found.')
                
            else:
                QMessageBox.information(self, 'Suggestions', 'You matched with these players based on the games you play: ' + ', '.join(map(str, suggested_players)))
                
        else:
            QMessageBox.information(self, 'Error', 'User not found or played games are not in the specified format.')

        
    def reset_password(self): # Password changing system - for forget case.
        email = self.reset_password_email_entry.text()
        new_password = self.new_password_entry.text()

        with open(r'Info\login_info.csv', 'r') as file: # Email Check
            reader = csv.reader(file)
            email_found = False
            for row in reader:
                if row[0] == email:
                    email_found = True
                    if row[1] == '':  # If the password field is empty
                        QMessageBox.warning(self, 'Error', 'Email address found but password field is empty.')
                        return
                    
                    if row[1] == new_password:
                        QMessageBox.warning(self, 'Error', 'Existing password cannot be the same as new password.')
                        return

                    # Update the new password in CSV file
                    if login.update_password(email, new_password):
                        QMessageBox.information(self, 'Successful', 'Password reset successfully.')
                        self.stacked_widget.setCurrentIndex(0)  # Go back to login screen
                        return
                    else:
                        QMessageBox.warning(self, 'Error', 'Password could not be reset.')
                        return

            if not email_found:
                QMessageBox.warning(self, 'Error', 'The email address entered was not found.')
                
        
    def update_password(self): # Password updating system.
            email = self.email
            new_password = self.new1_password_entry.text()
            prev_password = self.previous_password_entry.text()

            with open(r'Info\login_info.csv', 'r') as file:  # Email Check
                reader = csv.reader(file)
                email_found = False
                for row in reader:
                    if row[0] == email:
                        email_found = True
                        if row[1] == '':  # If the password field is empty
                            QMessageBox.warning(self, 'Error', 'Email address found but password field is empty.')
                            return

                        # Email and Password Check
                        if row[1] != prev_password:
                            QMessageBox.warning(self, 'Error', 'Your previous password is wrong.')
                            return
                        
                        if row[1] == new_password:
                            QMessageBox.warning(self, 'Error', 'Existing password cannot be the same as new password.')
                            return

                        # Update the new password in CSV file
                        if login.update_password(email, new_password):
                            QMessageBox.information(self, 'Successful', 'Password reset successfully.')
                            self.stacked_widget.setCurrentIndex(5)  # Go back to login screen
                            return
                        else:
                            QMessageBox.warning(self, 'Error', 'Password could not be reset.')
                            return

                if not email_found:
                    QMessageBox.warning(self, 'Error', 'The email address entered was not found.')
        
# GOOGLE AUTH SYSTEM FUNCTIONS #
    def email_exists_in_csv(self, email):
        try:
            with open(r"Info\login_info.csv", 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == email:
                        return True
                    
        except FileNotFoundError:
            pass

        return False
    
    def save_email_to_csv(self, email, password, username):
        if not self.email_exists_in_csv(email):
            print("yokki")
            try:
                with open(r"Info\login_info.csv", 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([email, password, username])
            
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'An error occurred: {str(e)}')
                
        else:
            pass

        
    def authenticate_with_google(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_673547085759-rhljrpugrrto2s8rakl4tj9gn3g0gb68.apps.googleusercontent.com.json',
            scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid'],
        )
        credentials = flow.run_local_server(port=0)
        id_token = credentials.id_token
        decoded_token = jwt.decode(id_token, verify=False)
        #print(decoded_token)
        #print(decoded_token.keys())
        self.log_entry("User logged in successfully", severity="INFO")
    
        first_name = self.convert_to_ascii(decoded_token.get('given_name'))
        self.email = decoded_token.get('email')
        
        if not self.email_exists_in_csv(self.email):
            if "family_name" in decoded_token.keys():
                last_name = self.convert_to_ascii(decoded_token.get('family_name'))
                username =f"{first_name.replace(' ','_')}_{last_name}_" + str(random.randint(0,99))
            else:
                username = f"{first_name.replace(' ','_')}_" + str(random.randint(0,99))
        else:
            username = self.get_username(self.email)
        self.username = username
        self.save_email_to_csv(decoded_token.get('email'),decoded_token.get("sub"),username)
        self.show_home_page()

    def log_entry(self, message, severity="INFO"):
        # Add log entry to Cloud Logging
        resource = {"type": "global", "labels": {"project_id": "pre-pair"}}
        log_name = "pre-pair-logs"
        logger = self.logging_client.logger(log_name)
        logger.log_text(message, severity=severity, resource=resource)
        

    def setup_logging_client(self):
        credentials = service_account.Credentials.from_service_account_file(
            'pre-pair-808d818371a1.json',
            scopes=SCOPES,
        )
        return logging_v2.Client(credentials=credentials)

           
# IMPORT ILE BASKA .PY DOSYASINDAN CAGIRILAN FONKSIYONLAR  #
    def perform_search(self):
        game_picker.run()
    
    def validate_login(self, email, password):
        return login.is_user(email, password)
    
    def validate_mail(self, email):
        return login.email_exist(email)

    def send_verification_email(self, email):
        return mailer.mail_to(email=email)
    
    def convert_to_ascii(self,text):
        return unidecode(text)
    
# PAGE INDEXES & SHOW FUNCTIONS #
    def logout(self):
        self.stacked_widget.setCurrentIndex(0)  # Login page index = 0.
        
    def show_create_account_page(self):
        self.stacked_widget.setCurrentIndex(1) # Create account page index = 1.
    
    def show_verify_code_page(self):
        self.stacked_widget.setCurrentIndex(2) # Code verification page index = 2.
        
    def show_home_page(self):
        self.stacked_widget.setCurrentIndex(3)  # Home page index = 3.
    
    def show_reset_password_page(self):  
        self.stacked_widget.setCurrentIndex(4) # Reset password page index = 4.
    
    def show_profile_page(self):
        self.stacked_widget.setCurrentIndex(5)  # Profile page index = 5.
    
    def show_change_password_page(self):
        self.stacked_widget.setCurrentIndex(6) # Change password page index = 6.
        
    def show_reset_password_email_page(self):
        self.stacked_widget.setCurrentIndex(7) # Email verif page for resetting password page index = 7.
        
    def show_add_game_page(self):
        self.stacked_widget.setCurrentIndex(8) # Adding games page index = 8.
                 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_screen = LoginScreen()
    login_screen.show()
    sys.exit(app.exec_())
