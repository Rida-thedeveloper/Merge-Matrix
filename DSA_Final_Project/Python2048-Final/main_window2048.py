import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk  # Import Pillow
import level_1_function
import level_2_function
import level_3_function
# Define button functions
def level_1():
    level_1_function.run_2048_game1()  # Call the run_2048_game function

def level_2():
    level_2_function.run_2048_game2()  # Call the run_2048_game function

def level_3():
    level_3_function.run_2048_game3()  # Call the run_2048_game function


# Function to create a rounded rectangle on the Canvas
def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)


# Create the main window
root = tk.Tk()
root.geometry('400x650+400+100')
root.title('Merge Matrix')
root.configure(bg='#DCC0B3')  # Main background color
root.resizable(0, 0)

# Create a frame for the picture and text with custom color
picture_frame = tk.Frame(root, bg='#DCC0B3')
picture_frame.pack(side='top', fill='both', expand=True)

# Load and display the image using Pillow
img = Image.open('image2.png')  # Use the correct path if needed
img = img.resize((400, 250))  # Resize the image if necessary
img = ImageTk.PhotoImage(img)
picture_label = tk.Label(picture_frame, image=img, bg='#DCC0B3')
picture_label.pack()

# Add text below the image
text_label = tk.Label(picture_frame, text="Welcome to Merge Matrix", font=('Times New Roman', 24, 'bold'), bg='#DCC0B3', fg='#003366')
text_label.pack(pady=10)  # Add some vertical space above the text

# Add text below the image
text_label = tk.Label(picture_frame, text="Select The Level", font=('Times New Roman', 18), bg='#DCC0B3', fg='#003366')
text_label.pack(pady=10)  # Add some vertical space above the text

# Create a frame for the buttons with custom color
button_frame = tk.Frame(root, bg='#DCC0B3')
button_frame.pack(side='bottom', pady=20)


# Function to create a button using a canvas with a rounded rectangle
def create_rounded_button(parent, text, command):
    button_canvas = tk.Canvas(parent, width=150, height=50, bg='#DCC0B3', highlightthickness=0)
    round_rectangle(button_canvas, 5, 5, 145, 45, radius=15, fill="#F5F6FA", outline="")
    button_canvas.create_text(75, 25, text=text, fill="#003366", font=("Times New Roman", 16))
    button_canvas.bind("<Button-1>", lambda event: command())  # Bind the click event to the command function
    button_canvas.pack(pady=10)  # Reduce padding to fit all buttons
    return button_canvas


# Create level buttons using the rounded rectangle button style
button1 = create_rounded_button(button_frame, "Level 1", level_1)
button2 = create_rounded_button(button_frame, "Level 2", level_2)
button3 = create_rounded_button(button_frame, "Level 3", level_3)

# Run the application
root.mainloop()
