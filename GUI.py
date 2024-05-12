import tkinter as tk
from tkinter import messagebox

def run_algorithm():
    # This function will run your algorithm
    # You can access the inputs using input_var.get() and output the results using output_var.set()
    # If your algorithm takes a long time to run, you might want to run it in a separate thread to avoid blocking the GUI
    pass

def about():
    # This function will show an "About" dialog
    messagebox.showinfo("About", "This is a GUI for the Agriculture Problem")

root = tk.Tk()

# Create frames
input_frame = tk.Frame(root)
output_frame = tk.Frame(root)
controls_frame = tk.Frame(root)

# Layout frames
input_frame.pack()
output_frame.pack()
controls_frame.pack()

# Create input widgets
input_label = tk.Label(input_frame, text="Input")
input_var = tk.StringVar()
input_entry = tk.Entry(input_frame, textvariable=input_var)

# Layout input widgets
input_label.pack(side=tk.LEFT)
input_entry.pack(side=tk.LEFT)

# Create output widgets
output_label = tk.Label(output_frame, text="Output")
output_var = tk.StringVar()
output_label2 = tk.Label(output_frame, textvariable=output_var)

# Layout output widgets
output_label.pack(side=tk.LEFT)
output_label2.pack(side=tk.LEFT)

# Create control widgets
run_button = tk.Button(controls_frame, text="Run", command=run_algorithm)
about_button = tk.Button(controls_frame, text="About", command=about)

# Layout control widgets
run_button.pack(side=tk.LEFT)
about_button.pack(side=tk.LEFT)

root.mainloop()
