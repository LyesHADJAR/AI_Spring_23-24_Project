import tkinter as tk
from tkinter import filedialog

from main import DataLoader, Country, AgricultureProblem, GraphSearch

def upload_file(file_var, label_var):
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    file_var.set(filename)
    # Update the label to display the filename
    label_var.config(text=filename.split("/")[-1])  # Display only the filename

def run_algorithm(products_file, wilaya_file, search_method, output_var):
    # Load data using DataLoader
    cities_data, consumption, total_production, prices = DataLoader.load_country_data(wilaya_file.get(), products_file.get())

    # Create an instance of Country
    country = Country(cities_data, consumption, total_production, prices)

    # Create an instance of AgricultureProblem
    problem = AgricultureProblem(country, search_method.get())

    # Create an instance of GraphSearch
    search = GraphSearch(problem, search_method.get())

    # Perform the search
    result = search.general_search()

    # Output the result
    output_var.set(result)

root = tk.Tk()
root.title("Agricultural Optimization Project")

# Set window size
root.geometry("800x500")

# Green theme
root.configure(bg="#2E8B57")  # Set background color

# Create variables
products_file = tk.StringVar()
wilaya_file = tk.StringVar()
search_method = tk.StringVar()
output_var = tk.StringVar()

# Define button style
button_style = {"bg": "white", "fg": "black", "activebackground": "#2E8B57", "activeforeground": "white", "highlightthickness": 0, "borderwidth": 0, "font": ("Helvetica", 12, "bold")}

# Create shadows for buttons
def create_shadow_button(master, text, command, width):
    shadow_button = tk.Button(master, text=text, command=command, **button_style, width=width)
    shadow_button.pack(side="top", pady=10, anchor="center")
    return shadow_button

# Create file upload buttons with shadows
products_label = tk.Label(root, text="No file selected", bg="white", fg="black")  # Initial label
products_shadow_button = create_shadow_button(root, "Upload Products File", lambda: upload_file(products_file, products_label), width=20)
products_button = tk.Button(root, text="Upload Products File", command=lambda: upload_file(products_file, products_label), **button_style, width=20)

wilaya_label = tk.Label(root, text="No file selected", bg="white", fg="black")  # Initial label
wilaya_shadow_button = create_shadow_button(root, "Upload Wilaya File", lambda: upload_file(wilaya_file, wilaya_label), width=20)
wilaya_button = tk.Button(root, text="Upload Wilaya File", command=lambda: upload_file(wilaya_file, wilaya_label), **button_style, width=20)

# Create dropdown menu
search_methods = ["UCS", "IDS", "A*"]  # Add your search methods here
search_dropdown = tk.OptionMenu(root, search_method, *search_methods)
search_method.set(search_methods[0])  # Set default search method
search_dropdown.config(bg="white", fg="black", highlightbackground="#2E8B57", activebackground="#2E8B57", activeforeground="white", font=("Helvetica", 12, "bold"))
search_dropdown.pack(side="top", pady=10, anchor="center")

# Create run button with shadow
run_shadow_button = create_shadow_button(root, "Run", lambda: run_algorithm(products_file, wilaya_file, search_method, output_var), width=20)
run_button = tk.Button(root, text="Run", command=lambda: run_algorithm(products_file, wilaya_file, search_method, output_var), **button_style, width=20)

# Create output label
output_label = tk.Label(root, textvariable=output_var, bg="white", fg="black")
output_label.pack(side="top", pady=10, anchor="center")

# Pack file upload labels
products_label.pack(side="top", pady=10, anchor="center")
wilaya_label.pack(side="top", pady=10, anchor="center")

root.mainloop()
