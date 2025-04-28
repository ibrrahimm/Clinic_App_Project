import requests
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QMessageBox, QFrame, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont, QColor, QPalette

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # API endpoint (to be updated with URL) # Hamdy Role
        self.api_url = "http://localhost:8080/api/auth/login" # <-------- REPLACE THE URL HERE

        #-----------------------------------------------Appearance------------------------------------------------------------------#
        self.setWindowTitle("Login System")
        self.setMinimumSize(450, 420)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f4f8; /* Light grayish blue  */
            }
            QFrame#container { /* Use object name for specificity */
                background-color: white;
                border-radius: 10px;
                border: 1px solid #d3d9e0; /* Lighter border */
                padding: 25px;
            }
            QLabel#titleLabel {
                font-size: 26px;
                font-weight: bold;
                color: #1e3a5f; /* Dark blue */
                margin-bottom: 5px;
            }
            QLabel#subtitleLabel {
                font-size: 14px;
                color: #5a6a7a; /* Slate gray */
                margin-bottom: 25px;
            }
            QLabel.fieldLabel { /* Class for field labels */
                font-size: 14px;
                font-weight: bold;
                color: #3e4e5e; /* Dark gray */
                margin-bottom: 5px; /* Space below label */
            }
            QLineEdit {
                padding: 12px;
                border: 1px solid #b0bec5; /* Slightly darker border */
                border-radius: 5px;
                background-color: #ffffff;
                font-size: 14px;
                color: #263238; /* Dark text */
            }
            QLineEdit:focus {
                border: 2px solid #2979ff; /* Blue focus highlight */
                background-color: #e3f2fd; /* Light blue background on focus */
            }
            QPushButton#loginButton {
                padding: 12px 18px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                background-color: #28a745; /* Green */
                color: white;
                border: none;
            }
            QPushButton#loginButton:hover {
                background-color: #218838; /* Darker green */
            }
            QPushButton#resetButton {
                padding: 12px 18px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                background-color: #dc3545; /* Red */
                color: white;
                border: none;
            }
            QPushButton#resetButton:hover {
                background-color: #c82333; /* Darker red */
            }
        """)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20) # Overall window margins
        main_layout.addStretch(1) # Add stretch before

        # Card-like container
        container = QFrame()
        container.setObjectName("container") # Set object name for styling
        container.setFixedWidth(420) # Fixed width for the card
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(15) # Adjusted spacing

        # Title
        title_label = QLabel("Login System")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Please enter your credentials")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(subtitle_label)

        # Add some vertical space
        container_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Form layout (within container)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15) # Consistent spacing

        # Username field (Label above input)
        username_label = QLabel("Username:")
        username_label.setProperty("class", "fieldLabel") # Add class for styling
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)

        # Password field (Label above input)
        password_label = QLabel("Password:")
        password_label.setProperty("class", "fieldLabel") # Add class for styling
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)

        # Add form to container layout
        container_layout.addLayout(form_layout)

        # Add spacing before buttons
        container_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Buttons layout (within container)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15) # Space between buttons

        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.reset_form)

        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.login)
        # Set Login as the default button (activated by Enter key)
        self.login_button.setDefault(True)
        # Also trigger login on Enter press in password field
        self.password_input.returnPressed.connect(self.login)

        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.login_button)

        container_layout.addLayout(button_layout)

        # Add container to the main layout
        main_layout.addWidget(container)

        # Set initial focus
        self.username_input.setFocus()
        
    #-----------------------------------------------CHECK------------------------------------------------------------------#
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            print("[Input Error] Username or password field is empty.")
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        # Prepare the login data for API
        login_data = {
            "username": username,
            "password": password
        }
        print(f"[API Request] Sending login request for user '{username}' to {self.api_url}")

        try:
            # Send request to backend API with a timeout
            response = requests.post(self.api_url, json=login_data, timeout=10) # 10-second timeout

            # Raise HTTPError for bad responses (4xx or 5xx client/server errors)
            response.raise_for_status()

            # If status code is 200 OK
            data = response.json()
            print(f"[API Response] Login successful. Status: {response.status_code}, Data: {data}")
            QMessageBox.information(self, "Login Successful", f"Welcome {username}!")
            # Here you might want to close the login window and open the main application window
            # self.close()

        # --- Specific Error Handling ---
        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors (e.g., 401 Unauthorized, 404 Not Found, 500 Internal Server Error)
            status_code = http_err.response.status_code
            error_msg = f"Login failed. Server returned status code {status_code}."
            print(f"[API Error] HTTP Error: {http_err}")
            try:
                # Try to get a specific error message from the response body
                error_data = http_err.response.json()
                if "message" in error_data and error_data["message"]:
                    error_msg = f"Login Failed: {error_data['message']} (Status {status_code})"
                elif "error" in error_data and error_data["error"]:
                     error_msg = f"Login Failed: {error_data['error']} (Status {status_code})"
                print(f"[API Error Detail] Response Body: {http_err.response.text}")
            except requests.exceptions.JSONDecodeError:
                 print(f"[API Error Detail] Response body was not valid JSON: {http_err.response.text}")
                 error_msg = f"Login failed. Received invalid response from server (Status {status_code})."

            if status_code == 401 or status_code == 403:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            elif status_code == 404:
                 QMessageBox.critical(self, "Configuration Error", f"Login endpoint not found ({self.api_url}). Please check the API URL.")
            else:
                QMessageBox.critical(self, "Login Failed", error_msg)

        except requests.exceptions.ConnectionError as conn_err:
            # Handle errors connecting to the server (DNS failure, refused connection, etc.)
            error_msg = "Could not connect to the server. Please check your network connection and ensure the backend service is running."
            print(f"[Connection Error] Failed to establish connection: {conn_err}")
            QMessageBox.critical(self, "Connection Error", error_msg)

        except requests.exceptions.Timeout as timeout_err:
            # Handle request timeouts
            error_msg = "The login request timed out. The server might be busy or unresponsive."
            print(f"[Timeout Error] Request timed out: {timeout_err}")
            QMessageBox.warning(self, "Request Timeout", error_msg)

        except requests.exceptions.RequestException as req_err:
            # Handle any other errors originating from the 'requests' library
            error_msg = f"An unexpected error occurred during the request: {req_err}"
            print(f"[Request Error] An error occurred: {req_err}")
            QMessageBox.critical(self, "Request Error", error_msg)

        except Exception as e:
            # Catch any other unexpected errors (e.g., issues with processing response data)
            error_msg = f"An unexpected error occurred: {e}"
            print(f"[Unexpected Error] Type: {type(e).__name__}, Details: {e}")
            QMessageBox.critical(self, "Error", error_msg)


    def reset_form(self):
        self.username_input.clear()
        self.password_input.clear()
        print("[Form Action] Form fields cleared.")
        self.username_input.setFocus() # Set focus back to username field


if __name__ == "__main__":
    # Ensure High DPI scaling is enabled for sharper UI elements
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # Apply a font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = LoginWindow()
    window.show()
    sys.exit(app.exec())