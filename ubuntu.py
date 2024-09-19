import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer

GIFS = [
    "resources/idle.gif",
    "resources/walk_f.gif",
    "resources/walk_b.gif",
]

class Pet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_gif = 0
        self.gif_label = None
        self.ms = 50
        self.move_direction = None
        self.move_speed = 5
        self.gif_speed = 25  # Default speed is 100% (normal speed)

        self.init_ui()
        self.change_speed(self.gif_speed)

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.gif_label = QLabel(self)
        
        self.load_all_gifs()
        
        self.gif_timer = QTimer(self)
        self.gif_timer.timeout.connect(self.update_gif)
        self.gif_timer.start(self.ms)
        
        self.show()

    def load_all_gifs(self):
        self.gifs = []
        for gif_path in GIFS:
            movie = QMovie(gif_path)
            movie.setCacheMode(QMovie.CacheAll)
            movie.setSpeed(self.gif_speed)  # Set initial speed
            self.gifs.append(movie)
            print(f"Loaded GIF: {gif_path}")

        self.gif = self.gifs[self.current_gif]
        self.gif_label.setMovie(self.gif)
        self.gif.start()

        # Update window size to match GIF size
        gif_size = self.gif.currentPixmap().size()
        self.resize(gif_size.width(), gif_size.height())
        self.gif_label.setGeometry(0, 0, gif_size.width(), gif_size.height())

        # Handle GIF direction for movement
        if "walk_f" in GIFS[self.current_gif]:
            self.move_direction = 'left'
        elif "walk_b" in GIFS[self.current_gif]:
            self.move_direction = 'right'
        else:
            self.move_direction = None

    def update_gif(self):
        self.gif_label.setMovie(self.gif)
        self.gif.start()
        
        if self.move_direction:
            self.move_window()

    def move_window(self):
        x, y = self.x(), self.y()
        if self.move_direction == 'left':
            x -= self.move_speed
        elif self.move_direction == 'right':
            x += self.move_speed
        
        self.move(x, y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.switch_gif()

        # NOTE: Maybe do something with this in the future
        # elif event.key() == Qt.Key_Up:
        #     self.change_speed(10)  # Increase speed
        # elif event.key() == Qt.Key_Down:
        #     self.change_speed(-10)  # Decrease speed
        super().keyPressEvent(event)

    def switch_gif(self):
        self.current_gif = (self.current_gif + 1) % len(GIFS)
        self.gif = self.gifs[self.current_gif]
        self.gif_label.setMovie(self.gif)
        self.gif.start()

        # Update window size to match new GIF size
        gif_size = self.gif.currentPixmap().size()
        self.resize(gif_size.width(), gif_size.height())
        self.gif_label.setGeometry(0, 0, gif_size.width(), gif_size.height())

        if "walk_f" in GIFS[self.current_gif]:
            self.move_direction = 'left'
        elif "walk_b" in GIFS[self.current_gif]:
            self.move_direction = 'right'
        else:
            self.move_direction = None

        print(f"Switching to GIF {self.current_gif}")

    def change_speed(self, delta):
        self.gif_speed = max(10, self.gif_speed + delta)  # Ensure speed is not less than 10%
        self.gif.setSpeed(self.gif_speed)
        print(f"Changed GIF speed to {self.gif_speed}")

    def mousePressEvent(self, event):
        self.drag_start_x = event.x()
        self.drag_start_y = event.y()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.drag_start_x
        dy = event.y() - self.drag_start_y
        self.move(self.x() + dx, self.y() + dy)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = Pet()
    sys.exit(app.exec_())
