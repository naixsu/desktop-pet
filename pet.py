import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

# Define custom vars here
# MS = 50  # Delay for GIF frames in milliseconds
GIFS = [
    "resources/idle.gif",
    "resources/walk_f.gif",
    "resources/walk_b.gif",
]

class Pet:
    def __init__(self, window: tk):
        self.current_gif = 0
        self.frames = {}  # Dictionary to store frames for each GIF
        self.gif = None
        self.gif_path = None
        self.x_start = None
        self.y_start = None
        self.gif_label = None
        self.ms = 50
        
        self.window = window
        self.load_all_gifs()  # Load all GIFs and their frames during initialization
        
        # Movement control
        self.move_direction = None
        self.move_speed = 5  # Speed of movement in pixels
    
    def load_all_gifs(self):
        for gif_path in GIFS:
            gif = Image.open(gif_path)
            frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif)]
            self.frames[gif_path] = frames
            print(f"Loaded {len(frames)} frames for {gif_path}")

    def start(self):
        # Load the initial GIF
        self.gif_path = GIFS[self.current_gif]
        self.gif = self.frames[self.gif_path]
        
        # Display the first frame with transparent background
        self.gif_label = tk.Label(self.window, bg="black")  # Set label background to black to match transparency
        self.gif_label.pack()
        
        # Bind mouse events for dragging
        self.gif_label.bind("<Button-1>", self.on_drag_start)  # Start dragging when mouse button is pressed
        self.gif_label.bind("<B1-Motion>", self.on_drag_motion)  # Drag window with mouse motion
        
        # Start the GIF loop
        self.window.after(0, self.update_gif, 0)
        # Run the window loop
        self.window.mainloop()

    def update_gif(self, ind):
        frame = self.gif[ind]
        self.gif_label.configure(image=frame)
        print('update_gif', frame, self.gif_path, ind)
        ind += 1
        if ind == len(self.gif):
            ind = 0
            # Schedule switch only after the last frame is displayed
            self.window.after(self.ms, self.switch_gif)  # Use self.ms delay to ensure the last frame is shown
            return
        
        # Move window based on current GIF
        if self.move_direction:
            self.move_window()
        
        # self.ms = self.ms, basically adjust the speed of the gif
        self.window.after(self.ms, self.update_gif, ind)

    def move_window(self):
        x, y = self.window.winfo_x(), self.window.winfo_y()
        if self.move_direction == 'left':
            x -= self.move_speed
        elif self.move_direction == 'right':
            x += self.move_speed
        
        # Update window position
        self.window.geometry(f"+{x}+{y}")
    
    def switch_gif(self):
        # Clear the label's image to avoid flickering
        self.gif_label.configure(image='')

        # Switch GIF
        self.current_gif = (self.current_gif + 1) % len(GIFS)
        self.gif_path = GIFS[self.current_gif]
        self.gif = self.frames[self.gif_path]
        
        # Update movement direction based on GIF
        if "walk_f" in self.gif_path:
            self.move_direction = 'left'
        elif "walk_b" in self.gif_path:
            self.move_direction = 'right'
        else:
            self.move_direction = None
        
        # This is just to smooth out the animation frames
        # NOTE: The `ms` numbers are all arbitrary
        if self.move_direction is None: # Idling
            self.ms = 50
        else:
            self.ms = 70
        
        print(f"Switching to GIF {self.current_gif} with {len(self.gif)} frames")

        # Restart the GIF animation
        self.update_gif(0)
    
    def on_drag_start(self, event):
        self.x_start = event.x
        self.y_start = event.y

    def on_drag_motion(self, event):
        x = self.window.winfo_pointerx() - self.x_start
        y = self.window.winfo_pointery() - self.y_start
        self.window.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    # Create a window
    window = tk.Tk()
    window.title("GIF Display")

    window.overrideredirect(True)  # Removes window decorations (title bar, borders)
    window.attributes("-topmost", True)  # Keep window always on top

    # NOTE: This is a bit iffy. Maybe some gifs have a white bg, so change this to the respective color.
    window.attributes("-transparentcolor", "black")  # Make the black color transparent.

    pet = Pet(window)
    pet.start()
