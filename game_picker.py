import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout, QListWidget, QDialog, QListWidgetItem
from PyQt5.QtCore import Qt
import pandas as pd
import csv

class GameChooserApp(QWidget):
    def __init__(self):
        super().__init__()

        # Read the CSV file
        self.filename = r'Info\games_info.csv'
        self.data = pd.read_csv(self.filename)

        self.selected_games = []  # List to store selected games

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.genre_label = QLabel('Choose Genre:')
        self.genre_dropdown = QComboBox()
        self.games_list = QListWidget()
        self.selected_games_label = QLabel('Selected Games: ')

        # Fill genre dropdown with all column names from CSV file
        self.genre_dropdown.addItems(self.data.columns.tolist())

        # Connect the slot for genre selection change
        self.genre_dropdown.currentIndexChanged.connect(self.update_game_list)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.genre_label)
        layout.addWidget(self.genre_dropdown)
        layout.addWidget(self.games_list)
        layout.addWidget(self.selected_games_label)

        # Set the main layout for the window
        self.setLayout(layout)

        # Set the window properties
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Game Chooser')

        # Connect game selection change event only once
        self.games_list.itemClicked.connect(self.add_to_selected_games)

        # Connect selected games label click event
        self.selected_games_label.mousePressEvent = self.show_selected_games

    def update_game_list(self):
        # Clear the current list
        self.games_list.clear()

        # Get the selected genre
        selected_genre = self.genre_dropdown.currentText()

        if selected_genre:
            # Get the games for the selected genre
            games = self.data[selected_genre].dropna().tolist()

            # Add games to the list, allowing only those not already selected
            for game in games:
                if game not in self.selected_games:
                    item = QListWidgetItem(game)
                    item.setFlags(item.flags() | Qt.ItemIsSelectable)
                    self.games_list.addItem(item)
        self.save_selected_games_to_csv()

    def add_to_selected_games(self, item):
        selected_game = item.text()

        # Check if the game is already selected
        if selected_game not in self.selected_games:
            # Append the selected game to the list of selected games
            self.selected_games.append(selected_game)
            self.update_selected_games_label()

            # Remove the selected game from the available games list
            self.games_list.takeItem(self.games_list.row(item))

    def update_selected_games_label(self):
        # Display selected games in the label
        games_text = ', '.join(self.selected_games)
        self.selected_games_label.setText(f'Selected Games: {games_text}')

    def show_selected_games(self, event):
        # Show a separate window with selected games on label click
        if event.button() == Qt.LeftButton:
            dialog = SelectedGamesDialog(self.selected_games, self)
            dialog.exec_()

    def save_selected_games_to_csv(self):
        with open(r"Info\selected.csv", 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Selected Games'])
            csv_writer.writerow(self.selected_games)

class SelectedGamesDialog(QDialog):
    def __init__(self, games, parent=None):
        super().__init__(parent)

        self.selected_games = games
        self.parent_window = parent

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Selected Games')
        self.setGeometry(300, 300, 300, 200)

        self.games_list = QListWidget(self)
        self.games_list.setGeometry(10, 10, 280, 180)

        for game in self.selected_games:
            item = QListWidgetItem(game)
            item.setFlags(item.flags() | Qt.ItemIsSelectable)
            self.games_list.addItem(item)

        self.games_list.itemClicked.connect(self.remove_selected_game)

    def remove_selected_game(self, item):
        selected_game = item.text()
        if selected_game in self.selected_games:
            self.selected_games.remove(selected_game)
            self.games_list.takeItem(self.games_list.row(item))
            self.parent_window.update_game_list()
            self.parent_window.update_selected_games_label()
            self.parent_window.games_list.addItem(selected_game)

def run():
    window = GameChooserApp()
    window.show()

    # Connect the aboutToQuit signal to save_selected_games_to_csv
    #'app.aboutToQuit.connect(window.save_selected_games_to_csv)
