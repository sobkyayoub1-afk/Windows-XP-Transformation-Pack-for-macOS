import sys
import time
from PyQt5 import QtWidgets, QtCore
from AppKit import NSWorkspace
import Quartz
from Quartz import AXUIElementCreateApplication, AXUIElementCopyAttributeValue, AXUIElementPerformAction

class XPOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

        # XP Title Bar
        self.title_bar = QtWidgets.QFrame(self)
        self.title_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                                            stop:0 #0a246a,
                                            stop:1 #3a6ea5);
                border: 1px solid #001a4d;
            }
        """)

        self.title_label = QtWidgets.QLabel("Active Window", self.title_bar)
        self.title_label.setStyleSheet("color: white; font: bold 10pt;")
        self.title_label.move(10, 2)

        # Buttons
        self.close_btn = QtWidgets.QPushButton("X", self.title_bar)
        self.close_btn.setStyleSheet("background:#ff5c5c; border:1px solid #800000; font-weight:bold;")

        self.min_btn = QtWidgets.QPushButton("_", self.title_bar)
        self.min_btn.setStyleSheet("background:#e0e0e0; border:1px solid #808080;")

        self.max_btn = QtWidgets.QPushButton("⬜", self.title_bar)
        self.max_btn.setStyleSheet("background:#e0e0e0; border:1px solid #808080;")

        self.close_btn.clicked.connect(self.close_window)
        self.min_btn.clicked.connect(self.minimize_window)
        self.max_btn.clicked.connect(self.maximize_window)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_overlay)
        self.timer.start(50)

    def get_focused_window(self):
        workspace = NSWorkspace.sharedWorkspace()
        app = workspace.frontmostApplication()
        pid = app.processIdentifier()

        ax_app = AXUIElementCreateApplication(pid)
        window = AXUIElementCopyAttributeValue(ax_app, "AXFocusedWindow", None)[1]
        return window

    def update_overlay(self):
        try:
            window = self.get_focused_window()
            position = AXUIElementCopyAttributeValue(window, "AXPosition", None)[1]
            size = AXUIElementCopyAttributeValue(window, "AXSize", None)[1]

            x = position.x
            y = position.y
            w = size.width

            self.setGeometry(int(x), int(y), int(w), 28)
            self.title_bar.setGeometry(0, 0, int(w), 28)

            self.close_btn.setGeometry(w - 35, 4, 30, 20)
            self.max_btn.setGeometry(w - 70, 4, 30, 20)
            self.min_btn.setGeometry(w - 105, 4, 30, 20)

            self.show()

        except Exception:
            self.hide()

    def close_window(self):
        window = self.get_focused_window()
        AXUIElementPerformAction(window, "AXClose")

    def minimize_window(self):
        window = self.get_focused_window()
        AXUIElementPerformAction(window, "AXMinimize")

    def maximize_window(self):
        window = self.get_focused_window()
        AXUIElementPerformAction(window, "AXZoom")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    overlay = XPOverlay()
    overlay.show()
    sys.exit(app.exec_())
