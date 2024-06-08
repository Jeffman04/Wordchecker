import tkinter as tk
from tkinter import simpledialog, ttk
from PIL import Image, ImageTk
import os

def load_images(folder):
    image_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    images = []
    for filename in image_files:
        image = Image.open(os.path.join(folder, filename))
        images.append(ImageTk.PhotoImage(image))
    return images
def get_part_of_speech(word):
    try:
        with open("words.txt", "r") as f:
            for line in f:
                word_and_part_of_speech = line.split()
                if len(word_and_part_of_speech) >= 2 and word_and_part_of_speech[0].lower() == word.lower():
                    return word_and_part_of_speech[1]
    except FileNotFoundError:
        return "Unable to find the part of speech!"

    user_input = simpledialog.askstring("Input", f"Don't know the part of speech of '{word}'. Please provide it if you know or type 'exit' to quit:")

    if user_input is None or user_input.lower() == 'exit':
        return "exit"

    # Read from a file
    with open("words.txt", "a") as f:
        f.write(f"{word.lower()} {user_input}\n")

    return user_input

def change_background_image():
    global current_image_index
    canvas.delete("bg_image")
    canvas.create_image(0, 0, anchor="nw", image=background_images[current_image_index], tag="bg_image")
    current_image_index = (current_image_index + 1) % len(background_images)
    canvas.after(7000, change_background_image)  # Schedule next image change
    # Update the word and its part of speech
    on_button_click()


def on_button_click():
    user_input = entry_var.get()
    words = user_input.split()  

    # Clear previous result
    canvas.delete("result_text")

    for i, word in enumerate(words):
        part_of_speech = get_part_of_speech(word)
        result_text = f"the word {word} is a {part_of_speech}"
        canvas.create_rectangle(canvas_width/2 - 150, canvas_height*0.6 + i*30 - 20, canvas_width/2 + 150, canvas_height*0.6 + i*30 + 20, fill="lightgrey", outline="")
        canvas.create_text(canvas_width/2, canvas_height*0.6 + i*30, text=result_text, font=("Arial", 18), fill="green", tag="result_text")

app = tk.Tk()
app.title("Part of Speech Identifier")

canvas_width = 800
canvas_height = 600

canvas = tk.Canvas(app, width=canvas_width, height=canvas_height)
canvas.pack()

style = ttk.Style()

label = ttk.Label(canvas, text="hello, welcome to the word checker application", font=("Arial", 24))
label.place(relx=0.5, rely=0.1, anchor="center")

label = ttk.Label(canvas, text="Enter a word or a sentence:")
label.place(relx=0.5, rely=0.3, anchor="center")

entry_var = tk.StringVar()
entry = ttk.Entry(canvas, textvariable=entry_var)
entry.place(relx=0.5, rely=0.4, anchor="center")

button = ttk.Button(canvas, text="Get Part of Speech", command=on_button_click)
button.place(relx=0.5, rely=0.5, anchor="center")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

window_width = 1000
window_height = 600

window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2

app.wm_geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Load background images
background_folder = "background_images"
background_images = load_images(background_folder)
current_image_index = 0

# Start the slideshow
change_background_image()

app.mainloop()
