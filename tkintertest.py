import tkinter as tk

root = tk.Tk()
root.title("Enter the URL")

root.geometry("500x300")

# Change the font size of the label
label = tk.Label(root, text="Enter URL here for cloud", font=("Arial", 24))
label.pack()

# Change the width of the entry field
entry = tk.Entry(root, width=50, font=("Arial", 18))
entry.pack()

# Change the font size and width of the button
button = tk.Button(root, text="go", font=("Arial", 18), width=20)
button.pack()

root.mainloop()