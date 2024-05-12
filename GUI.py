import customtkinter as ctk
from tkinter import filedialog, messagebox
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

root = ctk.CTk()  # Use the CTk class from CustomTkinter
root.title("Agricultural Optimization Project")  # Set window title

# Create variables
products_file = ctk.StringVar()
wilaya_file = ctk.StringVar()
search_method = ctk.StringVar()
output_var = ctk.StringVar()

# Create file upload buttons
products_button = ctk.CTkButton(root, text="Upload Products File", command=lambda: upload_file(products_file))
wilaya_button = ctk.CTkButton(root, text="Upload Wilaya File", command=lambda: upload_file(wilaya_file))

# Create dropdown menu
search_methods = ["UCS", "IDS", "A*"]  # Add your search methods here
search_dropdown = ctk.CTkOptionMenu(root, search_method, *search_methods)
search_method.set(search_methods[0])  # Set default search method

# Create run button
run_button = ctk.CTkButton(root, text="Run", command=lambda: run_algorithm(products_file, wilaya_file, search_method, output_var))

# Create output label
output_label = ctk.CTkLabel(root, textvariable=output_var)

# Layout widgets
products_button.pack(pady=10)
wilaya_button.pack(pady=10)
search_dropdown.pack(pady=10)
run_button.pack(pady=10)
output_label.pack(pady=10)

root.mainloop()
