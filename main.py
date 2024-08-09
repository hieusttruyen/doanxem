import sys
import os
import subprocess
import json
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

SETTINGS_FILE = "settings.json"

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_settings()
        self.process = None

    def initUI(self):
        # Tạo layout chính
        main_layout = QVBoxLayout()

        # Tạo layout cho phần input path
        path_layout = QHBoxLayout()
        self.label_path = QLabel("Path:")
        self.input_path = QLineEdit()
        self.button_browse = QPushButton("Browse")
        self.button_browse.clicked.connect(self.browse_path)
        path_layout.addWidget(self.label_path)
        path_layout.addWidget(self.input_path)
        path_layout.addWidget(self.button_browse)

        # Tạo layout cho phần chọn số lượng nhóm
        team_layout = QHBoxLayout()
        self.label_team_number = QLabel("Number of Teams:")
        self.combo_team_number = QComboBox()
        self.combo_team_number.addItems([str(i) for i in range(1, 6)])
        team_layout.addWidget(self.label_team_number)
        team_layout.addWidget(self.combo_team_number)

        # Tạo layout cho các nút
        self.button_start = QPushButton("Start")
        self.button_stop = QPushButton("Stop")
        self.button_stop.setEnabled(False)  # Vô hiệu hóa nút Stop ban đầu
        self.button_start.clicked.connect(self.start)
        self.button_stop.clicked.connect(self.stop)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_start)
        button_layout.addWidget(self.button_stop)

        # Thêm các layout con vào layout chính
        main_layout.addLayout(path_layout)
        main_layout.addLayout(team_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Team Selector")
        self.setFixedSize(300, 150)  # Thiết lập kích thước cố định cho cửa sổ

        # Đặt vị trí của cửa sổ ở phía trên bên phải
        screen_geometry = QApplication.desktop().availableGeometry()
        x = screen_geometry.width() - self.width() - 10
        y = 0
        self.move(x, y)

        self.show()

    def browse_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", "", options=options
        )
        if directory:
            self.input_path.setText(directory)

    def start(self):
        if self.process is not None:
            # Process is already running
            return

        path = self.input_path.text()
        file_to_check = os.path.join(path, "launcher.exe")
        if os.path.isfile(file_to_check):
            number_of_teams = self.combo_team_number.currentText()
            self.save_settings(path, number_of_teams)
            self.button_start.setEnabled(False)  # Vô hiệu hóa nút Start
            self.button_stop.setEnabled(True)  # Kích hoạt nút Stop
            self.process = subprocess.Popen([sys.executable, 'rok.py', path, number_of_teams, '3'])
        else:
            QMessageBox.warning(
                self,
                "File Not Found",
                f"The file 'launcher.exe' was not found in the specified path:\n{path}",
            )

    def stop(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None
            self.button_start.setText("Start")
            self.button_start.setEnabled(True)  # Kích hoạt nút Start
            self.button_stop.setEnabled(False)  # Vô hiệu hóa nút Stop

    def closeEvent(self, event):
        # Đảm bảo dừng quá trình khi đóng ứng dụng
        self.stop()
        event.accept()

    def save_settings(self, path, number_of_teams):
        settings = {
            "path": path,
            "number_of_teams": number_of_teams
        }
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        if os.path.isfile(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                self.input_path.setText(settings.get("path", ""))
                self.combo_team_number.setCurrentText(settings.get("number_of_teams", "5"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
