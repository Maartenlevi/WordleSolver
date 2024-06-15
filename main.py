import tkinter as tk
from tkinter import font

# Function to handle focus in and out for the Entry widget
def on_entry_click(event):
    if entry.get() == 'Input starting word...':
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # Insert blank for user input
        entry.config(fg='black')

def on_focusout(event):
    if entry.get() == '':
        entry.insert(0, 'Input starting word...')
        entry.config(fg='grey')

# Create the main window
root = tk.Tk()
root.geometry("1800x900")
root.title("Dashboard")
root.configure(background='#FFFFFF')

# Define fonts
inter_font_50_bold = font.Font(family='Inter', size=50, weight='bold')
inter_font_30 = font.Font(family='Inter', size=30)
inter_font_20 = font.Font(family='Inter', size=20)

# Navigation bar
nav_frame = tk.Frame(root, height=104, bg='#FFFFFF', highlightbackground='#E0E0E0', highlightthickness=1)
nav_frame.pack(fill='x', side='top')

# WordleSolver title
title_label = tk.Label(root, text="WordleSolver", font=inter_font_50_bold, fg='#000000', bg='#FFFFFF')
title_label.place(relx=0.5, rely=0.25, anchor='center')

# Rectangles with rounded corners
def create_rounded_frame(master, width, height, bg, x, y):
    canvas = tk.Canvas(master, width=width, height=height, bg=bg, bd=0, highlightthickness=0)
    canvas.place(x=x, y=y)
    radius = 10
    canvas.create_arc((0, 0, radius * 2, radius * 2), start=90, extent=90, fill=bg, outline=bg)
    canvas.create_arc((width - radius * 2, 0, width, radius * 2), start=0, extent=90, fill=bg, outline=bg)
    canvas.create_arc((0, height - radius * 2, radius * 2, height), start=180, extent=90, fill=bg, outline=bg)
    canvas.create_arc((width - radius * 2, height - radius * 2, width, height), start=270, extent=90, fill=bg, outline=bg)
    canvas.create_rectangle(radius, 0, width - radius, height, fill=bg, outline=bg)
    canvas.create_rectangle(0, radius, width, height - radius, fill=bg, outline=bg)

create_rounded_frame(root, 479, 496, '#D9D9D9', 84, 488)
create_rounded_frame(root, 479, 496, '#D9D9D9', 673, 488)
create_rounded_frame(root, 479, 496, '#D9D9D9', 1262, 488)
create_rounded_frame(root, 1068, 241, '#D9D9D9', 673, 177)

# Input field with label
input_frame = tk.Frame(root, bg='#FFFFFF')
input_frame.place(x=84, y=125)

# Starting word label
start_label = tk.Label(input_frame, text="Starting word", font=inter_font_30, fg='#000000', bg='#FFFFFF')
start_label.pack(anchor='w')

# Field with rounded corners
field_canvas = tk.Canvas(input_frame, width=457, height=52, bg='#E0E0E0', highlightthickness=0)
field_canvas.pack(pady=(8, 0))
radius = 10
field_canvas.create_arc((0, 0, radius * 2, radius * 2), start=90, extent=90, fill='#E0E0E0', outline='#E0E0E0')
field_canvas.create_arc((457 - radius * 2, 0, 457, radius * 2), start=0, extent=90, fill='#E0E0E0', outline='#E0E0E0')
field_canvas.create_arc((0, 52 - radius * 2, radius * 2, 52), start=180, extent=90, fill='#E0E0E0', outline='#E0E0E0')
field_canvas.create_arc((457 - radius * 2, 52 - radius * 2, 457, 52), start=270, extent=90, fill='#E0E0E0', outline='#E0E0E0')
field_canvas.create_rectangle(radius, 0, 457 - radius, 52, fill='#E0E0E0', outline='#E0E0E0')
field_canvas.create_rectangle(0, radius, 457, 52 - radius, fill='#E0E0E0', outline='#E0E0E0')

field_frame = tk.Frame(field_canvas, width=457, height=52, bg='#E0E0E0')
field_frame.pack()

entry = tk.Entry(field_frame, font=inter_font_20, fg='grey', bg='#E0E0E0', bd=0)
entry.insert(0, 'Input starting word...')
entry.bind('<FocusIn>', on_entry_click)
entry.bind('<FocusOut>', on_focusout)
entry.pack(fill='both', padx=16, pady=8)

# Run the application
root.mainloop()
