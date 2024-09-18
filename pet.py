import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

# Define custom vars here
MS = 75

# Function to update GIF frames
def update_gif(ind):
    frame = frames[ind]
    ind += 1
    if ind == len(frames):
        ind = 0
    gif_label.configure(image=frame)

    # MS = ms, basically adjust the speed of the gif
    window.after(MS, update_gif, ind)
    
# Function to handle window dragging
def on_drag_start(event):
    global x_start, y_start
    x_start = event.x
    y_start = event.y

def on_drag_motion(event):
    x = window.winfo_pointerx() - x_start
    y = window.winfo_pointery() - y_start
    window.geometry(f"+{x}+{y}")

# Create a window
window = tk.Tk()
window.title("GIF Display")

window.overrideredirect(True)  # Removes window decorations (title bar, borders)
window.attributes("-topmost", True)  # Keep window always on top
window.attributes("-transparentcolor", "black")  # Make the white color transparent

# Load the GIF
gif_path = "resources\miku_idle.gif"
gif = Image.open(gif_path)

# Convert frames to a list
frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif)]

# Display the first frame with transparent background
gif_label = tk.Label(window, bg="black")  # Set label background to black to match transparency
gif_label.pack()

# Bind mouse events for dragging
gif_label.bind("<Button-1>", on_drag_start)  # Start dragging when mouse button is pressed
gif_label.bind("<B1-Motion>", on_drag_motion)  # Drag window with mouse motion

# Start the GIF loop
window.after(0, update_gif, 0)

# Run the window loop
window.mainloop()
