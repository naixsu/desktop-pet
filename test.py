import sys
import random
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer

moods = ["cool", "happy", "normal", "special"]
actions = {
    "cool": ["angry", "doubt", "idle", "joy", "laugh", "listen", "sad", "surprise", "talk"],  # no "walk_f" and "walk_b"
    "happy": ["angry", "doubt", "idle", "joy", "laugh", "listen", "sad", "surprise", "talk"],  # no "walk_f" and "walk_b"
    "normal": ["angry", "doubt", "idle", "joy", "laugh", "listen", "surprise", "talk", "walk_f", "walk_b"],  # no "sad"
    "special": ["negi"],
}

# Create a dictionary that maps each mood to its respective available actions
GIFS = {mood: {action: f"resources/{mood}_{action}.gif" for action in actions[mood]} for mood in moods}

class Pet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_gif = 0
        self.gif_label = None
        self.ms = 50
        self.move_direction = None
        self.move_speed = 5
        self.gif_speed = 30
        self.mood = random.choice(moods)  # Randomly initialize mood

        self.init_ui()
        self.change_speed(self.gif_speed)

    def init_ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.gif_label = QLabel(self)
        
        self.load_gifs_by_mood()  # Load GIFs based on current mood
        
        self.gif_timer = QTimer(self)
        self.gif_timer.timeout.connect(self.update_gif)
        self.gif_timer.start(self.ms)
        
        self.show()

    def load_gifs_by_mood(self):
        self.gifs = []
        mood_gifs = GIFS[self.mood]  # Only load GIFs for the current mood
        for action, gif_path in mood_gifs.items():
            movie = QMovie(gif_path)
            movie.setCacheMode(QMovie.CacheAll)
            movie.setSpeed(self.gif_speed)  # Set initial speed
            self.gifs.append((action, movie))
            print(f"Loaded GIF for {self.mood}: {gif_path}")

        self.switch_gif()

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

        elif event.key() == Qt.Key_Up:
            self.change_speed(5)  # Increase speed
        elif event.key() == Qt.Key_Down:
            self.change_speed(-5)  # Decrease speed

        super().keyPressEvent(event)

    def switch_gif(self):
        self.current_gif = (self.current_gif + 1) % len(self.gifs)
        action, self.gif = self.gifs[self.current_gif]
        self.gif_label.setMovie(self.gif)
        self.gif.start()

        # Update window size to match new GIF size
        gif_size = self.gif.currentPixmap().size()
        self.resize(gif_size.width(), gif_size.height())
        self.gif_label.setGeometry(0, 0, gif_size.width(), gif_size.height())

        # Handle GIF direction for movement
        if "walk_f" in action:
            self.move_direction = 'left'
        elif "walk_b" in action:
            self.move_direction = 'right'
        else:
            self.move_direction = None

        print(f"Switched to {self.mood}:{action}")

    def change_speed(self, delta):
        self.gif_speed += delta
        self.gif_speed = max(10, self.gif_speed)  # Ensure speed is not less than 10%
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
