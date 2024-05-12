import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
from AI import DataLoader, Country, AgricultureProblem, GraphSearch

def upload_file(file_var):
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    file_var.set(filename)

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

root = ThemedTk(theme="arc")  # Use the "arc" theme
root.title("Agricultural Optimization Project")  # Set window title

# Create a style
style = ttk.Style()

# Configure a larger button size
style.configure('TButton', font=('Arial', 20), padding=20)

# Create variables
products_file = tk.StringVar()
wilaya_file = tk.StringVar()
search_method = tk.StringVar()
output_var = tk.StringVar()

# Create file upload buttons with larger font and padding
products_button = ttk.Button(root, text="Upload Products File", command=lambda: upload_file(products_file), style='TButton')
wilaya_button = ttk.Button(root, text="Upload Wilaya File", command=lambda: upload_file(wilaya_file), style='TButton')

# Create dropdown menu with larger font
search_methods = ["UCS", "IDS", "A*"]  # Add your search methods here
search_dropdown = ttk.OptionMenu(root, search_method, *search_methods)
search_method.set(search_methods[0])  # Set default search method

# Create run button with larger font and padding
run_button = ttk.Button(root, text="Run", command=lambda: run_algorithm(products_file, wilaya_file, search_method, output_var), style='TButton')

# Create output label with larger font
output_label = ttk.Label(root, textvariable=output_var)

# Layout widgets
products_button.pack(pady=10)
wilaya_button.pack(pady=10)
search_dropdown.pack(pady=10)
run_button.pack(pady=10)
output_label.pack(pady=10)

root.mainloop()
