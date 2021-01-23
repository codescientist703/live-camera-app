import sys
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QDateTime


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Live camera")
        self.setGeometry(50, 50, 1230, 980)
        self.setStyleSheet("background-color: lightblue;")
        self.available_cameras = QCameraInfo.availableCameras()

        if not self.available_cameras:
            sys.exit()

        self.save_path = "/home/madscientist/Desktop/live-feed"
        self.viewfinder = QCameraViewfinder()

        self.viewfinder.show()
        self.viewfinder.resize(10, 10)
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.header()
        self.buttons()

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.random_text = QLabel('Current Time')
        self.random_text.setStyleSheet(
            "background: lightyellow; border: 2px solid green;")

        self.grid.addWidget(self.viewfinder, 1, 0, 4, 2)
        self.select_camera(0)
        self.grid.addWidget(self.random_text, 1, 2)

        self.grid.setRowStretch(1, 1)
        self.grid.setColumnStretch(1, 1)

        self.grid.setVerticalSpacing(70)
        self.grid.setHorizontalSpacing(10)

    # Header component
    def showTime(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('hh:mm:ss')
        self.random_text.setText(timeDisplay)

    def header(self):
        self.main_title = QLabel("Nihal's Awesome GUI", self)
        self.main_title.setStyleSheet(
            "background: lightyellow; border: 2px solid green;font-size: 24px")
        self.main_title.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.main_title, 0, 1)

        self.logo = QLabel(self)
        self.pixmap = QPixmap('python.jpg')
        self.logo.setPixmap(self.pixmap)
        self.logo.resize(self.pixmap.width(),
                         self.pixmap.height())

        self.grid.addWidget(self.logo, 0, 0)

    # All buttons
    def buttons(self):
        self.screenshot = QPushButton('Screenshot')
        self.screenshot.clicked.connect(self.capture_photo)
        self.grid.addWidget(self.screenshot, 2, 2)
        self.screenshot.setStyleSheet("background-color: lightyellow")

        self.stop = QPushButton('STOP')
        self.stop.setStyleSheet("background-color: red; color: white")
        self.grid.addWidget(self.stop, 3, 2)
        self.stop.clicked.connect(self.close_window)

    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])

        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(
            lambda: self.alert(self.camera.errorString()))
        self.camera.start()
        self.capture = QCameraImageCapture(self.camera)

        self.current_camera_name = self.available_cameras[i].description()

    def capture_photo(self):
        self.capture.capture(self.save_path)

    def close_window(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
