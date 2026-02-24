#!/usr/bin/env python3
import sys
import os
import json
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore

HOME_APPS = Path.home() / "Applications"
CONFIG_FILE = Path.home() / ".xp_taskbar_config.json"

class StartMenu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedWidth(250)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Scroll area for apps
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll)

        self.populate_apps()

    def populate_apps(self):
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        apps_dirs = ["/Applications", str(HOME_APPS)]
        apps = []
        for d in apps_dirs:
            if os.path.exists(d):
                apps += [f for f in os.listdir(d) if f.endswith(".app")]
        apps.sort()

        for app in apps:
            btn = QtWidgets.QPushButton(app.replace(".app",""))
            icon_path = os.path.join(d, app, "Contents/Resources/AppIcon.icns")
            if os.path.exists(icon_path):
                btn.setIcon(QtGui.QIcon(icon_path))
            btn.setIconSize(QtCore.QSize(24,24))
            btn.setStyleSheet("text-align: left; padding: 5px;")
            btn.clicked.connect(lambda checked, a=app: self.launch_app(a))
            self.scroll_layout.addWidget(btn)

    def launch_app(self, app_name):
        paths = ["/Applications", str(HOME_APPS)]
        for p in paths:
            full_path = os.path.join(p, app_name)
            if os.path.exists(full_path):
                os.system(f'open "{full_path}"')
                break
        self.hide()


class Taskbar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(0, self.screen_geometry.height() - 40, self.screen_geometry.width(), 40)

        self.start_menu = StartMenu()
        self.pinned_apps = []
        self.running_apps = []

        self.load_config()
        self.init_ui()
        self.update_running_apps_timer()

    def init_ui(self):
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(2,2,2,2)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)

        # Start button
        self.start_btn = QtWidgets.QPushButton("Start")
        self.start_btn.setFixedSize(80, 36)
        self.start_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #000080;
                font-weight: bold;
                color: white;
            }
        """)
        self.start_btn.clicked.connect(self.toggle_start_menu)
        self.layout.addWidget(self.start_btn)

        # Pinned apps area
        self.pinned_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.pinned_layout)
        self.update_pinned_apps()

        # Running apps area
        self.running_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.running_layout)
        self.layout.addStretch()

        # Clock area
        self.tray = QtWidgets.QLabel(QtCore.QDateTime.currentDateTime().toString("hh:mm"))
        self.tray.setFixedWidth(60)
        self.tray.setAlignment(QtCore.Qt.AlignCenter)
        self.tray.setStyleSheet("color: white; font-weight: bold;")
        self.layout.addWidget(self.tray)

        # Update clock every second
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)

        # Right-click menu for pinning apps
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QtWidgets.QMenu()
        action = menu.addAction("Pin App…")
        action.triggered.connect(self.select_app_to_pin)
        menu.exec_(self.mapToGlobal(pos))

    def select_app_to_pin(self):
        file_dialog = QtWidgets.QFileDialog(self, "Select App", str(HOME_APPS))
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Applications (*.app)")
        if file_dialog.exec_():
            app_path = file_dialog.selectedFiles()[0]
            self.pin_app(app_path)

    # ---------------- Pinned apps management ----------------
    def pin_app(self, app_path):
        if app_path not in self.pinned_apps:
            self.pinned_apps.append(app_path)
            self.update_pinned_apps()
            self.save_config()

    def unpin_app(self, app_path):
        if app_path in self.pinned_apps:
            self.pinned_apps.remove(app_path)
            self.update_pinned_apps()
            self.save_config()

    def update_pinned_apps(self):
        # Clear old widgets
        while self.pinned_layout.count():
            item = self.pinned_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        for app_path in self.pinned_apps:
            btn = QtWidgets.QPushButton()
            btn.setFixedSize(36,36)
            icon_file = os.path.join(app_path, "Contents/Resources/AppIcon.icns")
            if os.path.exists(icon_file):
                btn.setIcon(QtGui.QIcon(icon_file))
            btn.setIconSize(QtCore.QSize(32,32))
            btn.clicked.connect(lambda checked, p=app_path: os.system(f'open "{p}"'))
            self.pinned_layout.addWidget(btn)

    # ---------------- Running apps detection ----------------
    def update_running_apps_timer(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_running_apps)
        timer.start(2000)

    def update_running_apps(self):
        stream = os.popen('osascript -e \'tell application "System Events" to get name of (processes where background only is false)\'')
        output = stream.read()
        names = [name.strip() for name in output.replace(",", "\n").split("\n") if name.strip()]
        self.running_apps = names
        self.refresh_running_apps_ui()

    def refresh_running_apps_ui(self):
        while self.running_layout.count():
            item = self.running_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        for app_name in self.running_apps:
            btn = QtWidgets.QPushButton(app_name)
            btn.setFixedSize(80,36)
            btn.clicked.connect(lambda checked, n=app_name: os.system(f'osascript -e \'tell application "{n}" to activate\''))
            self.running_layout.addWidget(btn)

    # ---------------- Clock & Start Menu ----------------
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        gradient = QtGui.QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QtGui.QColor(10, 36, 106))
        gradient.setColorAt(1, QtGui.QColor(0, 0, 128))
        painter.fillRect(self.rect(), gradient)

    def update_clock(self):
        self.tray.setText(QtCore.QDateTime.currentDateTime().toString("hh:mm"))

    def toggle_start_menu(self):
        if self.start_menu.isVisible():
            self.start_menu.hide()
        else:
            pos = self.mapToGlobal(QtCore.QPoint(0, -self.start_menu.height()))
            self.start_menu.move(pos)
            self.start_menu.show()

    # ---------------- Config persistence ----------------
    def load_config(self):
        if CONFIG_FILE.exists():
            try:
                data = json.loads(CONFIG_FILE.read_text())
                self.pinned_apps = data.get("pinned_apps", [])
            except Exception:
                self.pinned_apps = []

    def save_config(self):
        data = {"pinned_apps": self.pinned_apps}
        CONFIG_FILE.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    taskbar = Taskbar()
    taskbar.show()
    sys.exit(app.exec_())	