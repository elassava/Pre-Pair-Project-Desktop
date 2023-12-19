def get_stylesheet():
    return """
            QWidget {
                background-color: #222024;
                color: #e2e3e2;
            }
            QPushButton {
                padding: 8px 16px;
                font-size: 16px;
                font-family: "Calibri", sans-serif;
                background-color: #4e439d;
                color: #ffffff;
                border: 1px solid #4e439d;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #6b5fbb;
                color: #e2e3e2;
            }
            QLabel {
                font-size: 18px;
                font-family: "Calibri", sans-serif;
                color: #e2e3e2;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                font-family: "Calibri", sans-serif;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
        """