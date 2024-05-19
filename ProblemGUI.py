import customtkinter as ctk
from tkinter import filedialog, messagebox
import io
import sys
import csv
from DataLoader import DataLoader
from main import mycountry, search_for_year
import tkinter as tk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Project GUI")
        self.geometry("1000x1200")
        
        # Set dark mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")  # You can choose 'blue' or 'green'

        self.wilaya_file = None
        self.product_file = None

        self.font_size = 17
        self.font = ("Helvetica", self.font_size)
        self.title_font = ("Montserrat", self.font_size + 20, "bold")

        # Add the title label
        self.title_label = ctk.CTkLabel(self, text="AGRICULTURAL LAND OPTIMIZER", font=self.title_font)
        self.title_label.pack(pady=30, anchor=ctk.CENTER)

        # Create a frame to hold the file selection buttons and search method selection
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20, padx=20, anchor=ctk.CENTER)

        # Add the file selection buttons
        self.upload_wilaya_button = ctk.CTkButton(button_frame, text="Upload Wilaya CSV", command=self.upload_wilaya, font=self.font)
        self.upload_wilaya_button.pack(side=ctk.LEFT, padx=20)

        self.upload_product_button = ctk.CTkButton(button_frame, text="Upload Product CSV", command=self.upload_product, font=self.font)
        self.upload_product_button.pack(side=ctk.LEFT, padx=20)

        # Add the search method selection
        self.search_method_var = ctk.StringVar(self)
        self.search_method_var.set("Select Search Method")
        self.search_methods = ["Select Search Method", "IDA_Star", "IDS", "steepest", "UCS"]

        self.search_menu = ctk.CTkOptionMenu(button_frame, variable=self.search_method_var, values=self.search_methods, font=self.font)
        self.search_menu.pack(side=ctk.LEFT, padx=20)

        # Add the search button and export button in a separate frame
        action_frame = ctk.CTkFrame(self)
        action_frame.pack(pady=20, anchor=ctk.CENTER)

        # Add the "Export to CSV" button
        self.export_button = ctk.CTkButton(action_frame, text="Export to CSV", command=self.save_output_to_csv, state=ctk.NORMAL, font=self.font)
        self.export_button.pack(side=ctk.LEFT, padx=10)

        # Add the search button
        self.search_button = ctk.CTkButton(action_frame, text="Search", command=self.perform_search, fg_color="red", font=self.font, state=ctk.NORMAL)
        self.search_button.pack(side=ctk.LEFT, padx=10)

        # Create a frame for the text field and scrollbar
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=10, pady=20)

        self.output_text = ctk.CTkTextbox(text_frame, wrap=ctk.WORD, height=20, width=50)
        self.output_text.configure(font=("Courier", self.font_size))  # Use a monospaced font like Courier
        self.output_text.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        
    def upload_wilaya(self):
        self.wilaya_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.wilaya_file:
            self.upload_wilaya_button.configure(text=self.wilaya_file.split("/")[-1])
        else:
            messagebox.showerror("Error", "Failed to upload Wilaya CSV file")

    def upload_product(self):
        self.product_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.product_file:
            self.upload_product_button.configure(text=self.product_file.split("/")[-1])
        else:
            messagebox.showerror("Error", "Failed to upload Product CSV file")

    
    def perform_search(self):
        if not self.wilaya_file or not self.product_file:
            messagebox.showerror("Error", "Please upload both CSV files")
            return
    
        search_method = self.search_method_var.get()
        if search_method == "Select Search Method":
            messagebox.showerror("Error", "Please select a search method")
            return
    
        self.search_button.configure(text="Searching...", state=ctk.DISABLED)
        self.update_idletasks()
    
        try:
            cities_data, consumption, total_production, prices = DataLoader.load_country_data(self.wilaya_file, self.product_file)
            country = mycountry(cities_data, consumption, prices)
    
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
    
            search_for_year(country, search_method)
    
            sys.stdout = old_stdout
    
            output = redirected_output.getvalue()
            self.output_text.delete(1.0, ctk.END)
    
            # Split the output into lines and insert into the text widget
            for line in output.split('\n'):
                self.output_text.insert(ctk.END, line + '\n')
    
            self.highlight_text("[ >>>>> SEARCH FOR SPRING SEASON PLAN TOOK <<<<< ]: ", "#39FF14")
            self.highlight_text("[ >>>>> SEARCH FOR SUMMER SEASON PLAN TOOK <<<<< ]: ", "#39FF14")
            self.highlight_text("[ >>>>> SEARCH FOR FALL SEASON PLAN TOOK <<<<< ]: ", "#39FF14")
            self.highlight_text("[ >>>>> SEARCH FOR WINTER SEASON PLAN TOOK <<<<< ]: ", "#39FF14")
            self.highlight_text("[ >>>>> SEARCH FOR YEAR PLAN TOOK <<<<< ]", "#FFFF00")
    
            self.search_button.configure(text="Done!", state=ctk.NORMAL)
    
        except Exception as e:
            self.search_button.configure(text="Search", state=ctk.NORMAL)
            messagebox.showerror("Error", f"An error occurred: {e}")
    
        self.search_button.configure(text="Done!", state=ctk.NORMAL)


    def highlight_text(self, pattern, color):
        start_idx = self.output_text.search(pattern, "1.0", ctk.END)
        while start_idx:
            end_idx = f"{start_idx} lineend"
            self.output_text.tag_add(pattern, start_idx, end_idx)
            self.output_text.tag_config(pattern, foreground=color)
            start_idx = self.output_text.search(pattern, end_idx, ctk.END)
            
    def save_output_to_csv(self):
        output_text = self.output_text.get("1.0", ctk.END).strip()
        lines = output_text.split("\n")

        with open("output.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for line in lines:
                if line.strip():  # Check if the line is not empty
                    fields = [field.strip() for field in line.split('|')]  # Split using '|' and strip any extra spaces
                    writer.writerow(fields)

if __name__ == "__main__":
    app = App()
    app.mainloop()
