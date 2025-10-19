from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QMainWindow, QMenu
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QAction
import sys
import subprocess
import os

WALLPAPER_DIR = r"C:/Users/kumar17/OneDrive - Ecolab/Desktop/MercuryOS Ultimate"

class LoginScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background-color: black;")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: white; font-size: 24px;")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.time_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

    def keyPressEvent(self, event):
        self.show_password_entry()

    def update_time(self):
        current = QDateTime.currentDateTime()
        self.time_label.setText(current.toString("hh:mm:ss AP\ndd-MMM-yyyy"))

    def show_password_entry(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.layout.addWidget(QLabel("Enter Password:", alignment=Qt.AlignmentFlag.AlignCenter, styleSheet="color: white; font-size: 16px;"))
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setStyleSheet("font-size: 18px; padding: 10px; background-color: white;")
        self.layout.addWidget(self.password_entry)
        login_button = QPushButton("Login")
        login_button.setStyleSheet("font-size: 16px; padding: 8px;")
        login_button.clicked.connect(self.check_password)
        self.layout.addWidget(login_button)

    def check_password(self):
        if self.password_entry.text() == "4":
            self.parent.show_main_os()
        else:
            QMessageBox.critical(self, "Error", "Incorrect Password")

class DesktopIcon(QPushButton):
    def __init__(self, label, app_function, description, parent=None):
        super().__init__(label, parent)
        self.app_function = app_function
        self.description = description
        self.setFixedSize(80, 60)
        self.setStyleSheet("background-color: white;")
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.clicked.connect(self.app_function)

    def show_context_menu(self, pos):
        menu = QMenu()
        menu.addAction(f"Open {self.text()}", self.app_function)
        menu.addAction("Properties", lambda: QMessageBox.information(self, "Properties", self.description))
        menu.exec(self.mapToGlobal(pos))

class WallpaperApp(QWidget):
    def __init__(self, main_os):
        super().__init__()
        self.setWindowTitle("Wallpapers")
        self.setGeometry(200, 200, 300, 150)
        self.main_os = main_os

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Choose Wallpaper:")
        layout.addWidget(label)

        btn1 = QPushButton("Mercury_Wallpaper")
        btn2 = QPushButton("Mercury-Wallpaper2")

        btn1.clicked.connect(lambda: self.change_wallpaper("Mercury_Wallpaper.png"))
        btn2.clicked.connect(lambda: self.change_wallpaper("Mercury-Wallpaper2.png"))

        layout.addWidget(btn1)
        layout.addWidget(btn2)

    def change_wallpaper(self, filename):
        self.main_os.set_wallpaper(filename)
        self.close()

class MainOS(QWidget):
    def __init__(self):
        super().__init__()
        self.set_wallpaper("Mercury_Wallpaper.png")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.desktop_area = QWidget()
        self.desktop_area.setStyleSheet("background-color: transparent;")
        self.layout.addWidget(self.desktop_area)

        self.taskbar_widget = QWidget()
        self.taskbar_widget.setFixedHeight(20)
        self.taskbar_widget.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        self.taskbar_layout = QHBoxLayout()
        self.taskbar_layout.setContentsMargins(2, 0, 2, 0)
        self.taskbar_widget.setLayout(self.taskbar_layout)
        self.layout.addWidget(self.taskbar_widget)

        self.start_menu = QMenu()
        self.create_start_menu()

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("background-color: gray; color: white; font-size: 10px; padding: 1px;")
        self.start_button.clicked.connect(self.show_start_menu)
        self.taskbar_layout.addWidget(self.start_button)

        self.battery_label = QLabel("🔋 87%")
        self.battery_label.setStyleSheet("color: white; font-size: 10px; padding: 1px;")
        self.taskbar_layout.addWidget(self.battery_label)

        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: white; font-size: 10px; padding: 1px;")
        self.taskbar_layout.addWidget(self.time_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        self.create_desktop_icons()

    def update_time(self):
        current = QDateTime.currentDateTime()
        self.time_label.setText(current.toString("hh:mm:ss AP | dd-MMM-yyyy"))

    def show_start_menu(self):
        self.start_menu.exec(self.start_button.mapToGlobal(self.start_button.rect().bottomLeft()))

    def create_start_menu(self):
        apps = [
            ("Notepad", self.open_notepad),
            ("Paint", self.open_paint),
            ("CMD", self.open_cmd),
            ("Registry Editor", self.open_regedit),
            ("Microsoft Edge", self.open_edge),
            ("Calculator", self.open_calculator),
            ("File Explorer", self.open_file_explorer),
            ("Wallpapers", self.open_wallpaper_app),
            ("Shutdown", self.shutdown_os)
        ]
        for name, func in apps:
            action = QAction(name, self)
            action.triggered.connect(func)
            self.start_menu.addAction(action)

    def create_desktop_icons(self):
        icons = [
            ("Notepad", self.open_notepad, "Notepad for skeepOS", 50, 50),
            ("Registry Editor", self.open_regedit, "Registry Editor for skeepOS", 150, 50),
            ("Edge", self.open_edge, "Edge browser for skeepOS", 250, 50),
            ("CMD", self.open_cmd, "Command Prompt for skeepOS", 350, 50),
            ("Calculator", self.open_calculator, "Calculator for skeepOS", 450, 50)
        ]
        for label, func, desc, x, y in icons:
            icon = DesktopIcon(label, func, desc, self)
            icon.move(x, y)
            icon.show()
            label_widget = QLabel(label, self)
            label_widget.setStyleSheet("background-color: white; font-size: 10pt;")
            label_widget.move(x + 10, y + 50)
            label_widget.show()

    def open_notepad(self):
        subprocess.Popen(["notepad.exe"])

    def open_paint(self):
        subprocess.Popen(["mspaint.exe"])

    def open_cmd(self):
        subprocess.Popen(["cmd.exe"])

    def open_regedit(self):
        subprocess.Popen(["regedit.exe"])

    def open_edge(self):
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
        for path in edge_paths:
            if os.path.exists(path):
                subprocess.Popen([path])
                return
        QMessageBox.critical(self, "Error", "Edge not found!")

    def open_calculator(self):
        try:
            subprocess.Popen(["calc.exe"])
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Calculator not found!")

    def open_file_explorer(self):
        explorer = QWidget()
        explorer.setWindowTitle("File Explorer")
        explorer.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        explorer.setLayout(layout)
        files = ["Documents", "Pictures", "Music", "Videos", "file1.txt", "file2.docx"]
        for f in files:
            icon = "📁" if "." not in f else "📄"
            layout.addWidget(QLabel(f"{icon} {f}"))
        explorer.show()

    def open_wallpaper_app(self):
        self.wallpaper_app = WallpaperApp(self)
        self.wallpaper_app.show()

    def set_wallpaper(self, filename):
        path = os.path.join(WALLPAPER_DIR, filename).replace("\\", "/")
        self.setStyleSheet(f"""
            QWidget {{
                background-image: url("{path}");
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
            }}
        """)

    def shutdown_os(self):
        self.fade_out_and_shutdown()

    def fade_out_and_shutdown(self):
        for widget in self.findChildren(QWidget):
            widget.hide()
        self.shutdown_label = QLabel("Exiting safely...", self)
        self.shutdown_label.setStyleSheet("color: white; background-color: black; font-size: 24px;")
        self.shutdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.shutdown_label.setGeometry(0, 0, self.width(), self.height())
        self.shutdown_label.show()
        self.opacity = 1.0
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.fade)
        self.fade_timer.start(100)

    def fade(self):
        self.opacity -= 0.05
        if self.opacity <= 0:
            self.fade_timer.stop()
            self.close()
        else:
            self.setWindowOpacity(self.opacity)

class SkeepOS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("skeepOS Simulator")
        self.setFixedSize(800, 600)
        self.login_screen = LoginScreen(self)
        self.setCentralWidget(self.login_screen)

    def show_main_os(self):
        self.main_os = MainOS()
        self.setCentralWidget(self.main_os)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SkeepOS()
    window.show()
    sys.exit(app.exec())